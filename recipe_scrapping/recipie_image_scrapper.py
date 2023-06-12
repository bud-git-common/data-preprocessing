import json
import urllib.request

def download_images(json_file_path, output_folder):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    for recipe in data.get("recipes", []):
        image_url = recipe.get("image")
        if image_url:
            image_name = recipe.get("image_name")
            image_path = output_folder + '/' + image_name
            try:
                urllib.request.urlretrieve(image_url, image_path)
                print(f"Downloaded image: {image_name}")
            except Exception as e:
                print(f"Error occurred while downloading image {image_name}: {str(e)}")

# Example usage
output_json_file_path = "../dataset_folder/data1.json"  # Replace with the path to your output JSON file
output_folder = "../dataset_folder/recipie_images"  # Replace with the desired output folder path

download_images(output_json_file_path, output_folder)
