from recipe_scrapers import scrape_me
import json


def scrapper_recipes(file_path):
    data_scrapped = {
        "recipes": []
    }
    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)

    urls_list = []

    for item in json_data.get("data", []):
        for website_data in item:
            website = website_data["website"]
            links = website_data.get("links", [])
            urls_list.extend(links)
            substring = website.replace("https://", "")

            for url in urls_list[:]:
                if substring not in url:
                    urls_list.remove(url)

            for url in urls_list:
                print(url)
                try:
                    scraper = scrape_me(url)
                    data_fetched = scraper.to_json()
                    data_fetched["image_name"] = data_fetched["image"].split("/")[-1]
                    data_scrapped["recipes"].append(data_fetched)
                except Exception as e:
                    print(f"Error occurred while scraping data from {url}: {str(e)}")
                    continue

    return data_scrapped


# Example usage
file_path = "../dataset_folder/recipie_links.json"  # Replace with the path to your JSON file
data_scrapped = scrapper_recipes(file_path)

with open("../dataset_folder/recipies_final_data.json", 'w') as json_file:
    json.dump(data_scrapped, json_file, indent=4)

print("Scraping completed.")
