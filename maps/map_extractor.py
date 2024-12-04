import csv
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', type=str, help ='Path to map bytecode')
args = parser.parse_args()

mechanism_mapping = {
    123: ("green", "trigger"),
    125: ("green", "barrier"),
    120: ("purple", "trigger"),
    122: ("purple", "barrier")
}


def read_csv():
    map_details = []
    with open(args.m, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            map_details.append(row)
    return map_details


def extract_mechanisms():
    mechanisms = {}
    map_details = read_csv()
    for y, row in enumerate(map_details):
        for x, tile in enumerate(row):
            tile_idx = int(tile)
            process_tile(tile_idx, x, y, mechanisms)
    return mechanisms


def process_tile(tile_idx, x, y, mechanisms):
    if tile_idx in mechanism_mapping:
        mechanism_name, mechanism_type = mechanism_mapping[tile_idx]
        if mechanism_name not in mechanisms:
            mechanisms[mechanism_name] = {
                "triggers": [],
                "barriers": []
            }

        data = {
            "tile": tile_idx,
            "x": x,
            "y": y
        }
        mechanisms[mechanism_name][f"{mechanism_type}s"].append(data)


def remove_mechanisms():
    new_map = []
    map_details = read_csv()
    for y, row in enumerate(map_details):
        new_row = []
        for x, tile in enumerate(row):
            tile_idx = int(tile)
            if tile_idx not in mechanism_mapping:
                new_row.append(tile)
            else:
                new_row.append(-1)
        new_map.append(new_row)
    return new_map


def extract_players_pos():
    players = {}
    map_details = read_csv()
    for y, row in enumerate(map_details):
        for x, tile in enumerate(row):
            tile_idx = int(tile)
            if tile_idx == 0 or tile_idx == 1:
                players[f"player_{tile_idx}"] = {
                    "x": x,
                    "y": y
                }
    return players


if __name__ == "__main__":

    # Extract Mechanisms
    mechanisms = extract_mechanisms()
    mechanisms = list(mechanisms.values())
    map_name = args.m.split('/')[-1].split('.')[0]
    with open(f"{map_name}_mechanisms.json", 'w') as f:
        json.dump(mechanisms, f, indent=4)

    new_map = remove_mechanisms()
    with open(f"{map_name}_no_mechanisms.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerows(new_map)

    # Extract Players Initial Position
    players = extract_players_pos()
    with open(f"{map_name}_players.json", 'w') as f:
        json.dump(players, f, indent=4)