from pathlib import Path
from pprint import pprint
from typing import Iterable
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
    "34": "Unknown Origin",
    "40": "Traded (in-game)",
    "44": "Traded (#3)", ## TODO: Verify
    "48": "?",
    "80": "Traded (Guild Card)",
    "88": "Traded (Guild Card #2)"
}

def parse_grimoire_origin(grimoire_data):
    """Bytes 1-2 define origin"""
    origin_bytes = grimoire_data[0:2]
    try:
        origin = GRIMOIRE_ORIGIN_MAP[origin_bytes[0]]
    except Exception:
        ## Don't have map but don't use this yet so...
        origin = "Unknown"

    # print("Origin Bytes:", origin_bytes)
    # print("\tOrigin: {}".format(origin))

    return origin, origin_bytes

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
    "0E": "Fafnir",
    "FF": "??? #3"
}

def parse_grimoire_class(grimoire_data):
    """Bytes 3-4 determine originating class"""
    class_bytes = grimoire_data[2:4]
    grimoire_class = GRIMOIRE_CLASS_MAP[class_bytes[0]]
    # print("Class Bytes:", class_bytes)
    # print("\tClass: {}".format(grimoire_class))

    return grimoire_class, class_bytes


def parse_grimoire_origin_details(grimoire_data):
    """Bytes 5-6 determine things like 'Overhead Ronin'"""
    ## TODO: Fill me in
    orig_details_bytes = grimoire_data[4:6]
    # print("Origin Details Bytes:", orig_details_bytes)

    return "", orig_details_bytes


def parse_grimoire_mystery_bytes(grimoire_data):
    """Bytes 7-8 are Mystery Byte"""
    mystery_bytes = grimoire_data[6:8]
    # print("Mystery Bytes:", mystery_bytes)

    return "".join(mystery_bytes)


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

    # print("Name Bytes:", "".join(name_bytes))
    # print("\tName:", gg_unicode)

    return gg_unicode, "".join(name_bytes), unknown_origin


GRIMOIRE_BONUS_TYPE_MAP= {
    "0000": "(None)",
    "7C02": "Cut Up",
    "7D02": "Stab Up",
    "7E02": "Bash Up",
    "7F02": "Fire Up",
    "8002": "Ice Up",
    "8102": "Volt Up",
    "8202": "Ail Inf. up",
    "8302": "Bind Inf. up",
    "8402": "Grimoire Chance Up",
    "8502": "Rare Enemy Up",
    "8602": "Ail Rec. Up",
    "8702": "Bind Rec. Up",
    "8802": "Drop Amount Up",
    "8902": "Victory HP",
    "8A02": "Victory TP",
    "8B02": "[L] Auto-Heal", ## Legendary
    "8C02": "[L] Self-Heal Amp", ## Legendary
    "8D02": "[L] Force Up", ## Legendary
    "8E02": "[L] Grimoire Skill Level Up", ## Legendary
    "8F02": "[L] Turn TP Recover", ## Legendary
    "9002": "[L] TP Cost Recovery" ## Legendary
}


def parse_addon_bonus_type(grimoire_data):
    """Bytes 45-46 are the grimoire bonus type"""
    bonus_type_bytes = grimoire_data[44:46]
    bonus_type = GRIMOIRE_BONUS_TYPE_MAP["".join(bonus_type_bytes)]
    # print("Bonus Type Bytes:", bonus_type_bytes)
    # print("\tBonus Type:", bonus_type)

    return bonus_type, bonus_type_bytes


def parse_grimoire_skill(grimoire_data):
    """Bytes 47-48 are the grimoire skill ID"""
    skill_id_bytes = grimoire_data[46:48]
    skill_name = HEX_TO_NAME["".join(skill_id_bytes)]
    # print("Grimoire Skill Bytes:", skill_id_bytes)
    # print("\tGrimoire Skill:", skill_name)

    return skill_name, skill_id_bytes


def parse_grimoire_skill_level(grimoire_data):
    """Bytes 49 are the grimoire skill level"""
    skill_level_bytes = grimoire_data[48]
    skill_level_dec = int(skill_level_bytes, base=16)
    # print("Skill Level Bytes:", skill_level_bytes)
    # print("\tSkill Level:", skill_level_dec)

    return skill_level_dec, skill_level_bytes

def parse_addon_bonus_level(grimoire_data):
    """Bytes 50 are the grimoire bonus level"""
    bonus_level_bytes = grimoire_data[49]
    bonus_level_dec = int(bonus_level_bytes, base=16)
    # print("Bonus Level Bytes:", bonus_level_bytes)
    # print("\tBonus Level:", bonus_level_dec)

    return bonus_level_dec, bonus_level_bytes


