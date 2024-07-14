# webscrape/run_crawler.py
from crawler import CollectionParser

if __name__ == "__main__":
    try:
        collection_parser = CollectionParser()
        collection_parser.run()

    except Exception as e:
        print(e)
