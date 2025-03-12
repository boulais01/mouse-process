"""Collect the jsons of data and convert them into CSV files."""

import json
import csv
import os
from pathlib import Path

path = Path("research-data/data")

# list of lists; each list a line, do each line data from list in notebook
# passage, time between mouse moves, distance between mouse moves, quadrant(s)
#               ^out of total passage time?
# TODO: get all of my desired values, then determine how to csv it.
passage_sorting = {}
for folder in path.iterdir():
    cvs_file = os.getcwd() + "\\processed\\" + str(folder) + ".csv"
    for file in folder.iterdir():
        if file.match("info*"):
            with open(file, "r") as i_file:
                data = json.load(i_file)
                for i in data:
                    # TODO: sort passages into order
                    print(i)
                    if i["passage"] not in passage_sorting.keys():
                        passage_sorting[i["passage"]] = [i]
                    else:
                        passage_sorting[i["passage"]].append(i)
                        print(passage_sorting[i["passage"]])
            #with open(cvs_file, "w") as writeto:
             #   writer = csv.writer(writeto)
              #  for j in passage_sorting:
                    #print(j)
               #     writer.writerow(j)
            # write to one csv
        elif file.match("states*"):
            with open(file, "r") as s_file:
                data = json.load(s_file)
            # write to another csv
            break

        
