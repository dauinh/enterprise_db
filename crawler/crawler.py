# crawler/crawler.py
import re

from selenium import webdriver
from selenium.webdriver.common.by import By

class Crawler:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def fetch(self, url):
        self.driver.get(url)
        return self.driver.page_source

    def get_all_links(self, html):
        links = self.driver.find_elements(By.TAG_NAME, "a")
        results = []
        for l in links:
            url = l.get_attribute("href")
            x = re.search(".*/collections/[\w-]*$", url)
            if x:
                results.append(url)
        return results

    def quit(self):
        self.driver.quit()
