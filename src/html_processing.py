"""Parses the game's HTML file for the passage IDs and passage links to use in state assignments and choice processing."""

from bs4 import BeautifulSoup
from pathlib import Path

all_passages = []

with open(Path("..\\comp-game\\comp specs collect.html"), "r", encoding="utf8") as html_path:
    soup = BeautifulSoup(html_path, features="lxml")

    # figure out how to extract passage data of listed passages from times_processing?
    # get passage ID while doing that
    # get links info from parsing passage text for the content between [[]]
    passage_data = soup.find_all("tw-passagedata")
    #print(passage_data)
    for passage in passage_data:
        passage_dict = {}
        passage_dict["name"] = passage["name"]
        passage_dict["id"] = passage["pid"]
        text = passage.get_text()
        # TODO: go through text with str find and indexing to get choice names (and number them)
        start = text.find("[[")
        end = text.rfind("]]")
        choices = []
        #if start != -1 and end != -1:
            #for i in range(start, end):
                
        passage_dict["choices"] = choices
        all_passages.append(passage_dict)
    