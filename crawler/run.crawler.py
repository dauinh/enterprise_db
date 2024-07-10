# scripts/run_crawler.py
from crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler()
    try:
        url = 'https://www.muji.us/collections/'
        html = crawler.fetch(url)
        a = crawler.get_all_links(html)
        print(a)
    finally:
        crawler.quit()
