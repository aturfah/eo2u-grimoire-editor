from copy import deepcopy
from datetime import datetime
# import tkinter as tk
from tkinter import filedialog

import modify_helpers as mh
import parse_helpers as ph

## Hide tkinter window
# root = tk.Tk()
# root.withdraw()

class SaveFileManager():
    def __init__(self) -> None:
        ## Save File Information
        self.filename = None
        self.orig_hex = None
        self.orig_grimoire_data = None
        self.grimoire_data = None

        self.chosen_idx = 0

    def load_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("SAV files", ".sav")])
        if not self.filename:
            return

        try:
            self.orig_grimoire_data, self.orig_hex = ph.parse_save_file(self.filename)
            self.grimoire_data = deepcopy(self.orig_grimoire_data)
        except Exception as exc:
            raise exc

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

    def get_chosen_grimoire(self):
        return self.grimoire_data[self.chosen_idx]

    def reset_chosen_grimoire(self):
        """Return a grimoire to its original state."""
        self.grimoire_data[self.chosen_idx] = deepcopy(self.orig_grimoire_data[self.chosen_idx])


    def current_time(self):
        """for debugging purposes"""
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")