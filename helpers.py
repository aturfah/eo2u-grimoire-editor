from pathlib import Path
from pprint import pprint
import unicodedata

from unicode_to_sjis import UNICODE_TO_SJIS
from sjis_to_unicode import SJIS_TO_UNICODE

def load_skillname_hex_maps():
    data_dir = Path("data/")
    ## Read in the files
    skill_to_hex_data = data_dir.joinpath("skill_to_hex.txt").read_text().splitlines()
    player_skills = data_dir.joinpath("player_skills.txt").read_text().splitlines()
    enemy_grimoire_skills = data_dir.joinpath("enemy_grimoire_skills.txt").read_text().splitlines()

    ## Clean up spaces
    player_skills = [x.strip() for x in player_skills]
    enemy_grimoire_skills = [x.strip() for x in enemy_grimoire_skills]

    ## Prepare the dictionaries
    name_to_hex = {}
    hex_to_name = {}
    for line in skill_to_hex_data:
        hex_id, name = line.split("|")
        name = name.replace("(Passive)", "").strip()
        hex_id = hex_id.strip().replace(" ", "")

        if name == "Comet Drop":
            print("Hi")
            print(name in player_skills)
            print(name in enemy_grimoire_skills)
            # raise RuntimeError("AAAHHH")

        if (name in player_skills) or (name in enemy_grimoire_skills):
            name_to_hex[name] = hex_id
            hex_to_name[hex_id] = name

    return name_to_hex, hex_to_name

NAME_TO_HEX, HEX_TO_NAME = load_skillname_hex_maps()

GRIMOIRE_START = int(20192 / 2)
GRIMOIRE_LENGTH = int(100 / 2)

GRIMOIRE_ORIGIN_MAP = {
    "00": "Created/Etrian",
    "02": "Traded (retired Member)",
    "04": "Created",
    "08": "Traded (#1)", ## TODO: Verify
    "30": "Traded (#2)", ## TODO: Verify
    "40": "Traded (in-game)",
    "44": "Traded (#3)", ## TODO: Verify
    "48": "?",
    "80": "Traded (Guild Card)"
}

def parse_grimoire_origin(grimoire_data):
    """Bytes 1-2 define origin"""
    origin_bytes = grimoire_data[0:2]
    print("Origin Bytes:", origin_bytes)
    print("\tOrigin: {}".format(GRIMOIRE_ORIGIN_MAP[origin_bytes[0]]))

GRIMOIRE_CLASS_MAP = {
    "00": "Landsknecht",
    "01": "Survivalist",
    "02": "Protector",
    "03": "Dark Hunter",
    "04": "Medic",
    "05": "Alchemist",
    "06": "??? #1",
    "07": "Ronin ",
    "08": "??? #2",
    "09": "Gunner ",
    "0A": "War Magus",
    "0B": "Beast",
    "0C": "Sovereign",
    "0D": "Highlander",
    "0E": "Fafnir"
}

def parse_grimoire_class(grimoire_data):
    """Bytes 3-4 determine originating class"""
    class_bytes = grimoire_data[2:4]
    print("Class Bytes:", class_bytes)
    print("\tClass: {}".format(GRIMOIRE_CLASS_MAP[class_bytes[0]]))


def parse_grimoire_origin_details(grimoire_data):
    """Bytes 5-6 determine things like 'Overhead Ronin'"""
    ## TODO: Fill me in
    orig_details_bytes = grimoire_data[4:6]
    print("Origin Details Bytes:", orig_details_bytes)


def parse_grimoire_mystery_bytes(grimoire_data):
    """Bytes 7-8 are Mystery Byte"""
    mystery_bytes = grimoire_data[6:8]
    print("Mystery Bytes:", mystery_bytes)


def ascii_to_hex(str_in, padded_length=72):
    output_arr = []
    for char in str_in:
        ## Convert to full width characters
        if char != " " and ord(char) != 8140:
            output_arr.append(0xFEE0 + ord(char))
        else:
            output_arr.append(0x3000) ## Full Width Space?

    output = ""
    for idx in range(len(output_arr)):
        try: 
            output += UNICODE_TO_SJIS[output_arr[idx]]
        except Exception:
            raise RuntimeError("Invalid character in name: '{}'".format(str_in[idx]))

    output = output.replace(" ", "")

    while len(output) < padded_length:
        output += "0"

    if len(output) > padded_length:
        raise RuntimeError("Name too Long")

    return output

