import json
import requests
import os


def download_images(json_file_path, output_folder):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    for recipe in data.get("recipes", []):
        image_url = recipe.get("image")
        if image_url:
            image_name = os.path.basename(image_url)  # Extract the filename from the image_url
            image_path = os.path.join(output_folder, image_name)  # Join the output_folder and image_name
            try:
                response = requests.get(image_url, stream=True)
                response.raise_for_status()

                # Determine the file extension based on the content type
                content_type = response.headers.get("Content-Type")
                if content_type:
                    extension = content_type.split("/")[-1]
                    if extension:
                        image_name = f"{os.path.splitext(image_name)[0]}.{extension}"
                        image_path = os.path.join(output_folder, image_name)

                with open(image_path, 'wb') as image_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        image_file.write(chunk)
                recipe["image_downloaded"] = 1  # Set the image_downloaded flag to 1
                recipe["image_name"] = image_name  # Update the image_name with the new filename
                print(f"Downloaded image: {image_name}")
            except Exception as e:
                recipe["image_downloaded"] = 0  # Set the image_downloaded flag to 0
                print(f"Error occurred while downloading image {image_name}: {str(e)}")

    # Write the updated JSON data to a new file
    output_json_file_path = json_file_path.replace(".json", "_updated.json")
    with open(output_json_file_path, 'w') as output_json_file:
        json.dump(data, output_json_file, indent=4)


# Example usage
json_file_path = "../dataset_folder/recipie_final_data.json"  # Replace with the path to your JSON file
output_folder = "../dataset_folder/recipie_images"  # Replace with the desired output folder path

download_images(json_file_path, output_folder)
