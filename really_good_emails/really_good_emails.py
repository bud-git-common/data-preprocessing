import requests
import os
import json
import time

def download_image(url, destination_folder):
    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Extract the image file name from the URL
    filename = url.split("/")[-1]

    # Build the complete path to save the image
    destination_path = os.path.join(destination_folder, filename)

    try:
        # Send a GET request to the image URL
        response = requests.get(url, stream=True)
        time.sleep(10)
        # Check if the request was successful
        if response.status_code == 200:
            # Open the destination file and write the image data to it
            with open(destination_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Image downloaded successfully: {filename}")

            # Return the downloaded file name
            return filename
        else:
            print("Failed to download image. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error occurred while downloading the image:", str(e))
    return None


def save_failed_url(url, output_file_path):
    # Save the failed URL to a new text file
    with open(output_file_path, "a") as file:
        file.write(url + "\n")


# Example usage
json_file_path = "../dataset_folder/really_good_emails/really_good_emails_images.json"
destination_folder = "../dataset_folder/really_good_emails/really_good_emails/images"  # Specify the folder where you want to save the images
failed_urls_file_path = "../dataset_folder/really_good_emails/failed_urls.txt"

try:
    # Open the JSON file
    with open(json_file_path) as file:
        # Load the JSON data as a list of dictionaries
        data_list = json.load(file)

        # Iterate over each dictionary in the list
        for data in data_list:
            # Extract the image URL from the dictionary
            image_url = data.get("img_full")

            # Skip dictionary if "img_url" key is not present
            if not image_url:
                continue

            # Download the image and get the downloaded file name
            downloaded_filename = download_image(image_url, destination_folder)

            # Check if the image was downloaded successfully
            if downloaded_filename:
                # Add the downloaded file name to the dictionary
                data["image_name"] = downloaded_filename
            else:
                # Save the failed URL to the text file
                save_failed_url(image_url, failed_urls_file_path)

    # Create a new JSON file with the updated data
    new_json_file_path = "../dataset_folder/really_good_emails/really_good_emails_output.json"
    with open(new_json_file_path, "w") as new_file:
        json.dump(data_list, new_file, indent=4)
    print("JSON file updated with the downloaded file names.")
except FileNotFoundError:
    print("JSON file not found.")
except json.JSONDecodeError as e:
    print("Error occurred while parsing the JSON file:", str(e))
