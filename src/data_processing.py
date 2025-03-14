"""Collect the jsons of data and convert them into CSV files."""

import json
import csv
import pandas as pd
import os
from pathlib import Path

path = Path("research-data/data")


# list of lists; each list a line, do each line data from list in notebook
# passage, time between mouse moves, distance between mouse moves, quadrant(s)
#               ^out of total passage time?
# TODO: get all of my desired values, then determine how to csv it.
#passage_sorting = {}
for folder in path.iterdir():
    cvs_file = os.getcwd() + "\\processed\\" + str(folder)
    for file in folder.iterdir():
        if file.match("info*"):
            with file.open("r", encoding="utf-8") as i_file:
                # read json
                data = json.loads(i_file.read())

                # create dataframe
                df = pd.json_normalize(data)
                
                # save to csv
                df.to_csv(cvs_file + "_moves.csv", index=False, encoding="utf-8")
        elif file.match("states*"):
            states_sorting = {}
            with file.open("r", encoding="utf-8") as s_file:
                # read json
                data = json.loads(s_file.read())

                for i in range(len(data) - 1):
                    if isinstance(data[i], list) or isinstance(data[i], dict):
                        if len(data[i]) < 30:
                            states_sorting[i] = data[i]
                    else:
                        states_sorting[i] = data[i]
                # TODO: 4 and 5 are just copies of width and height, try/except for values > 5 and values < len(data)
                # that puts all the unlabeled vars in a list, compare to relevant values in listed passages to determine identity

                # TODO: also time math

                # create dataframe
                #df = pd.json_normalize(data)
                
                # save to csv
                #df.to_csv(cvs_file + "_all.csv", index=False, encoding="utf-8")
                print(states_sorting)
                #with open(cvs_file + "_states.csv", "w") as writeto:
                   #writer = csv.writer(writeto)
                   #for j in states_sorting:
                        #print(states_sorting[j])
                        #writer.writerow(j)
            break

        
