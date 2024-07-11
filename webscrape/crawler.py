# webscrape/crawler.py
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from storage import CVSStorage

options = webdriver.FirefoxOptions()
options.add_argument("--headless")

class Crawler:
    def __init__(self):
        self.driver = webdriver.Firefox(options=options)

    def fetch(self, url):
        self.driver.get(url)
        return self.driver.page_source

    def parse_collections_links(self) -> list:
        """Parse collections links from Muji Collections page.

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

    def save_collections(self, links: list) -> None:
        """Save collection titles to CSV file.
        This function appends to existing CSV file, i.e. does not overwrite.

        Parameter:
            links (list): a list of urls that is `https://www.muji.us/collections/*`
        """
        save_file = CVSStorage("data/collections.csv")
        save_file.save(["No", "Collection"])
        for i, l in enumerate(links):
            collection = l.split("/")[-1]
            save_file.save([i + 1, collection])

    def parse_products_per_collection(self, collection_url: str) -> list:
        """Parse product links from given collection.

        Parameter:
            collection_url (str): url for selected collection

        Return:
            results (list): list of urls
        """
        products = self.driver.find_elements(By.CLASS_NAME, "productgrid--item")
        # results = []
        # for l in links:
        #     url = l.get_attribute("href")
        #     x = re.search(".*/collections/[\w-]*$", url)
        #     if x:
        #         results.append(url)
        # return results

    def quit(self):
        self.driver.quit()


if __name__ == "__main__":
    crawler = Crawler()
    file = CVSStorage("data/collections.csv")
    header, collections = file.read()
    print(len(collections), header)
    print(collections[:5])
