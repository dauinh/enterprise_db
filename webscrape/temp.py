from storage import CSVStorage

products = CSVStorage("data/products.csv").read()
for p in products:
    print(p)