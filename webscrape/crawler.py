# webscrape/crawler.py
import re
from os import listdir

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from storage import CSVStorage

BASE_URL = "https://www.muji.us"

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
options.add_argument('--disable-blink-features=AutomationControlled')

# TODO: create separate classes for collection page crawler and product page crawler
class Crawler:
    def __init__(self):
        self.driver = webdriver.Firefox(options=options)
        self.current_page = None
        self.driver.delete_all_cookies()

    def fetch(self, url):
        self.driver.get(url)
        self.current_page = url
        return self.driver.page_source
    
    def save_urls(self, file_name: str, urls: list) -> None:
        """Save scraped urls to CSV file.

        Parameter:
            file_name (str): name of file
            urls (list): a list of urls
        """
        save_file = CSVStorage("data/" + file_name + ".csv")
        save_file.clear()
        for u in urls:
            save_file.save([u])
    
    def quit(self):
        self.driver.quit()


class CollectionParser:
    def __init__(self):
        self.crawler = Crawler()
        self.driver = self.crawler.driver
        self.url = BASE_URL + "/collections/"

    def run(self) -> None:
        """Parse collections urls from Muji Collections page.
        """
        try:
            self.crawler.fetch(self.url)
            urls = self.get_collections()
            self.crawler.save_urls("collections", urls)
        except Exception as e:
            print(e)
        finally:
            self.crawler.quit()

    def get_collections(self) -> list:
        links = self.crawler.driver.find_elements(By.TAG_NAME, "a")
        unique = set()
        results = []
        for l in links:
            url = l.get_attribute("href")
            x = re.search(".*/collections/[\w-]*$", url)
            if x and url not in unique:
                results.append(url)
                unique.add(url)

        return results


