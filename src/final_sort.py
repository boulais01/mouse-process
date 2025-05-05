"""Collecting all of the data parsed in other files into the final uses for analysis."""

import json
import ast  
import csv

from pathlib import Path

data_path = Path("research-data/data")
states_path = Path("research-data/path_states")
processed_path = Path("processed/research-data/data")
passages_path = Path("processed")

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

def get_choices_pos() -> dict:
    """Get a dictionary of choices in each passage and their positions."""
    passage_press = {}
    passage_links = {}
    choices_dict = {}

    # iterate through the default path datasets
    for states in states_path.iterdir():
        with states.open("r", encoding="utf-8") as state:
            # read json
            data = json.loads(state.read())

            rows = data[0]
            # dict_keys(['passage', 'variables'])
            #print(row["variables"].keys())
            #dict_keys(['playtime', 'history', 'started', 'tracking', 'press_count', 'passage_count', 'passage_sets', 'passage_links', 'mouse_movements', 'quest', 'location', 'armor', 'sword', 'injured', 'trophies_drake', 'tunnel', 'nest_know', 'direction', 'trapped'])
            for row in rows:
                for key in row["variables"].keys():
                    # get num of choices in each passage
                    if key == "passage_links":
                        passage_links[row["passage"]] = row["variables"][key]
                    # get choice positions
                    elif key == "mouse_movements" and row == rows[len(rows) - 1]:
                        for press in row["variables"][key]:
                            if press["passage"] not in passage_press.keys():
                                passage_press[press["passage"]] = []
                            passage_press[press["passage"]].append((press["press"], press["mouseX"], press["mouseY"]))
    passage_press = check_choice_pos(passage_press)
    
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
    return {"presses": passage_press, "links": passage_links, "choice_sets": choices_dict}


def get_passage_choice(passage: str, choices_dict: dict) -> dict:
    """Get the choice positions of one passage based on the num of choices."""

    if choices_dict["choice_sets"][passage][1] == "True":
        print(choices_dict["links"][passage], type(print(choices_dict["links"][passage])))
    #if x1 > x2 and y4 < y3:
    #elif x1 > x2 and y4 > y3:


def get_states_default():
    """Get the states for each passage/path."""
    consts = ['playtime', 'history', 'started', 'tracking', 'press_count', 'passage_count', 'passage_sets', 'passage_links', 'mouse_movements']
    states_dict = {}
    states_by_quest = {}
    passage_states = {}
    # iterate through the default path datasets
    for states in states_path.iterdir():
        with states.open("r", encoding="utf-8") as state:
            # read json
            data = json.loads(state.read())

            rows = data[0]
            # dict_keys(['passage', 'variables'])
            #print(row["variables"].keys())
            #dict_keys(['playtime', 'history', 'started', 'tracking', 'press_count', 'passage_count', 'passage_sets', 'passage_links', 'mouse_movements', 'quest', 'location', 'armor', 'sword', 'injured', 'trophies_drake', 'tunnel', 'nest_know', 'direction', 'trapped'])
            for row in rows:
                skip = False
                name = ""
                # get states
                if row["passage"] not in states_dict.keys():
                    states_dict[row["passage"]] = {}
                try:
                    name = row["variables"]["quest"] + "_" + row["variables"]["location"]
                    if name not in states_by_quest.keys():
                        states_by_quest[name] = {}
                except KeyError:
                    skip = True
                for key in row["variables"].keys():
                    if key not in consts:
                        if key not in states_dict[row["passage"]].keys():
                            states_dict[row["passage"]][key] = row["variables"][key]
                        if not skip:
                            if key not in states_by_quest[name].keys():
                                states_by_quest[name][key] = row["variables"][key]
                if not skip:
                    if row["passage"] not in passage_states.keys():
                        passage_states[row["passage"]] = {name: states_by_quest[name]}
                    else:
                        passage_states[row["passage"]][name] = states_by_quest[name]
    return states_dict, states_by_quest, passage_states

"""
final processing make the data points all in one file, formatted
| Player_Num | Passage | Move_time | Move_X | Move_Y |
then another file for states,
| Player_Num | Passage | All States... |
"""
# player num from the file count

# get each passage's states -- {"Passage Name": {"location": "forest", ...}, ...}
# get each choice position -- {"Passage Name": {"Fetch the Majesty's Medicine": [(x,y), (x,y), (x,y), (x,y)], ...}}
# combine -- {"Passage Name": {"States": {states}}, {"Choices"}: {choices}}

# defaults for each passage, as "passage_name" : {"variable": "value"}
var_defaults, quest_defaults, synthesis = get_states_default()
#print(quest_defaults)
#print(var_defaults)
#print(synthesis)

