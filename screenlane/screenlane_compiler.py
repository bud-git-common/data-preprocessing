import pandas as pd
import json


def process_csv_file(csv_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Create an empty dictionary to store the grouped data
    grouped_data = {"data": []}

    # Group the data based on "url"
    grouped_df = df.groupby("url")

    # Iterate through each group
    for url, group in grouped_df:
        group_data = []

        # Iterate through each row in the group
        for index, row in group.iterrows():
            url_parts = url.split("/")
            imgurl_parts = row["imgurl"].split("/")

            # Keep the last string value
            application_name = url_parts[-2]
            platform = url_parts[-3]
            imgurl = imgurl_parts[-1]
            title = row["title"]

            # Append the item to the group data
            group_data.append({
                "imgurl": imgurl,
                "title": title
            })

        # Append the group data to the grouped data dictionary
        grouped_data["data"].append({
            "application_name": application_name,
            "platform": platform,
            "images": group_data
        })

    return grouped_data


def convert_to_json(grouped_data, output_file):
    # Convert the grouped data to JSON format
    json_data = json.dumps(grouped_data, indent=4)

    # Save the JSON data to a file
    with open(output_file, "w") as file:
        file.write(json_data)

    print("Grouped data saved as JSON")


# Example usage
csv_file = "../dataset_folder/screenlane.csv"  # Replace with the path to your CSV file
output_file = "../dataset_folder/screenlane.json"  # Replace with the desired path for the output JSON file

# Process the CSV file and obtain the grouped data
grouped_data = process_csv_file(csv_file)

# Convert the grouped data to JSON and save it
convert_to_json(grouped_data, output_file)
