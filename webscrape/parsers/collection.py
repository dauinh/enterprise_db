# webscrape/parsers/collection.py
import re
from selenium.webdriver.common.by import By
from webscrape.crawler import Crawler
from webscrape.config import BASE_URL


class CollectionParser:
    def __init__(self, collection_file: str):
        self.crawler = Crawler()
        self.collection_file = collection_file

    def fetch(self) -> None:
        return self.crawler.fetch("https://www.muji.us/collections/")

    def get_collections(self) -> list:
        self.fetch()
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
    
    def run(self) -> None:
        """Parse collections urls from Muji Collections page."""
        try:
            urls = self.get_collections()
            self.crawler.save_urls(self.collection_file, urls)
        except Exception as e:
            print(e)
        finally:
            self.crawler.quit()
