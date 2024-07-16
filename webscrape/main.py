# webscrape/main.py
from parsers.collection import CollectionParser
from parsers.product import ProductParser

if __name__ == "__main__":
    try:
        collection_parser = CollectionParser()
        # collection_parser.run()

        # product_parser = ProductParser()
        # product_parser.parse_urls_per_collection()
        # product_parser.parse_product_info()

    except Exception as e:
        print(e)
