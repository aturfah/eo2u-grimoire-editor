import eel
import random
from datetime import datetime

import parse_helpers as ph
import ui_helpers as uih

@eel.expose
def get_random_name():
    eel.prompt_alerts('Random name')

@eel.expose
def get_random_number():
    eel.prompt_alerts(random.randint(1, 100))

@eel.expose
def get_date():
    eel.prompt_alerts(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

@eel.expose
def get_ip():
    eel.prompt_alerts('127.0.0.1')


if __name__ == "__main__":
    eel.init('web')
    eel.start('index.html')