# tests/test_crawler.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from crawler import Crawler

@pytest.fixture(scope="module")
def crawler():
    crawler = Crawler()
    yield crawler
    crawler.quit()

def test_fetch(crawler):
    url = 'https://www.muji.us/collections/'
    html = crawler.fetch(url)
    assert '<title>Collections - MUJI USA</title>' in html

# def test_parse(crawler):
#     crawler.driver.get('http://example.com')
#     title = crawler.driver.find_element(By.TAG_NAME, 'title').get_attribute('innerText')
#     assert title == 'Example Domain'
