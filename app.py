import requests
from bs4 import BeautifulSoup
import os
import time
import re
import urllib
import urllib.request
from pathlib import Path

# -*- coding: utf-8 -*-

# Main goal:
# Get all collateral adjectives and the animal names related to them from the second table with beutiful soup from https://en.wikipedia.org/wiki/List_of_animal_names


class Animal:
    def __init__(self, name, collateral_adjectives, url):
        self.name = name
        self.collateral_adjectives = collateral_adjectives
        self.url = url

    # Bonus:
    # Download the picture of each animal into /tmp/ and add a local link when displaying the animals.
    # To do so, we iterate on each animal object and call the download_animal_image mathod.

    def download_animal_image(url: str):
        r = requests.get(f"https://en.wikipedia.org{url}")
        soup = BeautifulSoup(r.text, "lxml")
        try:
            image = soup.findAll(
                'img', {'src': re.compile('.jpg', re.IGNORECASE)})[0]['src']
        except Exception as e:
            print(e)
            return "No Image Found"

        full_url_for_image = f"https:{image}"

        url_animal_name = url.split("/")[-1]
        print(url_animal_name)

        PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
        # Change sub_dir for the subdirectory you want to save the images in.
        sub_dir = f"tmp"
        if os.path.exists(sub_dir) is False:
            os.mkdir(sub_dir)
        local_path = Path(f'{PROJECT_DIR}/{sub_dir}/{url_animal_name}.jpg')
        print(local_path)
        urllib.request.urlretrieve(full_url_for_image, local_path)
        return local_path

# This function is our "main" function. Call it to get all the adjectives-names.
# We also call Animal.download_animal_image(url) and output into html for the bonus.


def get_adj_name_pairs():
    r = requests.get("https://en.wikipedia.org/wiki/List_of_animal_names")
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find_all("table", class_="wikitable sortable")[1]

    all_adj_name_pairs = {}

    # Bonus 2: Output everything into an html file.
    html_output = "<html> <body> <table border = '1' > <tr> <th>Adjective</th> <th>Animal</th> <th>URL</th> </tr>"

    for row in table.find_all("tr"):
        cols = row.find_all("td")
        # After we got all columns, we extract the names (cols[0]) and the adjectives (cols[5])
        # Then, we add the adjectives to the dictionary "all_adj_name_pairs" as keys and the names as values
        if len(cols) > 0:
            Animal.name = cols[0].text
            # check if animal name in tmp directory. If so - no need to download image.
            if os.path.exists(Path(f"./tmp/{Animal.name}.jpg")):
                continue
            Animal.collateral_adjective = cols[5].text
            if Animal.collateral_adjective not in all_adj_name_pairs:
                all_adj_name_pairs[Animal.collateral_adjective] = []
            all_adj_name_pairs[Animal.collateral_adjective].append(Animal.name)
            url = cols[0].find('a').get('href')
            local_path = Animal.download_animal_image(url)
            html_output += f"<tr> <td>{Animal.collateral_adjective}</td> <td>{Animal.name}</td> <td><img src='{local_path}'></td> </tr>"
            with open("output.html", "w", encoding="utf-8") as local_html_file:
                html_output += "</body > </html>"
                html_output
                local_html_file.write(
                    html_output)
    return all_adj_name_pairs


if __name__ == "__main__":
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.submit(get_adj_name_pairs)
