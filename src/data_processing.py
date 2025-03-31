"""Collect the jsons of data and convert them into CSV files."""
# Specifically: sorts for use in times_processing and establishes overall times

import json
import pandas as pd
import os

from pathlib import Path

path = Path("research-data/data")
#var_defaults = {}

for folder in path.iterdir():
    csv_file = os.getcwd() + "\\processed\\" + str(folder)
    for file in folder.iterdir():
        if file.match("info*"):
            with file.open("r", encoding="utf-8") as i_file:
                # read json
                data = json.loads(i_file.read())

                # create dataframe
                df = pd.json_normalize(data)
                
                # save to csv
                df.to_csv(csv_file + "_moves.csv", index=False, encoding="utf-8")
        elif file.match("states*"):
            states_sorting = {}
            with file.open("r", encoding="utf-8") as s_file:
                # read json
                data = json.loads(s_file.read())

                for i in range(len(data) - 1):
                    if isinstance(data[i], list) or isinstance(data[i], dict):
                        states_sorting[i] = data[i]
                    else:
                        states_sorting[i] = data[i]
                time_dict = {}
                time_dict["total_ms"] = states_sorting[2] - states_sorting[0]
                last_time = states_sorting[0]
                for passage in states_sorting[1]:
                    if passage["passage"] != "The End":
                        time_dict[passage["passage"]] = passage["time"] - last_time
                        last_time = passage["time"]
                
                #run_vars = var_defaults[states_sorting[7]]
                sort_count = 8
                """
                # make a default dict for mountain versus forest save
                for key in run_vars.keys():
                    run_vars[key] = states_sorting[sort_count]
                    sort_count += 1
                    if sort_count >= len(states_sorting):
                        break"
                """
                # states moved to final processing

                states = {"times": time_dict, "scene_area": states_sorting[4] * states_sorting[5]}
                # create dataframe
                df = pd.json_normalize(states)
                
                # save to csv
                df.to_csv(csv_file + "_states.csv", index=False, encoding="utf-8")
            break     
