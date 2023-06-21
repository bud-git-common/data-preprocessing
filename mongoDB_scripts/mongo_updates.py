import json
import pymongo
import certifi
ca = certifi.where()

def insert_json_items(json_file, collection_name):
    # Connect to MongoDB
    uri = 'mongodb+srv://inference_user:PrNLLcDRhEz4en9Q@budecosystem.qig24.mongodb.net/?retryWrites=true&w=majority'
    client = pymongo.MongoClient(uri,tlsCAFile=ca)
    db = client['BudCollector']
    collection = db[collection_name]

    # Load JSON data from file
    with open(json_file) as file:
        data = json.load(file)

    # Iterate over items and insert into MongoDB
    for category, items in data.items():
        for item in items:
            collection.insert_one(item)

    # Close the MongoDB connection
    client.close()
    print("mongo update completed")


# Usage example
json_file_path = "../dataset_folder/screenlane.json"
collection_name = 'screenlane_data'
insert_json_items(json_file_path, collection_name)
