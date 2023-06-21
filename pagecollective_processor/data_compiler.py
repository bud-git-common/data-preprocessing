import json

def group_json_data(json_data, group_key):
    grouped_data = {"data": []}
    for item in json_data:
        key_value = item.get(group_key)

        # Find the existing entry for the key value or create a new one
        key_entry = next((entry for entry in grouped_data["data"] if entry.get(group_key) == key_value), None)
        if key_entry is None:
            key_entry = {group_key: key_value, "items": []}
            grouped_data["data"].append(key_entry)

        # Remove the group key from the item before appending
        item.pop(group_key, None)
        key_entry["items"].append(item)

    return grouped_data

# Read JSON data from file
with open('../dataset_folder/pagecollective/product-data.json') as file:
    json_data = json.load(file)

group_key = 'div/category'  # Replace with the key based on which you want to group the data

# Group the JSON data
grouped_data = group_json_data(json_data, group_key)

# Save the grouped data as a new JSON file
with open('../dataset_folder/pagecollective/output/product-data-grouped.json', 'w') as file:
    json.dump(grouped_data, file, indent=2)

print("Grouped data saved as JSON")

