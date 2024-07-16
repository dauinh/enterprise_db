# Muji Crawler

- [x] Get collections links
- [x] Save collections to cvs file
- [ ] Get all products
collections ~ specializations
    - [x] Implement headless driver and wait time
    - [x] Get product urls
    - [x] Remove duplicates from `collections.csv`
    - [x] Refactor crawler
    - [ ] Refactor to `run_crawler.py`
    - [ ] Write test
    - [x] Get product details
    - [x] Fix product detail size and color
- [ ] Check overlapping products
- [ ] Redesign ER model

> Product description use `<p>` and `<span>` interchangbly, so it's diffifcult to completely scrape

### Run tests
In `webscrape` directory, run `python -m pytest`