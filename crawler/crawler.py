# crawler/crawler.py
import re

from selenium import webdriver
from selenium.webdriver.common.by import By

from storage import CVSStorage


class Crawler:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def fetch(self, url):
        self.driver.get(url)
        return self.driver.page_source

    def parse_collections_links(self, html):
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

        Parameters:
            links (list): a list of urls that is `https://www.muji.us/collections/*`
        """
        save_file = CVSStorage('data/collections.csv')
        save_file.save(['No', 'Collection'])
        for i, l in enumerate(links):
            collection = l.split('/')[-1]
            save_file.save([i+1, collection])

    def quit(self):
        self.driver.quit()
