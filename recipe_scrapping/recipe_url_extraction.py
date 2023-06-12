import json
from recipe_scrapers import scrape_me

def process_website(website):
    # Perform your desired operations with the website value
    try:
        scraper = scrape_me(website)
        raw_data = scraper.links()
        procesed_urls = []
        links = []
        for data in raw_data:
            temp = data["href"]
            links.append(temp)
        json_template = {"website": website, "links": links}
        procesed_urls.append(json_template)
        print(f"Processing website: {website}")
        return procesed_urls
    except:
        print(f"Error occurred while processing website {website}")

# Function to read JSON file and pass values to process_website()
def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        website_list = data.get("websites", [])
        extracted_data = {
            "data": []
        }
        for website in website_list:
           processed_data =  process_website(website)
           extracted_data["data"].append(processed_data)
    return extracted_data

def write_json_file(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
json_file_path = "../dataset_folder/recipies_websites.json"
output_json_file_path = "../dataset_folder/recipie_links.json"
result = read_json_file(json_file_path)
write_json_file(result, output_json_file_path)
print("execution completed")

