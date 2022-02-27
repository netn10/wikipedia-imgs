import requests
from bs4 import BeautifulSoup
import os
import time
import re
import urllib
import urllib.request
from pathlib import Path


class Animal:
    def __init__(self, name, collateral_adjectives, url):
        self.name = name
        self.collateral_adjectives = collateral_adjectives

    def download_animal_image(url: str):
        # TODO: Implement this method for bonus
        local_path = ""
        return local_path

# This function is our "main" function. Call it to get all the adjectives-names.
# We also call Animal.download_animal_image(url) and output into html for the bonus.


def get_adj_name_pairs():
    r = requests.get("https://en.wikipedia.org/wiki/List_of_animal_names")
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find_all("table", class_="wikitable sortable")[1]

    all_adj_name_pairs = {}

    for row in table.find_all("tr"):
        cols = row.find_all("td")
        # After we got all columns, we extract the names (cols[0]) and the adjectives (cols[5])
        # Then, we add the adjectives to the dictionary "all_adj_name_pairs" as keys and the names as values
        if len(cols) > 0:
            Animal.name = cols[0].text
            Animal.collateral_adjective = cols[5].text
            if Animal.collateral_adjective not in all_adj_name_pairs:
                all_adj_name_pairs[Animal.collateral_adjective] = []
            all_adj_name_pairs[Animal.collateral_adjective].append(Animal.name)
    return all_adj_name_pairs

if __name__ == "__main__":
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.submit(get_adj_name_pairs)
