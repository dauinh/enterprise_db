# webscrape/tests/test_crawler.py
import pytest
from webscrape.storage import CSVStorage
from webscrape.parsers.collection import CollectionParser


@pytest.fixture(scope="module")
def expected_urls():
    return [
        "https://www.muji.us/collections/apparel",
        "https://www.muji.us/collections/new-arrivals",
        "https://www.muji.us/collections/women",
        "https://www.muji.us/collections/mens",
        "https://www.muji.us/collections/unisex",
        "https://www.muji.us/collections/stationery",
        "https://www.muji.us/collections/notebook",
        "https://www.muji.us/collections/pens",
        "https://www.muji.us/collections/home",
        "https://www.muji.us/collections/food",
    ]


@pytest.fixture(scope="module")
def temp_file(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    temp_file = temp_dir / "collection.csv"
    return temp_file


@pytest.fixture(scope="module")
def parser(temp_file):
    parser = CollectionParser(temp_file)
    yield parser
    parser.crawler.quit()


def test_fetch(parser):
    parser.fetch()
    assert "Collections — MUJI USA" == parser.crawler.driver.title


def test_get_collections(expected_urls, parser):
    urls = parser.get_collections()
    url_map = set(urls)
    for e in expected_urls:
        assert e in url_map


def test_run(expected_urls, temp_file, parser):
    parser.run()
    collections = CSVStorage(temp_file).read()
    collection_map = set([c[0] for c in collections])
    for e in expected_urls:
        assert e in collection_map
