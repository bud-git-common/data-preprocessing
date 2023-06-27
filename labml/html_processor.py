import csv
import json
import os
from bs4 import BeautifulSoup
import requests

def parse_html_to_json(url, category, name):
    try:
        # Make a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check for any HTTP errors

        html_code = response.content

        # Parse the HTML content
        soup = BeautifulSoup(html_code, 'html.parser')

        # Find the <h1> tag for the title
        h1_tag = soup.find('h1')
        title = h1_tag.get_text(strip=True) if h1_tag else ""

        # Find all sections
        sections = soup.find_all('section') + soup.find_all('div', class_='section')

        # Extract the content within <p> and <h2> tags for each section
        data = {"category": category, "name": name,"title":title,"content": []}
        current_section = None  # Track the current section data
        current_h2_key = None  # Track the current <h2> tag key
        for section in sections:
            h2_tag = section.find('h2')
            if h2_tag:
                if current_section is not None:
                    data["content"].append(current_section)

                current_h2_key = h2_tag.get_text(strip=True)
                current_section = {"subtitle": current_h2_key, "explanation": []}
            elif current_section is not None:
                p_tags = section.find_all('p')
                for p_tag in p_tags:
                    p_text = p_tag.get_text(strip=True)
                    current_section["explanation"].append(p_text)

        # Add the last section data if it exists
        if current_section is not None:
            data["content"].append(current_section)

        # Remove empty arrays and corresponding data from the "content" key
        data["content"] = [section for section in data["content"] if any(section.values())]

        # Convert data to JSON
        json_data = json.dumps(data, indent=4)

        # Save JSON file with the name as the filename
        file_name = "{}.json".format(name) if name else "content_data.json"
        output_file_path = os.path.join("../labml/parsed_data", file_name)
        with open(output_file_path, 'w') as file:
            file.write(json_data)

        print("Content extracted and saved to '{}'".format(output_file_path))

    except requests.exceptions.RequestException as e:
        # Save failed URL to a text file
        failed_urls_file = "../labml/failed_urls.txt"
        with open(failed_urls_file, 'a') as file:
            file.write("{} - {}\n".format(url, str(e)))
        print("Failed to process URL: {}".format(url))


# Read URLs from a CSV file and process them
def process_urls_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            url = row['Url']
            category = row['Category']
            name = row['Title']
            parse_html_to_json(url, category, name)

# Example usage:
csv_file_path = '../labml/labmlUrlList_CSV.csv'
process_urls_from_csv(csv_file_path)
