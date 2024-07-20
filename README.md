# Muji Database Project

## Muji Crawler

#### 1. Get collections
- [x] Get collections links
- [x] Save collections to cvs file

> collections ~ specializations

#### 2. Get products
- [x] Implement headless driver and wait time
- [x] Get product urls
- [x] Remove duplicates from `collections.csv`
- [x] Refactor crawler
- [x] Refactor to `run_crawler.py`
- [ ] Write test
- [x] Get product details
- [x] Fix product detail size and color
- [x] Implement start range for parsing product info
- [x] Save data, then check refactor
- [ ] Implement saving error messages/ failed urls

> Product description use `<p>` and `<span>` interchangbly, so it's diffifcult to completely scrape. Product details and care has diverse styling, so original HTML is retained

#### 3. Run tests

In `webscrape` directory, run `python -m pytest`

## Muji Analysis
- [ ] Install necessary packages

#### 1. Data cleaning & transform
- [ ] Check overlapping products
- [ ] Add quantity

## Muji DB
- [ ] Redesign ER model
