import pandas as pd
import os

def excel_to_json(excel_file, output_folder):
    # Load the Excel file
    xls = pd.ExcelFile(excel_file)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over each sheet in the Excel file
    for sheet_name in xls.sheet_names:
        # Read the sheet into a pandas DataFrame
        df = pd.read_excel(excel_file, sheet_name=sheet_name)

        # Convert the DataFrame to a JSON string
        json_data = df.to_json(orient='records')

        # Build the output file path
        output_file = os.path.join(output_folder, f"{sheet_name}.json")

        # Save the JSON data to a file
        with open(output_file, 'w') as file:
            file.write(json_data)

        print(f"Sheet '{sheet_name}' converted to JSON and saved as '{output_file}'")

# Example usage
excel_file = '/Users/sreelekshmyselvin/Downloads/pagecollective/pagecollective.xlsx'  # Replace with your Excel file path
output_folder = 'dataset_folder'  # Replace with the desired output folder path

excel_to_json(excel_file, output_folder)
