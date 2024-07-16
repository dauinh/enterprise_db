# webscrape/parsers/collection.py
import re
from selenium.webdriver.common.by import By
from webscrape.crawler import Crawler
from webscrape.config import BASE_URL

class CollectionParser:
    def __init__(self):
        self.crawler = Crawler()
        self.driver = self.crawler.driver
        self.url = BASE_URL + "/collections/"

    def run(self) -> None:
        """Parse collections urls from Muji Collections page."""
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
