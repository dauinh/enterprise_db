# webscrape/tests/test_crawler.py
import pytest
from webscrape.crawler import Crawler


@pytest.fixture(scope="module")
def crawler():
    crawler = Crawler()
    yield crawler
    crawler.quit()


def test_fetch(crawler):
    url = "https://www.muji.us/collections/"
    crawler.fetch(url)
    assert "Collections — MUJI USA" == crawler.driver.title
