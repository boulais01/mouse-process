"""Collecting all of the data parsed in other files into the final uses for analysis."""

import json
import ast  
import csv

from pathlib import Path

data_path = Path("research-data/data")
states_path = Path("research-data/path_states")
processed_path = Path("processed/research-data/data")

"""
final processing make the data points all in one file, formatted
| Player_Num | Passage | Move_time | |Move_X | Move_Y |
then another file for states,
| Player_Num | Passage | All States... |
"""
# player num from the file count

def check_choice_pos(passage_press: dict) -> dict:
    """Sort through the click positions to ensure no repeats."""
    uniquified_passage = {}
    prevX = -1
    prevY = -1
    for passage in passage_press.keys():
        uniquified_passage[passage] = []
        for pos in passage_press[passage]:
            if prevX != -1 and prevY != -1:
                if prevX != pos[1] or prevY != pos[2]:
                    uniquified_passage[passage].append(pos)
            prevX = pos[1]
            prevY = pos[2]
    return uniquified_passage

def get_states_default() -> dict:
    """Get the states for each passage/path."""
    consts = ['playtime', 'history', 'started', 'tracking', 'press_count', 'passage_count', 'passage_sets', 'passage_links', 'mouse_movements']
    var_defaults = {}
    states_dict = {}
    passage_press = {}
    choices_dict = {}
    choice_points = {}
    # iterate through the default path datasets
    for states in states_path.iterdir():
        with states.open("r", encoding="utf-8") as state:
            # read json
            data = json.loads(state.read())

            # TODO:
            # get each passage's states -- {"Passage Name": {"location": "forest", ...}, ...}
            # get each choice position -- {"Passage Name": {"Fetch the Majesty's Medicine": [(x,y), (x,y), (x,y), (x,y)], ...}}
            # combine -- {"Passage Name": {"States": {states}}, {"Choices"}: {choices}}
            rows = data[0]
            # dict_keys(['passage', 'variables'])
            #print(row["variables"].keys())
            #dict_keys(['playtime', 'history', 'started', 'tracking', 'press_count', 'passage_count', 'passage_sets', 'passage_links', 'mouse_movements', 'quest', 'location', 'armor', 'sword', 'injured', 'trophies_drake', 'tunnel', 'nest_know', 'direction', 'trapped'])
            for row in rows:
                # get states
                if row["passage"] not in states_dict.keys():
                    states_dict[row["passage"]] = {}
                for key in row["variables"].keys():
                    if key not in consts:
                        if key not in states_dict[row["passage"]].keys():
                            states_dict[row["passage"]][key] = row["variables"][key]

                    # get choice positions
                    if key == "mouse_movements" and row == rows[len(rows) - 1]:
                        for press in row["variables"][key]:
                            if press["passage"] not in passage_press.keys():
                                passage_press[press["passage"]] = []
                            passage_press[press["passage"]].append((press["press"], press["mouseX"], press["mouseY"]))
    # get choice from the passages.csv file
    reader = csv.DictReader(open(Path("processed/passages.csv")))

    for row in reader:
        choice_list = []
        for i in range(len(row) - 2):
            try:
                if row["choices." + str(i)] != "" and row["choices." + str(i)] != " ":
                    unstring_choice = ast.literal_eval(row["choices." + str(i)])
                    choice_list.append(unstring_choice[0])
            except KeyError:
                continue
        choices_dict[row["name"]] = (choice_list, row["if"], row["choice_sets"])

    unique_pass_press = check_choice_pos(passage_press)
    for key in choices_dict.keys():
        if key in unique_pass_press.keys():
            #print(choices_dict[key], unique_pass_press[key])
            if choices_dict[key][1] == "True":
                print(choices_dict[key][0], choices_dict[key][2])
    #if x1 > x2 and y4 < y3:
    #elif x1 > x2 and y4 > y3:
    return var_defaults

# TODO: create a main that runs the other three processers, then the functions defined above

get_states_default()