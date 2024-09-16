# Enterprise Database Project

## Enterprise Crawler

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
- [ ] Put base url into .env file
- [ ] Refactor comment to hide enterprise

> Product description use `<p>` and `<span>` interchangbly, so it's diffifcult to completely scrape. Product details and care has diverse styling, so original HTML is retained

#### 3. Run tests

In `webscrape` directory, run `python -m pytest`

#### 4. Data cleaning & transform

- [x] Install necessary packages
- [x] Check overlapping products
- [x] Add quantity

## Enterprise DB
- [x] Set up FastAPI and SQLalchemy
- [x] Model `product` entity
- [x] Implement APIs for fetching product data
- [x] Model `collection` entity and relationship
- [x] Model `attribute` entity and relationship
- [ ] Implement APIs for collection and product attributes
- [x] Upload local data
- [ ] Model `transaction`
- [ ] Redesign APIs
- [ ] Implement customer/user interface and workflow (https://github.com/minimal-ui-kit/material-kit-react)
- [ ] Implement transaction APIs
- [ ] Generate data for store
- [ ] Use Selenium to generate user
