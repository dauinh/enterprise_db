# scripts/run_crawler.py
from crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler()
    try:
        url = 'https://www.muji.us/collections/'
        html = crawler.fetch(url)
        links = crawler.parse_collections_links(html)
        crawler.save_collections(links)
        
    except Exception as e:
        print(e)
    finally:
        crawler.quit()
