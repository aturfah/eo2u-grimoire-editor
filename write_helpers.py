from pathlib import Path

from parse_helpers import parse_save_file, write_save_file
from parse_helpers import NAME_TO_HEX, GRIMOIRE_BONUS_TYPE_MAP, GRIMOIRE_CLASS_MAP, GRIMOIRE_ORIGIN_MAP

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


if __name__ == "__main__":
    grimoire_info, file_hex = parse_save_file("backups/base/mo2r00_game.sav")

    grimoire_info[0] = modify_grimoire_skill(grimoire_info[0], "HP Up")

    write_save_file(Path("backups/base_mod/mo2r00_game.sav"), file_hex, grimoire_info)