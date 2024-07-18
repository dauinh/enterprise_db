# webscrape/crawler.py
from selenium import webdriver
from webscrape.storage import CSVStorage

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")


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
        save_file = CSVStorage(file_name)
        save_file.clear()
        for u in urls:
            save_file.save([u])

    def quit(self):
        self.driver.quit()
