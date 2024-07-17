# webscrape/tests/test_crawler.py
import pytest
from webscrape.storage import CSVStorage
from webscrape.parsers.product import ProductParser


@pytest.mark.skip()
class TestProductParser:
    @pytest.fixture(scope="module")
    def parser(self):
        parser = ProductParser()
        yield parser

    @pytest.fixture(scope="module")
    def urls(self, tmpdir, parser):
        parser.url = "https://www.muji.us/collections/"
        parser.crawler.fetch(parser.url)
        return parser.get_collections()