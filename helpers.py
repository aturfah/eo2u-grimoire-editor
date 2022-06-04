from pathlib import Path
from pprint import pprint

def load_skillname_hex_maps():
    data_dir = Path("data/")
    ## Read in the files
    skill_to_hex_data = data_dir.joinpath("skill_to_hex.txt").read_text().splitlines()
    player_skills = data_dir.joinpath("player_skills.txt").read_text().splitlines()
    enemy_grimoire_skills = data_dir.joinpath("enemy_grimoire_skills.txt").read_text().splitlines()

    ## Prepare the dictionaries
    name_to_hex = {}
    hex_to_name = {}
    for line in skill_to_hex_data:
        name, _, hex_id = line.split("\t")
        name = name.strip()
        hex_id = hex_id.strip()

        ## 0DB => DB00 so it actually works
        hex_id = "0" + hex_id[1:] + hex_id[0]

        if name in player_skills or name in enemy_grimoire_skills:
            name_to_hex[name] = hex_id
            hex_to_name[hex_id] = name

    return name_to_hex, hex_to_name
