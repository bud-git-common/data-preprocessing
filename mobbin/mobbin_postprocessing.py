import json

def group_json_data(json_data):
    grouped_data = {"data": []}
    for item in json_data:
        app_name = item.get('application_name')
        flow_heading = item.get('flow_pattern_heading')
        flow_item = item.get('flow_pattern_item')

        # Find the existing entry for the app_name or create a new one
        app_entry = next((entry for entry in grouped_data["data"] if entry["application_name"] == app_name), None)
        if app_entry is None:
            app_entry = {"application_name": app_name, "app_icon_img_filename": item.get('app_icon_img_filename'), "tagline": item.get('tagline'), "platform": item.get('platform'), "app_category": item.get('app_category'), "flows": {}}
            grouped_data["data"].append(app_entry)

        # Find the existing entry for the flow_heading or create a new one
        flow_heading_entry = app_entry["flows"].get(flow_heading)
        if flow_heading_entry is None:
            flow_heading_entry = {}
            app_entry["flows"][flow_heading] = flow_heading_entry

        # Find the existing entry for the flow_item or create a new one
        flow_item_entry = flow_heading_entry.get(flow_item)
        if flow_item_entry is None:
            flow_item_entry = []
            flow_heading_entry[flow_item] = flow_item_entry

        # Remove unnecessary fields from the item before appending
        item.pop('flow_pattern_heading', None)
        item.pop('flow_pattern_item', None)
        item.pop('application_name', None)
        item.pop('app_icon_img_filename', None)
        item.pop('tagline', None)
        item.pop('platform', None)
        item.pop('app_category', None)

        flow_item_entry.append(item)

    return grouped_data

# Read JSON data from file
with open('/Users/sreelekshmyselvin/Downloads/mobbin_data/data/mobbin_web.json') as file:
    json_data = json.load(file)

# Group the JSON data
grouped_data = group_json_data(json_data)

# Save the grouped data as a new JSON file
with open('/Users/sreelekshmyselvin/Downloads/mobbin_data/data/mobbin_web_final.json', 'w') as file:
    json.dump(grouped_data, file, indent=2)

print("Grouped data saved as json")