# choices present in each passage in the base states and their positions, as {"presses": {"passage_name": [(x,y),..]}, "links": {"passage_name": [link_tracking_info]}}
choice_info = get_choices_pos()

# for loop for each movements, get player num then by passage basis for other factors
# get_passage_choice(passage: str, states: dict) for passing in a passage name and states and getting choice pos dict
"""
    final processing make the data points all in one file, formatted
    | Player_Num | Passage | Move_time | Move_X | Move_Y |
    then another file for states,
    | Player_Num | Passage | All States... |
"""
# build csv files
all_states = []
states_fieldnames = ["Player_Num"]
all_moves = []
by_passage = {}
for i in range(1, 14):
    passages = []
    if i != 4:
        #move_file = Path(passages_path, "movements" + str(i) + ".csv")
        move_file = Path(processed_path, "data" + str(i) + "_moves.csv")
        with move_file.open("r", encoding="utf-8") as moves:
            #get_passage_choice()
            for row in moves:
                row = row.split(",")
                if row[0] != "Disclaimer and Consent" and row[0] != "The End" and row[0] != "passage":
                    move = {"Player_Num": i, "Passage": row[0], "Time_ms": row[1], "MouseX": int(row[2]), "MouseY": int(row[3])}
                    if row[0] not in passages:
                        passages.append(row[0])
                    all_moves.append(move)
        states_file = Path(processed_path, "data" + str(i) + "_states.csv")
        state = {"Player_Num": i}
        with states_file.open("r", encoding="utf-8") as states:
            rows = [row.split(",") for row in states]
            index = -1
            for val in range(len(rows[0])):
                if "states" in rows[0][val]:
                    index = val
                    break
            states_list = rows[1][index:]
            base_states = {}
            base_states_2 = {}
            for passage in passages:
                skip = False
                try:
                    if states_list[1] in ["mountain", "forest"]:
                        name = states_list[0] + "_" + states_list[1]
                    else:
                        name = states_list[0] + "_" + states_list[2]
                except KeyError:
                    skip = True
                #for key in var_defaults[passage].keys():
                #    if key not in base_states.keys():
                #        base_states[key] = var_defaults[passage][key]
                if not skip:
                    for key_2 in quest_defaults[name].keys():
                        if key_2 not in base_states_2.keys():
                            base_states_2[key_2] = quest_defaults[name][key_2]
                if passage in synthesis.keys() and not skip:
                    for key in quest_defaults[name].keys():
                        if key not in base_states.keys():
                            #print(passage, key, name, synthesis[passage])
                            base_states[key] = synthesis[passage][name][key]
            count = 0
            for key in base_states.keys():
                state[key] = states_list[count].strip("\n")
                if key not in states_fieldnames:
                    states_fieldnames.append(key)
                count += 1
                if count >= len(states_list):
                    break
        all_states.append(state)  

move_num = 0
for move in all_moves:
    if move["Passage"] not in by_passage.keys():
        by_passage[move["Passage"]] = []
    by_passage[move["Passage"]].append({"Player_Num": move["Player_Num"], "Move_Label": str(move["Player_Num"]) + "." + str(move_num), "Time_ms": move["Time_ms"], "MouseX": move["MouseX"], "MouseY": move["MouseY"]})
    move_num += 1

base_passage_path = Path(passages_path, "passages")
players_in_pass = {}
for key in by_passage.keys():
    player_nums = {record["Player_Num"] for record in by_passage[key] if record["Player_Num"] != ""}
    players_in_pass[key] = player_nums
    if len(player_nums) > 1:
        #print(f"Writing passage {key} with {player_nums}")
        with open(Path(base_passage_path, str(key) + ".csv"), mode="w", newline="") as passage_file:
            writer = csv.DictWriter(passage_file, fieldnames=["Player_Num", "Move_Label", "Time_ms", "MouseX", "MouseY"])
            writer.writeheader()
            writer.writerows(by_passage[key])
         
all_moves_path = Path(passages_path, "final_moves.csv")
all_states_path = Path(passages_path, "final_states.csv")

with open(all_moves_path, mode='w', newline='') as file_write:
    writer = csv.DictWriter(file_write, fieldnames=["Player_Num", "Passage", "Time_ms", "MouseX", "MouseY"])
    writer.writeheader()
    writer.writerows(all_moves)

with open(all_states_path, mode='w', newline='') as file_write:
    writer = csv.DictWriter(file_write, fieldnames=states_fieldnames)
    writer.writeheader()
    writer.writerows(all_states)
