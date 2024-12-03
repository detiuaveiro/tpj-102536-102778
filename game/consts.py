import json
from pathlib import Path 

SETTINGS_FOLDER = "settings/"
DISPLAY_W, DISPLAY_H = 960, 640
SCALE = 2
MAP_FOLDER = "maps/6"
TILESIZE = 32
MENU_BOX_SIZE = (250, 50)
RESISTANCES = ["fire", "water"]  # player 1, player 2
TRESHOLD = 200


if Path(SETTINGS_FOLDER + "current.json").exists():
    with open(SETTINGS_FOLDER + "current.json") as f:
        SETTINGS = json.load(f)
else:
    with open(SETTINGS_FOLDER + "default.json") as f:
        SETTINGS = json.load(f)