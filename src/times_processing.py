"""Use the csv files to run final processing calculations and collate data for analysis."""

import csv
from pathlib import Path

path = Path("processed/research-data/data")


for file in path.iterdir():
    if file.match("*_moves.csv"):
        passage_sort = {}
        reader = csv.DictReader(open(file))
        for row in reader:
            try:
                passage_sort[row["passage"]].append({"time": int(row["time"]), "mouseX": int(row["mouseX"]), "mouseY": int(row["mouseY"])})
            except KeyError:
                passage_sort[row["passage"]] = [{"time": int(row["time"]), "mouseX": int(row["mouseX"]), "mouseY": int(row["mouseY"])}]
        sorted_passages = {}
        for passage in passage_sort.keys():
            sorted_passages[passage] = sorted(passage_sort[passage], key=lambda x: x["time"])
        