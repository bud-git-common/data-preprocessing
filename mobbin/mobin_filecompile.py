import os
import pandas as pd
import json

def process_excel_files(source_folder, output_file):
    # Get a list of all Excel files in the source folder
    excel_files = [file for file in os.listdir(source_folder) if file.endswith(".xlsx")]

    # Initialize an empty list to store the combined data
    combined_data = []

    # Iterate over each Excel file
    for file in excel_files:
        # Construct the full file path
        file_path = os.path.join(source_folder, file)

        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path)

        # Select the desired columns
        desired_columns = ['platform', 'application_name', 'tagline', 'app_category',
                           'app_icon_img_filename', 'flow_pattern_heading', 'flow_pattern_item',
                           'flow_pattern_img_filename', 'tag', 'hot_spot_style']
        df = df[desired_columns]

        # Convert the DataFrame to a list of dictionaries
        data_dict = df.to_dict(orient='records')

        # Append the data to the combined list
        combined_data.extend(data_dict)

    # Save the combined data as a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(combined_data, json_file, indent=4)

    print("Data processing and combining completed. The combined file is saved as JSON.")


# Example usage
source_folder = "/Users/sreelekshmyselvin/Downloads/mobbin_data"
output_file = "/Users/sreelekshmyselvin/Downloads/mobbin_data/data/mobbin_android.json"
process_excel_files(source_folder, output_file)
