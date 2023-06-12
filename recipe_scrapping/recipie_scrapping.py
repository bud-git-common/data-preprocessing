from recipe_scrapers import scrape_me
import json


def scrapper_recipes(file_path):
    data_scrapped = {
        "recipes": []
    }
    recipe_counter = 0  # Counter variable to track the number of scraped recipes

    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)

    for item in json_data.get("data", []):
        for website_data in item:
            website = website_data["website"]
            links = website_data.get("links", [])
            substring = website.replace("https://", "")

            for url in links:
                if substring not in url:
                    continue

                try:
                    scraper = scrape_me(url)
                    data_fetched = scraper.to_json()
                    data_fetched["image_name"] = data_fetched["image"].split("/")[-1]
                    data_scrapped["recipes"].append(data_fetched)
                    recipe_counter += 1  # Increment the recipe counter
                    print("Recipe Counter:", recipe_counter)

                    # Save the data as JSON after each recipe is fetched
                    with open("../dataset_folder/recipie_final_data.json", 'w') as json_file:
                        json.dump(data_scrapped, json_file, indent=4)

                except Exception as e:
                    print(f"Error occurred while scraping data from {url}: {str(e)}")
                    continue

    print("Scraping completed.")


file_path = "../dataset_folder/recipie_links.json"  # Replace with the path to your JSON file
data_scrapped = scrapper_recipes(file_path)
