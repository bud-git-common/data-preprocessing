def db_data_rertrival():
    import pymongo
    import json
    import certifi
    ca = certifi.where()
    from bson import ObjectId
    # Connect to MongoDB
    uri = 'mongodb+srv://inference_user:PrNLLcDRhEz4en9Q@budecosystem.qig24.mongodb.net/?retryWrites=true&w=majority'
    client = pymongo.MongoClient(uri, tlsCAFile=ca)
    database = client["BudCollector"]
    # Get references to the collections
    collection1 = database["mobbin_android_processed"]
    collection2 = database["mobbin_ios_processed"]
    collection3 = database["mobbin_web_processed"]
    # Define the key to match on
    key_to_match = "application_name"
    # Find the common values for the key in all collections
    common_values = set(collection1.distinct(key_to_match)) & set(collection2.distinct(key_to_match)) & set(
        collection3.distinct(key_to_match))
    # Initialize a list to store the matching documents
    matching_documents = []
    # Iterate over the common values and extract matching documents from each collection
    for value in common_values:
        documents1 = collection1.find({key_to_match: value})
        documents2 = collection2.find({key_to_match: value})
        documents3 = collection3.find({key_to_match: value})

        for doc in documents1:
            doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
            matching_documents.append(doc)
        for doc in documents2:
            doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
            matching_documents.append(doc)
        for doc in documents3:
            doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
            matching_documents.append(doc)
    # Convert the matching documents to JSON
    json_data = json.dumps(matching_documents, default=str)
    # Save the JSON data to a file
    with open("../dataset_folder/data_filtered.json", "w") as file:
        file.write(json_data)
    # Close the MongoDB connection
    client.close()


db_data_rertrival()
print("execution completed")
