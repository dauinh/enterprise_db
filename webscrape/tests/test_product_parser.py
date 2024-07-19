# webscrape/tests/test_crawler.py
import csv
import pytest
from unittest.mock import patch
from webscrape.storage import CSVStorage
from webscrape.parsers.collection import CollectionParser
from webscrape.parsers.product import ProductParser


@pytest.fixture(scope="module")
def collection_urls_file(tmp_path_factory):
    urls = [
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
    temp_dir = tmp_path_factory.mktemp("data")
    temp_file = temp_dir / "collection.csv"
    with open(temp_file, "a") as f:
        writer = csv.writer(f)
        writer.writerow(urls)
    return temp_file


@pytest.fixture(scope="module")
def collection_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("data") / "collections"


@pytest.fixture(scope="module")
def parser(tmp_path_factory, collection_urls_file, collection_dir):
    temp_dir = tmp_path_factory.mktemp("data")
    temp_file = temp_dir / "products.csv"
    return ProductParser(collection_urls_file, collection_dir, temp_file)


def test_init(parser):
    for url in parser.collections:
        assert url[:5] == "https"


@pytest.mark.skip
def test_parse_urls_per_collection(collections):
    print(collections)
    assert False
