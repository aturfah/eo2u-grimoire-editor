
from datetime import datetime

import modify_helpers as mh
import parse_helpers as ph

class SaveFileManager():
    def __init__(self) -> None:
        pass


    def current_time(self):
        """for debugging purposes"""
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")