def parse_name_of_trader(grimoire_data):
    """Bytes 9-44 are the Trader Name"""
    name_bytes = grimoire_data[8:44]
    print("Name Bytes:", "".join(name_bytes))

    gg_unicode = []
    cur_char = []
    for h_number in [x.upper() for x in name_bytes]:
        if not cur_char and h_number in SJIS_TO_UNICODE.keys():
            gg_unicode.append(SJIS_TO_UNICODE[h_number])
            if gg_unicode[-1] != 0:
                gg_unicode[-1] = chr(gg_unicode[-1])
            continue

        cur_char.append(h_number)
        if len(cur_char) == 2:
            char_hex = "".join(cur_char)
            char_unic = SJIS_TO_UNICODE[char_hex]
            gg_unicode.append(chr(char_unic))
            cur_char = []

    ## Entirely 0; unknown origin
    gg_unicode = [x for x in gg_unicode if x != 0]
    unknown_origin = False
    if not gg_unicode:
        unknown_origin = True
        gg_unicode = []

    gg_unicode = "".join(gg_unicode)
    ## Names correspond to full-width characters, need half width
    gg_unicode = unicodedata.normalize("NFKC", gg_unicode)

    print("\tName:", gg_unicode)

    return gg_unicode, "".join(name_bytes), unknown_origin


GRIMOIRE_BONUS_TYPE_MAP= {
    "0000": "None",
    "7C02": "Cut Up",
    "7D02": "Stab Up",
    "7E02": "Bash Up",
    "7F02": "Fire Up",
    "8002": "Ice Up",
    "8102": "Volt-Up",
    "8202": "Ail inf up",
    "8302": "Bind inf up",
    "8402": "Grimoire Chance Up",
    "8502": "Rare enemy",
    "8602": "Ail Rec Up",
    "8702": "Bind rec Up",
    "8802": "Drop amount up",
    "8902": "Victory HP",
    "8A02": "Victory TP",
    "8B02": "Auto-Heal",
    "8C02": "Self-Heal Amp",
    "8D02": "Force Up",
    "8E02": "Grimoire Skill Level Up",
    "8F02": "Turn TP Recover",
    "9002": "TP Cost Recovery"
}


def parse_addon_bonus_type(grimoire_data):
    """Bytes 45-46 are the grimoire bonus type"""
    bonus_type_bytes = grimoire_data[44:46]
    print("Bonus Type Bytes:", bonus_type_bytes)
    print("\tBonus Type:", GRIMOIRE_BONUS_TYPE_MAP["".join(bonus_type_bytes)])


def parse_grimoire_skill(grimoire_data):
    """Bytes 47-48 are the grimoire skill ID"""
    skill_id_bytes = grimoire_data[46:48]
    print("Grimoire Skill Bytes:", skill_id_bytes)
    print("\tGrimoire Skill:", HEX_TO_NAME["".join(skill_id_bytes)])


def parse_grimoire_skill_level(grimoire_data):
    """Bytes 49 are the grimoire skill level"""
    skill_level_bytes = grimoire_data[48]
    print("Skill Level Bytes:", skill_level_bytes)
    print("\tSkill Level:",int(skill_level_bytes, base=16))

def parse_addon_bonus_level(grimoire_data):
    """Bytes 50 are the grimoire bonus level"""
    bonus_level_bytes = grimoire_data[49]
    print("Bonus Level Bytes:", bonus_level_bytes)
    print("\tBonus Level:",int(bonus_level_bytes, base=16))


def parse_grimoire(grimoire_data):
    print(grimoire_data)
    parse_grimoire_origin(grimoire_data)
    parse_grimoire_class(grimoire_data)
    parse_grimoire_origin_details(grimoire_data)
    parse_grimoire_mystery_bytes(grimoire_data)
    parse_name_of_trader(grimoire_data)
    parse_addon_bonus_type(grimoire_data)
    parse_addon_bonus_level(grimoire_data)
    parse_grimoire_skill(grimoire_data)
    parse_grimoire_skill_level(grimoire_data)
    print("\n\n")

    return 1

def parse_save_file(fname_path:Path):
    if not isinstance(fname_path, Path):
        fname_path = Path(fname_path)

    if fname_path.is_dir():
        fname_path = fname_path.joinpath("mo2r00_game.sav")

    file_bytes = fname_path.read_bytes()
    file_hex = file_bytes.hex(" ").split(" ")
    num_bytes = len(file_hex)

    if GRIMOIRE_START > num_bytes:
        raise RuntimeError("Invalid File")

    grimoire_info = []
    grimoire_data = []
    counter = 0
    for idx in range(GRIMOIRE_START, num_bytes):
        grimoire_data.append(file_hex[idx])
        if len(grimoire_data) == GRIMOIRE_LENGTH:
            print("Grimoire #{}".format(counter+1))
            grimoire_data = [x.upper() for x in grimoire_data]
            # grimoire_data = "40	00	07	00	02	17	07	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	DB	00	0A	00".split("\t")
            g_info = parse_grimoire(grimoire_data)
            if g_info:
                grimoire_info.append(g_info)
            
            counter += 1
            grimoire_data = []

        if counter == 400:
            ## Max of 400 Grimoires
            break

    return grimoire_info, "".join(file_hex)

if __name__ == "__main__":
    parse_save_file("backups/base/mo2r00_game.sav")