"""Parses the game's HTML file for the passage IDs and passage links to use in state assignments and choice processing."""

import pandas as pd
import re

from bs4 import BeautifulSoup
from pathlib import Path

all_passages = []

def check_choice(choices: dict, choice: list, choice_count: int) -> tuple:
    """Check if a choice has already been included in the dict, and add it if it hasn't."""
    for chose in choices:
        if choices[chose] == choice:
            return choices, choice_count
    choices[choice_count] = choice
    choice_count += 1
    return choices, choice_count

def check_ifs(start: int, end: int, text: str) -> tuple:
    """Check if the choices present varies based on other factors."""
    has_if = False
    choice_sets = []
    # iterate through text
    if text.find("<<else>>", start) != -1 or text.find("<<if", start) != -1:
        has_if = True
        # else indicates more than 2 sets
        if "<<else>>" in text[start:end]:
            start_set = start
            while "[[" in text[start_set:] and start_set < end and start_set >= start:
                if text.find("<<", start_set) != -1:
                    #print(text[start_set:text.find("<<", start_set)])
                    if text.count("[[", start_set, text.find("<<", start_set)) != 0:
                        choice_sets.append(text.count("[[", start_set, text.find("<<", start_set)))
                start_set = text.find(">>", start_set) + 1
            return (has_if, choice_sets)
        else:
            return (has_if, [2, 3])
    return (has_if, choice_sets)
                            

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
                choice: str = text[text.find("[[", i, end):text.find("]]", i, end)]
                if choice != "":
                    choice = choice.strip("[[]]\n.<</if>")
                    if "]]" in choice:
                        choice = choice[0:choice.find("]]")]
                    if "|" in choice:
                        has_var = choice.split("|")
                        if "]" in has_var[1]:
                            var_starts = has_var[1].find("$")
                            var_name = has_var[1][(var_starts+1):has_var[1].find(" ", var_starts)]
                            var_val = has_var[1][(has_var[1].find("to", var_starts) + 2):]
                            choices, choice_count = check_choice(choices, [has_var[0].strip("[[]]\n."), has_var[1][0:var_starts].strip("[[]]\n."), {var_name:var_val}], choice_count)
                        else:
                            choices, choice_count = check_choice(choices, [has_var[0].strip("[[]]\n."), has_var[1].strip("[[]]\n.")], choice_count)
                    else:
                        if "]" in choice:
                            var_starts = choice.find("$")
                            var_name = choice[(var_starts+1):choice.find(" ", var_starts)]
                            var_val = choice[(choice.find("to", var_starts) + 2):]
                            choices, choice_count = check_choice(choices, [choice[0:var_starts].strip("[[]]\n."), "", {var_name:var_val}], choice_count)
                        else:
                            choices, choice_count = check_choice(choices, [choice.strip("[[]]\n."), "", {}], choice_count)
        passage_dict["choices"] = choices
        if start != -1 and end != -1:
            if_ifs = check_ifs(start, end, text)
            passage_dict["if"] = if_ifs[0]
            if if_ifs[1] == []:
                passage_dict["choice_sets"] = [choice_count]
            else:
                passage_dict["choice_sets"] = if_ifs[1]
        #print(choices)
        all_passages.append(passage_dict)
    
# print(all_passages)

csv_file = Path("processed/passages.csv")

# create dataframe
df = pd.json_normalize(all_passages)
                
# save to csv
df.to_csv(csv_file, index=False, encoding="utf-8")
