"""Collecting all of the data parsed in other files into the final uses for analysis."""

import pandas as pd
import json
import os
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

def get_states_default() -> dict:
    """Get the states for each passage/path."""
    var_defaults = {}
    # iterate through the default path datasets
    for states in states_path.iterdir():
        with states.open("r", encoding="utf-8") as state:
            # read json
            data = json.loads(state.read())

            # TODO:
            # get each passage's states -- {"Passage Name": {"location": "forest", ...}, ...}
            # get each choice position -- {"Passage Name": {"Fetch the Majesty's Medicine": [(x,y), (x,y), (x,y), (x,y)], ...}}
            # combine -- {"Passage Name": {"States": {states}}, {"Choices"}: {choices}}

    return var_defaults

# TODO: create a main that runs the other three processers, then the functions defined above