def parse_grimoire(grimoire_data):
    empty_grimoire = False
    if set(grimoire_data) == {"00"}:
        empty_grimoire = True

    try:
        origin, origin_bytes = parse_grimoire_origin(grimoire_data)
    except Exception as exc:
        raise RuntimeError("Error Parsing Grimoire Origin: {}".format(exc))

    try:
        grim_class, class_bytes = parse_grimoire_class(grimoire_data)
    except Exception as exc:
        raise RuntimeError("Error Parsing Grimoire Class: {}".format(exc))

    try:
        origin_details, origin_details_bytes = parse_grimoire_origin_details(grimoire_data)
    except Exception as exc:
        raise RuntimeError("Error Parsing Grimoire Origin: {}".format(exc))

    try:
        trader_name, trader_bytes, _ = parse_name_of_trader(grimoire_data)
    except Exception as exc:
        raise RuntimeError("Error Parsing Grimoire Trader Name: {}".format(exc))

    try:
        bonus_type, bonus_type_bytes = parse_addon_bonus_type(grimoire_data)
    except Exception as exc:
        raise RuntimeError("Error Parsing Grimoire Bonus: {}".format(exc))

    try:
        bl_dec, bl_hex = parse_addon_bonus_level(grimoire_data)
    except Exception as exc:
        raise RuntimeError("Error Parsing Grimoire Bonus Level: {}".format(exc))

    try:
        skill_name, skill_id_bytes = parse_grimoire_skill(grimoire_data)
    except Exception as exc:
        raise RuntimeError("Error Parsing Grimoire Skill: {}".format(exc))

    try:
        sl_dec, sl_hex = parse_grimoire_skill_level(grimoire_data)
    except Exception as exc:
        raise RuntimeError("Error Parsing Grimoire Skill Level: {}".format(exc))

    ## No clue what this does
    mystery_bytes = parse_grimoire_mystery_bytes(grimoire_data)

    return {
        "original_hex": "".join(grimoire_data),
        "empty": empty_grimoire,
        ## Parsed Values
        "origin": origin,
        "grim_class": grim_class,
        "origin_details": origin_details,
        "trader_name": trader_name,
        "bonus_type": bonus_type,
        "bonus_level": bl_dec,
        "skill_name": skill_name,
        "skill_level": sl_dec,
        ## Raw values
        "origin_bytes": origin_bytes,
        "grim_class_bytes": class_bytes,
        "origin_details_bytes": origin_details_bytes,
        "mystery_bytes": mystery_bytes,
        "trader_name_bytes": trader_bytes,
        "bonus_type_bytes": bonus_type_bytes,
        "bonus_level_bytes": bl_hex,
        "skill_id_bytes": skill_id_bytes,
        "skill_level_bytes": sl_hex
    }

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
            # print("Grimoire #{}".format(counter+1))
            grimoire_data = [x.upper() for x in grimoire_data]
            # grimoire_data = "40	00	07	00	02	17	07	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	00	DB	00	0A	00".split("\t")
            g_info = parse_grimoire(grimoire_data)
            if not "empty" in str(g_info["skill_name"]).lower():
                print(len(grimoire_info))
                pprint(g_info)
                print("\n\n")

            if g_info:
                grimoire_info.append(g_info)

            counter += 1
            grimoire_data = []

        if counter == 400:
            ## Max of 400 Grimoires
            break

    return grimoire_info, "".join(file_hex)


def recreate_grimoire_hex(grimoire_datum:dict):
    """Recreate the grimoire hex string from the dictinary."""
    output_str = ""

    output_str += "".join(grimoire_datum["origin_bytes"])
    output_str += "".join(grimoire_datum["grim_class_bytes"])
    output_str += "".join(grimoire_datum["origin_details_bytes"])
    output_str += grimoire_datum["mystery_bytes"]
    output_str += grimoire_datum["trader_name_bytes"]
    output_str += "".join(grimoire_datum["bonus_type_bytes"])
    output_str += "".join(grimoire_datum["skill_id_bytes"])
    output_str += grimoire_datum["skill_level_bytes"]
    output_str += grimoire_datum["bonus_level_bytes"]

    ## Make sure we don't lose anything
    assert len(output_str) == GRIMOIRE_LENGTH*2
    return output_str.lower()


def write_save_file(destination:Path, original_hex:str, grimoire_info:Iterable):
    grimoire_hex = "".join([recreate_grimoire_hex(x) for x in grimoire_info])
    start_posn_dec = GRIMOIRE_START*2
    output_hex = original_hex[:start_posn_dec] + \
        grimoire_hex + \
            original_hex[(start_posn_dec+len(grimoire_hex)):]

    ## Error checking before output
    if isinstance(destination, str):
        destination = Path(destination)
    if destination.is_dir():
        destination = destination.joinpath("mo2r00_game.sav")
    if not destination.exists():
        destination.touch()
    
    destination.write_bytes(bytes.fromhex(output_hex))


if __name__ == "__main__":
    grimoire_info, file_hex = parse_save_file("backups/base/mo2r00_game.sav")
    write_save_file(Path("backups/base_mod/mo2r00_game.sav"), file_hex, grimoire_info)