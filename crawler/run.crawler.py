# scripts/run_crawler.py
from crawler import Crawler
from storage import CVSStorage

if __name__ == '__main__':
    crawler = Crawler()
    try:
        url = 'https://www.muji.us/collections/'
        html = crawler.fetch(url)
        links = crawler.get_all_collections_links(html)
        
        save_file = CVSStorage('data.collections.csv')
        save_file.save(['No', 'Collection'])
        for i, l in enumerate(links):
            collection = l.split('/')[-1]
            save_file.save([i+1, collection])
    except Exception as e:
        print(e)
    finally:
        crawler.quit()
