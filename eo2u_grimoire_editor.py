import eel

from save_file_manager import SaveFileManager

@eel.expose
def get_random_number():
    eel.prompt_alerts(7)

@eel.expose
def get_date():
    eel.prompt_alerts(SFM.current_time())


@eel.expose
def load_file():
    try:
        SFM.load_file()
    except Exception as exc:
        print(exc)
        eel.prompt_alerts(str(exc))

    eel.prompt_alerts("Successfully loaded file: {}".format(SFM.filename))
    eel.setGrimoireDropdown(SFM.get_grimoire_labels())


@eel.expose
def reset_grimoire():
    SFM.reset_chosen_grimoire()


if __name__ == "__main__":
    SFM = SaveFileManager()

    eel.init('web')
    eel.start('index.html')