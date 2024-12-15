import json
from pathlib import Path 

SETTINGS_FOLDER = "settings/"
ASSETS_FOLDER = "assets/"
MAP_FOLDER = "maps"
MAP_FILE = "map.csv"
MAP_METADATA = "map.json"

DISPLAY_W, DISPLAY_H = 960, 640
SCALE = 2
TILESIZE = 32
MENU_BOX_SIZE = (250, 50)
TRESHOLD = 100
ANIMATION_COOLDOWN = 100
DEATH_FRAMES = 50

GRAVITY = 0.4
HORIZONTAL_SPEED = 1
VERTICAL_SPEED = 10

PLAYERS = ['Fire Monster', 'Water Monster']    # player 1, player 2
RESISTANCES = ["lava", "water"]                # player 1, player 2

SOUND_COOLDOWN = 0.1
SOUNDS = {
    "jump": "assets/Sounds/jump.mp3",
    "die": "assets/Sounds/die.mp3",
    "transition": "assets/Sounds/transition.mp3",
}


if Path(SETTINGS_FOLDER + "current.json").exists():
    with open(SETTINGS_FOLDER + "current.json") as f:
        SETTINGS = json.load(f)
else:
    with open(SETTINGS_FOLDER + "default.json") as f:
        SETTINGS = json.load(f)