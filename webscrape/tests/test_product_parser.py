# webscrape/tests/test_crawler.py
import pytest
from unittest.mock import patch
from webscrape.storage import CSVStorage
from webscrape.parsers.collection import CollectionParser
from webscrape.parsers.product import ProductParser


@pytest.mark.skip
class TestProductParser:
    @pytest.fixture(scope="module")
    def parser(self):
        return ProductParser()


    @pytest.fixture(scope="module")
    def collections(self):
        parser = CollectionParser()
        parser.url = "https://www.muji.us/collections/"
        parser.crawler.fetch(parser.url)
        yield parser.get_collections()
        parser.crawler.quit()


    def test_parse_urls_per_collection(self, collections):
        print(collections)
        assert False