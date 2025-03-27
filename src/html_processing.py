"""Parses the game's HTML file for the passage IDs and passage links to use in state assignments and choice processing."""

from bs4 import BeautifulSoup
from pathlib import Path

with open(Path("..\\comp-game\\comp specs collect.html"), "r", encoding="utf8") as html_path:
    soup = BeautifulSoup(html_path, features="lxml")