class ProductParser:
    def parse_urls_per_collection(self) -> None:
        """Parse product urls by collection from given Muji collection page.
        """
        collections = CSVStorage("data/collections.csv").read()
        for i, c in enumerate(collections):
            # if i > 2: break
            print(i, c)
            crawler = Crawler()
            url = c[0]
            save_file_name = "collections/" + url.split('/')[-1]
            try:
                crawler.fetch(url)
                res = self.get_urls_per_collection(crawler)
                if not res:
                    print("Cannot scrape", save_file_name)
                else:
                    crawler.save_urls(save_file_name, res)
            except Exception as e:
                print("Cannot scrape", save_file_name)
                print(e)
                continue
            finally:
                crawler.quit()

    def get_urls_per_collection(self, crawler: Crawler) -> list:
        crawler.driver.implicitly_wait(2)
        products = crawler.driver.find_elements(By.CLASS_NAME, "productgrid--item")
        results = []
        # Parse by alternative method
        if len(products) == 0: results = self.get_from_alt_collection(crawler)

        unique = set()
        for p in products:
            url = p.get_attribute("data-product-quickshop-url")
            if url and url not in unique: 
                results.append(url)
                unique.add(url)

        return results
    
    def get_from_alt_collection(self, crawler: Crawler) -> list:
        """Special parser for collections with different layout.
        Load all products then get urls from product title.

        Return:
            results (list): list of urls
        """
        # Load all products
        load_text = WebDriverWait(crawler.driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='ns-pagination-container']/div"))
        )
        total_products = load_text.text.split()[-1]
        crawler.fetch(f"{crawler.current_page}?products.size={total_products}")

        # Parse urls
        titles = WebDriverWait(crawler.driver, 2).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "productitem--title"))
        )
        # print(len(titles), 'titles')
        results = []
        unique = set()
        for t in titles:
            link = t.find_element(By.TAG_NAME, "a")
            url = link.get_attribute("href")
            if url not in unique:
                results.append(url)
                unique.add(url)

        return results
    
    def parse_product_info(self) -> None:
        products_file = CSVStorage("data/products.csv")
        products_file.clear()

        # iterate each collection
        collection_files = [f for f in listdir("data/collections")]
        for i, collection in enumerate(collection_files):
            if i < 4: continue
            if i > 4: break
            print(i, collection)
            product_urls = CSVStorage(f"data/collections/{collection}").read()

            # iterate each product url
            for i, url in enumerate(product_urls):
                if i > 2: break
                url = url[0]
                print(url)
                # check if url is relative, add base url if not
                if "https" != url[:5]:
                    url = BASE_URL + url

                # save product info to products.csv
                info = self.get_product_info(url)
                products_file.save([collection[:-4]] + info)

    def get_product_info(self, url) -> list:
        crawler = Crawler()
        try:
            crawler.fetch(url)
            crawler.driver.implicitly_wait(2)

            data = []
            # data cols: [title, price, color, size, description, product details, material & care]
            title = self.get_title(crawler.driver)
            data.append(title)

            price = self.get_price(crawler.driver)
            data.append(price)

            colors = self.get_colors(crawler.driver)
            data.append(colors)

            sizes = self.get_sizes(crawler.driver)
            data.append(sizes)

            description = self.get_description(crawler.driver)
            data.append(description)

            details, care = self.get_details_and_care(crawler.driver)
            data.append(details)
            data.append(care)

            return data
        except Exception as e:
            print("Error with", url)
            print(e)
        finally:
            crawler.quit()

    def get_title(self, driver) -> str:
        try:
            title_element = driver.find_element(By.CLASS_NAME, "product-title")
            return title_element.text
        except Exception as e:
            print("Error getting product title")
            print(e)
            return ""

    def get_product_title(self, driver) -> str:
        try:
            title_element = driver.find_element(By.CLASS_NAME, "product-title")
            return title_element.text
        except Exception as e:
            print("Error getting product title")
            print(e)
            return ""
        
    def get_price(self, driver) -> str:
        try:
            current_price_element = driver.find_element(By.CLASS_NAME, "price__current")
            price_element = current_price_element.find_element(By.CLASS_NAME, "money")
            return price_element.text
        except Exception as e:
            print("Error getting product price")
            print(e)
            return ""
        
    def get_colors(self, driver) -> list:
        colors = []
        try:
            options = driver.find_elements(By.CLASS_NAME, "options-selection__option-swatch-wrapper")
            for opt in options:
                c = opt.get_attribute("data-swatch-tooltip")
                colors.append(c)
        except Exception as e:
            print("Error getting product colors")
            print(e)
        finally:
            return colors
        
    def get_sizes(self, driver) -> list:
        sizes = []
        try:
            options = driver.find_elements(By.CLASS_NAME, "options-selection__option-value-name")
            for opt in options:
                sizes.append(opt.text)
        except Exception as e:
            print("Error getting product sizes")
            print(e)
        finally:
            return sizes
        
    def get_description(self, driver) -> str:
        description = ""
        try:
            description_element = driver.find_element(By.CLASS_NAME, "product-description")
            texts = description_element.find_elements(By.TAG_NAME, "p")
            full_text = [t.text for t in texts]
            if all(full_text) != None:
                description = "\n".join(full_text)
        except Exception as e:
            print("Error getting product description")
            print(e)
        finally:
            return description
        
    def get_details_and_care(self, driver) -> list[str, str]:
        try:
            collapsibles = driver.find_elements(By.CLASS_NAME, "collapsible-tab__text")
            details = collapsibles[0].find_elements(By.TAG_NAME, "p")
            care = collapsibles[1].find_elements(By.TAG_NAME, "p")
            details_text = [x.text for x in details]
            care_text = [x.text for x in care]
            return ["\n".join(details_text), "\n".join(care_text)]
        except Exception as e:
            print("Error getting product details and care")
            print(e)
            return [[], []]

if __name__ == "__main__":
    # collection_parser = CollectionParser()
    # collection_parser.run()

    product_parser = ProductParser()
    product_parser.parse_product_info()