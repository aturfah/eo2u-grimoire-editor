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


GRIMOIRE_START = int(20192 / 2)
GRIMOIRE_LENGTH = int(100 / 2)

def parse_save_file(fname_path:Path):
    if not isinstance(fname_path, Path):
        fname_path = Path(fname_path)

    if fname_path.is_dir():
        fname_path = fname_path.joinpath("mo2r00_game.sav")

    file_bytes = fname_path.read_bytes()
    file_hex = file_bytes.hex(" ").split(" ")
    num_bytes = len(file_hex)

    ## Locate Natural Instinct Lv9 Grimoire
    # hex_str = "".join(file_hex)
    # match_idx = hex_str.index("0000820109")
    # print(match_idx)
    # grimoire_str = hex_str[(match_idx-88):(match_idx+12)]
    # print(grimoire_str)
    # print(len(grimoire_str))
    # print()
    # abs_start = match_idx - 88
    # print(abs_start)
    # print(hex_str[abs_start:(abs_start+100)])

    # raise RuntimeError("AAAHHH")

    if GRIMOIRE_START > num_bytes:
        raise RuntimeError("Invalid File")

    grimoire_info = []
    grimoire_data = []
    counter = 0
    for idx in range(GRIMOIRE_START, num_bytes):
        grimoire_data.append(file_hex[idx])
        if len(grimoire_data) == GRIMOIRE_LENGTH:
            print("Grimoire #{}".format(counter+1))
            print(" ".join(grimoire_data))
            # grimoire_data = "00	02	04	01	07	00	82	71	82	81	82	91	82	95	82	8E	82	81	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	48	00	0A	00	89	00	0A	00	B1	01	0A	00	04	02	0A	00	02	00	0A	00	03	00	0A	00	41	00	0A	00".lower().split("\t")
            # g_info = parse_grimoire(grimoire_data)
            # if g_info:
            #     grimoire_info.append(g_info)
            # # break
            counter += 1
            grimoire_data = []

        if counter == 400:
            ## Max of 400 Grimoires
            break

    return grimoire_info, "".join(file_hex)

if __name__ == "__main__":
    parse_save_file("backups/base/mo2r00_game.sav")