import json
from pathlib import Path 

SETTINGS_FOLDER = "settings/"

if Path(SETTINGS_FOLDER + "current.json").exists():
    with open(SETTINGS_FOLDER + "current.json") as f:
        SETTINGS = json.load(f)
else:
    with open(SETTINGS_FOLDER + "default.json") as f:
        SETTINGS = json.load(f)