from pathlib import Path
from pprint import pprint

from parse_helpers import parse_save_file, write_save_file
from parse_helpers import NAME_TO_HEX, GRIMOIRE_BONUS_TYPE_MAP, GRIMOIRE_CLASS_MAP, GRIMOIRE_ORIGIN_MAP

GRIMOIRE_CLASS_ID_MAP = {v: k for k, v in GRIMOIRE_CLASS_MAP.items()}
GRIMOIRE_BONUS_ID_MAP = {v: k for k, v in GRIMOIRE_BONUS_TYPE_MAP.items()}
pprint(GRIMOIRE_CLASS_ID_MAP)

def modify_grimoire_skill(grimoire_datum:dict, skill_name:str):
    """Set the grimoire's skill"""
    skill_name = skill_name.strip()
    if skill_name not in NAME_TO_HEX.keys():
        raise ValueError("Invalid Skill Name: {}".format(skill_name))

    skill_hex = NAME_TO_HEX[skill_name]

    grimoire_datum = dict(grimoire_datum)
    grimoire_datum["skill_name"] = skill_name
    grimoire_datum["skill_id_bytes"] = skill_hex
    return grimoire_datum


def modify_grimoire_class(grimoire_datum:dict, class_name:str):
    """Set grimoire class; DOES NOT DO ANYTHING."""
    class_name = class_name.strip()
    if class_name not in GRIMOIRE_CLASS_ID_MAP.keys():
        raise ValueError("Invalid Class Name: {}".format(class_name))

    class_hex = GRIMOIRE_CLASS_ID_MAP[class_name]

    grimoire_datum = dict(grimoire_datum)
    grimoire_datum["grim_class"] = class_name
    grimoire_datum["grim_class_bytes"][0] = class_hex
    return grimoire_datum


def modify_grimoire_bonus(grimoire_datum:dict, bonus_type:str):
    """Set grimoire bonus."""
    bonus_type = bonus_type.strip()
    if bonus_type not in GRIMOIRE_BONUS_ID_MAP.keys():
        raise ValueError("Invalid Grimoire Bonus: {}".format(bonus_type))

    bonus_hex = GRIMOIRE_BONUS_ID_MAP[bonus_type]

    grimoire_datum = dict(grimoire_datum)
    grimoire_datum["bonus_type"] = bonus_type
    grimoire_datum["bonus_type_bytes"] = bonus_hex
    return grimoire_datum


def modify_grimoire_bonus_level(grimoire_datum:dict, bonus_level:int):
    """Set grimoire bonus level."""
    if bonus_level not in [x for x in range(4)]:
        raise ValueError("Bonus level must be between [0-3]")

    level_hex = "0{}".format(bonus_level)

    grimoire_datum = dict(grimoire_datum)
    grimoire_datum["bonus_level"] = bonus_level
    grimoire_datum["bonus_level_bytes"] = level_hex
    return grimoire_datum


if __name__ == "__main__":
    grimoire_info, file_hex = parse_save_file("backups/base/mo2r00_game.sav")

    print("Original:")
    pprint(grimoire_info[0])

    grimoire_info[0] = modify_grimoire_skill(grimoire_info[0], "Madness Curse")
    grimoire_info[0] = modify_grimoire_class(grimoire_info[0], "??? #1") ## Does this do anything?
    grimoire_info[0] = modify_grimoire_bonus(grimoire_info[0], "Cut Up")
    grimoire_info[0] = modify_grimoire_bonus_level(grimoire_info[0], 3)

    print("\bModified:")
    pprint(grimoire_info[0])

    write_save_file(Path("C:/Users/aturf/AppData/Roaming/Citra/sdmc/Nintendo 3DS/00000000000000000000000000000000/00000000000000000000000000000000/title/00040000/0015f200/data/00000001"), file_hex, grimoire_info)