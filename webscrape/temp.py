from os import listdir

collection_files = [f for f in listdir("data/collections")]
for i, collection in enumerate(collection_files):
    print(i, collection)