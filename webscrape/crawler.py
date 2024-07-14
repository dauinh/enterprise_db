# webscrape/crawler.py
import re

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

        Return:
            results (list): list of urls
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
    def parse_product_urls(self) -> None:
        """Parse product urls by collection from given Muji collection page.

        Return:
            results (list): list of urls
        """
        collections = CSVStorage("data/collections.csv").read()

        for i, c in enumerate(collections):
            if i > 2: break
            print(i, c)
            crawler = Crawler()
            url = c[0]
            save_file_name = "collections/" + url.split('/')[-1]
            try:
                crawler.fetch(url)
                res = self.get_product_urls(crawler)
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
        pass

    def get_product_urls(self, crawler: Crawler) -> list:
        driver = crawler.driver
        driver.implicitly_wait(2)
        products = driver.find_elements(By.CLASS_NAME, "productgrid--item")
        results = []
        for p in products:
            url = p.get_attribute("data-product-quickshop-url")
            if url: results.append(url)

        # Parse by alternative method
        if len(results) == 0: results = self.get_from_alt_collection(crawler)

        return results
    
    def get_from_alt_collection(self, crawler: Crawler) -> list:
        """Special parser for collections with different layout.
        Load all products then get urls from product title.

        Return:
            results (list): list of urls
        """
        driver = crawler.driver
        # Load all products
        load_text = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='ns-pagination-container']/div"))
        )
        total_products = load_text.text.split()[-1]
        crawler.fetch(f"{crawler.current_page}?products.size={total_products}")

        # Parse urls
        titles = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "productitem--title"))
        )
        # print(len(titles), 'titles')
        results = []
        for t in titles:
            link = t.find_element(By.TAG_NAME, "a")
            url = link.get_attribute("href")
            results.append(url)

        return results


if __name__ == "__main__":
    # collection_parser = CollectionParser()
    # collection_parser.run()

    product_parser = ProductParser()
    product_parser.parse_product_urls()