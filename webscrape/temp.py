from os import listdir
from webscrape.storage import CSVStorage

collection_files = [f for f in listdir("data/collections")]
for i, collection in enumerate(collection_files):
    product_urls = CSVStorage(f"data/collections/{collection}").read()
    print(i, len(product_urls), collection)

product_file = CSVStorage("data/products.csv").read()
print(len(product_file))
