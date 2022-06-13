from copy import deepcopy
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from pprint import pprint

import modify_helpers as mh
import parse_helpers as ph

## Hide tkinter window
root = tk.Tk()
root.wm_attributes('-topmost', 1)
root.withdraw()


def invert_dictionary(dict_in):
    return {v: k for k, v in dict_in.items()}


class SaveFileManager():
    def __init__(self) -> None:
        ## Save File Information
        self.filename = None
        self.orig_hex = None
        self.orig_grimoire_data = None
        self.grimoire_data = None

        self.chosen_idx = 0

    def _load_file_helper(self, filename):
        try:
            self.orig_grimoire_data, self.orig_hex = ph.parse_save_file(filename)
            self.grimoire_data = deepcopy(self.orig_grimoire_data)
        except Exception as exc:
            raise exc

    def load_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("SAV files", ".sav")])
        if not self.filename:
            return

        try:
            self._load_file_helper(self.filename)
        except Exception as exc:
            raise exc

    def save_file(self):
        destination = filedialog.asksaveasfilename(filetypes=[("SAV files", ".sav")])
        if not destination:
            return

        try:
            ph.write_save_file(destination, self.orig_hex, self.grimoire_data)
        except Exception as exc:
            raise exc

        ## Reload from new file
        self._load_file_helper(destination)

        return destination

    def get_grimoire_labels(self):
        output = []
        widths = {key:0 for key in ["skill_name", "skill_level"]}
        for rec in self.grimoire_data:
            for key in widths:
                widths[key] = max(widths[key], len(str(rec[key])))

        widths["skill_level"] += 2

        for g_datum in self.grimoire_data:
            if g_datum["empty"] is True:
                output.append("(Empty)")
                continue

            bonus_str = ""
            if g_datum["bonus_type"] != "(None)":
                bonus_str = "({name} Lv{level})".format(
                    name=g_datum["bonus_type"],
                    level=g_datum["bonus_level"]
                )

            ## Can we Monospace this
            out_str = f"{g_datum['skill_name']:{widths['skill_name']}} {'Lv{}'.format(g_datum['skill_level']):{widths['skill_level']}} {bonus_str}"
            out_str = out_str.replace(" ", "&nbsp;")
            output.append(out_str)

        return output

    def set_grimoire_skill(self, skill_name):
        """Set the skill ID for the grimoire and the corresponding hex."""
        skill_bytes = ph.NAME_TO_HEX[skill_name]
        old_bytes = "".join(self.grimoire_data[self.chosen_idx]["skill_id_bytes"])

        self.grimoire_data[self.chosen_idx]["skill_name"] = skill_name
        self.grimoire_data[self.chosen_idx]["skill_id_bytes"] = skill_bytes

        ## Set skill to None, should be level 0
        if set("".join(skill_bytes)) == {"0"}:
            self.set_grimoire_skill_level(0)
        ## Skill used to be none, set bonus to level 1
        elif set(old_bytes) == {"0"}:
            self.set_grimoire_skill_level(1)

    def set_grimoire_skill_level(self, new_level):
        if not isinstance(new_level, int):
            new_level = int(new_level)

        self.grimoire_data[self.chosen_idx]["skill_level"] = new_level
        self.grimoire_data[self.chosen_idx]["skill_level_bytes"] = hex(new_level).removeprefix("0x").zfill(2)

    def set_grimoire_bonus_type(self, new_bonus):
        bonus_bytes = invert_dictionary(ph.GRIMOIRE_BONUS_TYPE_MAP)[new_bonus]
        bonus_bytes_list = [bonus_bytes[:2], bonus_bytes[2:]]
        old_bytes = "".join(self.grimoire_data[self.chosen_idx]["bonus_type_bytes"])

        self.grimoire_data[self.chosen_idx]["bonus_type"] = new_bonus
        self.grimoire_data[self.chosen_idx]["bonus_type_bytes"] = bonus_bytes_list

        ## Set Bonus to None, should be level 0
        if set(bonus_bytes) == {"0"}:
            self.set_grimoire_bonus_level(0)
        ## Bonus used to be none, set bonus to level 1
        elif set(old_bytes) == {"0"}:
            self.set_grimoire_bonus_level(1)



    def set_grimoire_bonus_level(self, new_level):
        if not isinstance(new_level, int):
            new_level = int(new_level)

        self.grimoire_data[self.chosen_idx]["bonus_level"] = new_level
        self.grimoire_data[self.chosen_idx]["bonus_level_bytes"] = hex(new_level).removeprefix("0x").zfill(2)

    def get_chosen_grimoire(self):
        """Get the grimoire currently chosen."""
        return self.grimoire_data[self.chosen_idx]

    def reset_chosen_grimoire(self):
        """Return a grimoire to its original state."""
        self.grimoire_data[self.chosen_idx] = deepcopy(self.orig_grimoire_data[self.chosen_idx])

    def current_time(self):
        """for debugging purposes"""
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")