from copy import deepcopy
from datetime import datetime
from tkinter import filedialog

import modify_helpers as mh
import parse_helpers as ph

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


    def reset_chosen_grimoire(self):
        """Return a grimoire to its original state."""
        self.grimoire_data[self.chosen_idx] = deepcopy(self.orig_grimoire_data[self.chosen_idx])


    def current_time(self):
        """for debugging purposes"""
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")