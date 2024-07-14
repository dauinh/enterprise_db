# webscrape/crawler.py
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

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

    # TODO: rewrite to fit new change
    def parse_collections(self) -> list:
        """Parse collections urls from Muji Collections page.

        Return:
            results (list): list of urls
        """
        links = self.driver.find_elements(By.TAG_NAME, "a")
        results = []
        for l in links:
            url = l.get_attribute("href")
            x = re.search(".*/collections/[\w-]*$", url)
            if x:
                results.append(url)

        return results

    def parse_products_per_collection(self) -> list:
        """Parse product urls from given Muji collection page.

        Return:
            results (list): list of urls
        """
        self.driver.implicitly_wait(2)
        products = self.driver.find_elements(By.CLASS_NAME, "productgrid--item")
        results = []
        for p in products:
            url = p.get_attribute("data-product-quickshop-url")
            if url: results.append(url)

        # Parse by alternative method
        if len(results) == 0: results = self.parse_alt_products()

        return results
    
    def parse_alt_products(self) -> list:
        """Special parser for collections/new-arrivals.
        Load all products then get urls from product title.

        Return:
            results (list): list of urls
        """
        # Load all products
        load_text = WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='ns-pagination-container']/div"))
        )
        total_products = load_text.text.split()[-1]
        self.fetch(f"{self.current_page}?products.size={total_products}")

        # Parse urls
        titles = WebDriverWait(self.driver, 2).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "productitem--title"))
        )
        # print(len(titles), 'titles')
        results = []
        for t in titles:
            link = t.find_element(By.TAG_NAME, "a")
            url = link.get_attribute("href")
            results.append(url)

        return results

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


if __name__ == "__main__":
    file = CSVStorage("data/collections.csv")
    collections = file.read()
    seen = set()

    for i, c in enumerate(collections):
        print(i, c)
        crawler = Crawler()
        url = c[0]
        save_file_name = url.split('/')[-1]

        try:
            crawler.fetch(url)
            if url not in seen:
                res = crawler.parse_products_per_collection()
                if not res:
                    print("Cannot scrape", save_file_name)
                else:
                    crawler.save_urls(save_file_name, res)
                    seen.add(url)
        except Exception as e:
            print("Cannot scrape", save_file_name)
            print(e)
            continue
        finally:
            crawler.quit()