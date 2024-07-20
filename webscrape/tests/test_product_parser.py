# webscrape/tests/test_crawler.py
import os
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
        "https://www.muji.us/collections/unisex",
        "https://www.muji.us/collections/stationery",
        "https://www.muji.us/collections/home"
    ]
    temp_dir = tmp_path_factory.mktemp("data")
    temp_file = temp_dir / "collection.csv"
    with open(temp_file, "w") as f:
        writer = csv.writer(f)
        for u in urls:
            writer.writerow([u])
    return temp_file


@pytest.fixture(scope="module")
def collection_dir(tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / "collections"
    path.mkdir()
    return path


@pytest.fixture(scope="module")
def parser(tmp_path_factory, collection_urls_file, collection_dir):
    temp_dir = tmp_path_factory.mktemp("data")
    temp_file = temp_dir / "products.csv"
    return ProductParser(collection_urls_file, collection_dir, temp_file)


def test_init(parser):
    assert len(parser.collections) == 5
    for url in parser.collections:
        assert url[:5] == "https"


def test_parse_urls_per_collection(parser, collection_dir):
    parser.parse_urls_per_collection()
    collection_files = [f for f in os.listdir(collection_dir)]
    assert len(collection_files) == 5
