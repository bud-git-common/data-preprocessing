from recipe_scrapers import scrape_me
import json

def scrapper_recipes(file_path):
    data_scrapped = {
        "recipes": []
    }
    recipe_counter = 0  # Counter variable to track the number of scraped recipes

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
                    recipe_counter += 1  # Increment the recipe counter
                    print(recipe_counter)

                    if recipe_counter >= 2500:
                        # Save the data as JSON
                        with open("../dataset_folder/recipies_final_data.json", 'w') as json_file:
                            json.dump(data_scrapped, json_file, indent=4)

                        print("Scraping completed.")
                        return  # Exit the function
                except Exception as e:
                    print(f"Error occurred while scraping data from {url}: {str(e)}")
                    continue

    # Save the data as JSON if the loop completes without reaching 2000 recipes
    with open("../dataset_folder/recipies_final_data.json", 'w') as json_file:
        json.dump(data_scrapped, json_file, indent=4)

    print("Scraping completed.")
file_path = "/Users/sreelekshmyselvin/PycharmProjects/Data_Processing/dataset_folder/2.json"  # Replace with the path to your JSON file
data_scrapped = scrapper_recipes(file_path)