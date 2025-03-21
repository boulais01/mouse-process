"""Use the csv files to run final processing calculations and collate data for analysis."""

import csv
from pathlib import Path

path = Path("processed/research-data/data")
all_passages = []

for file in path.iterdir():
    # locate the files with the mouse movements
    if file.match("*_moves.csv"):
        passage_sort = {}
        reader = csv.DictReader(open(file))
        # iterate through each instance of movement
        for row in reader:
            # sort the movement into a list for each passage
            if row["passage"] not in all_passages:
                all_passages.append(row["passage"])
            try:
                passage_sort[row["passage"]].append({"time": int(row["time"]), "mouseX": int(row["mouseX"]), "mouseY": int(row["mouseY"])})
            except KeyError:
                passage_sort[row["passage"]] = [{"time": int(row["time"]), "mouseX": int(row["mouseX"]), "mouseY": int(row["mouseY"])}]
        sorted_passages = {}
        # order the list
        for passage in passage_sort.keys():
            sorted_passages[passage] = sorted(passage_sort[passage], key=lambda x: x["time"])
        
print(all_passages)
        