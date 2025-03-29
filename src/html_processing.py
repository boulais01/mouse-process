"""Parses the game's HTML file for the passage IDs and passage links to use in state assignments and choice processing."""

import pandas as pd

from bs4 import BeautifulSoup
from pathlib import Path

all_passages = []

with open(Path("..\\comp-game\\comp specs collect.html"), "r", encoding="utf8") as html_path:
    # extract file
    soup = BeautifulSoup(html_path, features="lxml")

    # get only the passage information
    passage_data = soup.find_all("tw-passagedata")
    #print(passage_data)
    # iterate through the passages to get each name, id, and choice list
    for passage in passage_data:
        passage_dict = {}
        passage_dict["name"] = passage["name"]
        passage_dict["id"] = passage["pid"]
        text = passage.get_text()
        # go through text to get choice names (and number them)
        start = text.find("[[")
        end = text.rfind("]]")
        choices = {}
        choice_count = 0
        # make sure there are choices
        if start != -1 and end != -1:
            for i in range(start, end):
                choice = text[text.find("[[", i, end) :text.find("]]", i, end)]
                if choice != "":
                    choice = choice.strip("[[]]")
                    if "|" in choice:
                        has_var = choice.split("|")
                        choices[choice_count] = [has_var[0], has_var[1]]
                    else:
                        choices[choice_count] = [choice, ""]
                    choice_count += 1
        passage_dict["choices"] = choices
        all_passages.append(passage_dict)
    
# print(all_passages)

csv_file = Path("../processed/passages.csv")

# create dataframe
df = pd.json_normalize(all_passages)
                
# save to csv
df.to_csv(csv_file, index=False, encoding="utf-8")
