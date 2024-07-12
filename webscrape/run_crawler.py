# webscrape/run_crawler.py
from crawler import Crawler

if __name__ == "__main__":
    crawler = Crawler()
    try:
        url = "https://www.muji.us/collections/"
        crawler.fetch(url)
        urls = crawler.parse_collections_urls()
        crawler.save_to_csv("collections", urls)

    except Exception as e:
        print(e)
    finally:
        crawler.quit()
