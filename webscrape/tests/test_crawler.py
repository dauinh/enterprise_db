# webscrape/tests/test_crawler.py
import pytest
from webscrape.crawler import Crawler


class TestCrawler:
    @pytest.fixture(scope="module")
    def crawler(self):
        crawler = Crawler()
        yield crawler
        crawler.quit()


    def test_fetch(self, crawler):
        url = "https://www.muji.us/collections/"
        crawler.fetch(url)
        assert "Collections — MUJI USA" == crawler.driver.title
