# webscrape/tests/test_crawler.py
import pytest
from webscrape.storage import CSVStorage
from webscrape.parsers.collection import CollectionParser


@pytest.fixture(scope="module")
def parser():
    parser = CollectionParser()
    yield parser
    parser.crawler.quit()

@pytest.fixture(scope="module")
def urls(parser):
    parser.url = "https://www.muji.us/collections/"
    parser.crawler.fetch(parser.url)
    return parser.get_collections()


def test_get_collections(urls):
    assert len(urls) > 0, "Got no urls"
    assert all(urls) != None, "Some urls are empty" 


def test_save_collections(parser, urls):
    some_expected = [
        'https://www.muji.us/collections/apparel',
        'https://www.muji.us/collections/new-arrivals',
        'https://www.muji.us/collections/women',
        'https://www.muji.us/collections/mens',
        'https://www.muji.us/collections/unisex',
        'https://www.muji.us/collections/stationery',
        'https://www.muji.us/collections/notebook',
        'https://www.muji.us/collections/pens',
        'https://www.muji.us/collections/home',
        'https://www.muji.us/collections/food'
    ]
    parser.crawler.save_urls("tests/data/collections.csv", urls)
    collections = CSVStorage("data/collections.csv").read()
    collection_map = set([c[0] for c in collections])
    for e in some_expected:
        assert e in collection_map
