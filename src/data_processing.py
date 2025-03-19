"""Collect the jsons of data and convert them into CSV files."""

import json
import csv
import pandas as pd
import os
from pathlib import Path

path = Path("research-data/data")
var_defaults_fetch = {"quest": "fetch", "location": "", "plant_known": 0, "unicorn": 0, "armor": 1, "village": 0}
var_defaults_save = {"quest": "save", "location": "", "direction": "", "armor": True, "sword": True, "injured": 0, "trophies_drake": False, "tunnel": False, "nest_know": False, "around": False, "approach": "", "chick": "", "griffin_hp": 4, "observed": False, "ledge": False, "dawn": 0, "trapped": False}
var_defaults_bandit = {"quest": "bandit", "camp_known": False, "location": "", "direction": "", "armor": True, "sword": True, "injured": 0, "trophies_drake": False, "day": False, "spoken": False}
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
                        if len(data[i]) < 40:
                            states_sorting[i] = data[i]
                    else:
                        states_sorting[i] = data[i]
                # TODO: 4 and 5 are just copies of width and height, try/except for values > 5 and values < len(data)
                # that puts all the unlabeled vars in a list, compare to relevant values in listed passages to determine identity
                """
                {0: 1740597714729, 1: [{'passage': 'Disclaimer and Consent', 'time': 1740597728161}, 
                {'passage': 'The Beginning', 'time': 1740597744974}, {'passage': 'Save the Prince From the Griffon', 'time': 1740597752255},
                {'passage': 'The Mountain', 'time': 1740597755598}, {'passage': 'A Long Walk to Nothing', 'time': 1740597760895},
                {'passage': 'Make Camp', 'time': 1740597777972}, {'passage': 'Investigate the Rumbling', 'time': 1740597787006},
                {'passage': 'Go Back to Sleep', 'time': 1740597806135}, {'passage': 'Sneak Around the Drake', 'time': 1740597824246},
                {'passage': 'Continue Ascending the Mountain', 'time': 1740597835440}, {'passage': 'Enter the Tunnel', 'time': 1740597847323},
                {'passage': 'Explore the Clifftop', 'time': 1740597873715}, {'passage': 'Hold On!', 'time': 1740597898771},
                {'passage': "Attempt to Strike the Griffon's Underbelly", 'time': 1740597916429},
                {'passage': 'Keep Holding On', 'time': 1740597932174}, {'passage': 'Drop Down', 'time': 1740597950054},
                {'passage': 'Try to Flee With the Prince', 'time': 1740597968149}, {'passage': 'Escape!', 'time': 1740597991127},
                {'passage': 'The End', 'time': 0}], 2: 1740597714791, 4: 963, 5: 1854, 7: 'save', 8: 'mountain', 9: False, 10: True,
                11: 1, 12: False, 13: True, 14: False, 15: True, 16: 3, 17: True, 18: False}
                """
                """
                {0: 1740597714729, 1: [{'passage': 'Disclaimer and Consent', 'time': 1740597728161},
                {'passage': 'The Beginning', 'time': 1740597744974}, {'passage': 'Save the Prince From the Griffon', 'time': 1740597752255},
                {'passage': 'The Mountain', 'time': 1740597755598}, {'passage': 'A Long Walk to Nothing', 'time': 1740597760895},
                {'passage': 'Make Camp', 'time': 1740597777972}, {'passage': 'Investigate the Rumbling', 'time': 1740597787006},
                {'passage': 'Go Back to Sleep', 'time': 1740597806135}, {'passage': 'Sneak Around the Drake', 'time': 1740597824246},
                {'passage': 'Continue Ascending the Mountain', 'time': 1740597835440}, {'passage': 'Enter the Tunnel', 'time': 1740597847323},
                {'passage': 'Explore the Clifftop', 'time': 1740597873715}, {'passage': 'Hold On!', 'time': 1740597898771},
                {'passage': "Attempt to Strike the Griffon's Underbelly", 'time': 1740597916429}, {'passage': 'Keep Holding On', 'time': 1740597932174},
                {'passage': 'Drop Down', 'time': 1740597950054}, {'passage': 'Try to Flee With the Prince', 'time': 1740597968149},
                {'passage': 'Escape!', 'time': 1740597991127}, {'passage': 'The End', 'time': 0}], 2: 1740597714791,
                3: ['Disclaimer and Consent', [963, 1854], 'The Beginning', [963, 1854], 'Save the Prince From the Griffon', [963, 1854],
                'The Mountain', [963, 1854], 'A Long Walk to Nothing', [963, 1854], 'Make Camp', [963, 1854],
                'Investigate the Rumbling', [963, 1854], 'Go Back to Sleep', [963, 1854], 'Sneak Around the Drake', [963, 1854],
                'Continue Ascending the Mountain', [963, 1854], 'Enter the Tunnel', [963, 1854], 'Explore the Clifftop', [963, 1854],
                'Hold On!', [963, 1854], "Attempt to Strike the Griffon's Underbelly", [963, 1854], 'Keep Holding On', [963, 1854],
                'Drop Down', [963, 1854], 'Try to Flee With the Prince', [963, 1854], 'Escape!', [963, 1854], 'The End', [963, 1854]],
                4: 963, 5: 1854, 7: 'save', 8: 'mountain', 9: False, 10: True, 11: 1, 12: False, 13: True, 14: False, 15: True, 16: 3,
                17: True, 18: False}
                """
                time_dict = {}
                time_dict["total_ms"] = states_sorting[2] - states_sorting[0]
                last_time = states_sorting[0]
                for passage in states_sorting[1]:
                    time_dict[passage["passage"]] = passage["time"] - last_time
                    last_time = passage["time"]

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

        
