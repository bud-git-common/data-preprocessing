import os
import zipfile

def unzip_all_files(source_folder):
    # Iterate over all files in the source folder
    for file_name in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file_name)

        # Check if the file is a zip archive
        if zipfile.is_zipfile(file_path):
            # Create a destination folder with the same name as the zip file
            destination_folder = os.path.join(source_folder, os.path.splitext(file_name)[0])
            os.makedirs(destination_folder, exist_ok=True)

            # Open the zip file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Extract all files to the destination folder
                zip_ref.extractall(destination_folder)
                print(f"Extracted {file_name} to {destination_folder}")

# Specify the source folder containing the zip files
source_folder = '/Users/sreelekshmyselvin/Downloads/infograpify'

# Call the function to unzip all files
unzip_all_files(source_folder)
