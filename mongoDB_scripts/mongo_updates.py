import json
from pymongo import MongoClient


def insert_json_items(json_file, collection_name):
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://inference_user:PrNLLcDRhEz4en9Q@budecosystem.qig24.mongodb.net/?retryWrites=true&w=majority')
    db = client['BudCollector']
    collection = db["sree_test"]

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
json_file_path = "/Users/sreelekshmyselvin/Downloads/mobbin_data/data/mobbin.json"
collection_name = 'mobbin_android_processed'
insert_json_items(json_file_path, collection_name)
