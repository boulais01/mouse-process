"""Use the csv files to run final processing calculations and collate data for analysis."""
# Specifically, calculates the time / distance for each movement in each passage
# Also displays each unique passage visited
import csv
import pandas as pd

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
        # order the list
        for passage in passage_sort.keys():
            passage_sort[passage] = sorted(passage_sort[passage], key=lambda x: x["time"])
        passage_moves = {}
        # calculate movement distances and times
        for current in passage_sort.keys():
            passage_moves[current + " Shifts"] = []
            for time in range(len(passage_sort[current]) - 1):
                passage_moves[current  + " Shifts"].append({"time_length": passage_sort[current][time + 1]["time"] - passage_sort[current][time]["time"], "x_distance": passage_sort[current][time + 1]["mouseX"] - passage_sort[current][time]["mouseX"], "y_distance": passage_sort[current][time + 1]["mouseY"] - passage_sort[current][time]["mouseY"]})

        if file.stem[5] == "_":
            csv_file = Path("processed/movements" + file.stem[4] + ".csv")
        else:
            csv_file = Path("processed/movements" + file.stem[4] + file.stem[5] + ".csv")

        with open(csv_file, mode='w', newline='') as file_write:
            writer = csv.DictWriter(file_write, fieldnames=passage_moves.keys())
            writer.writeheader()
            writer.writerow(passage_moves)

#print(passage_moves)
print(all_passages)

csv_file = Path("processed/movements.csv")

# create dataframe
df = pd.json_normalize(passage_moves)
                
# save to csv
df.to_csv(csv_file, index=False, encoding="utf-8")
        