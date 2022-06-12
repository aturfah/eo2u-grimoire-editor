import eel
import parse_helpers as ph

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

@eel.expose
def prepare_ui():
    eel.setGrimoireDropdown(SFM.get_grimoire_labels())

    skill_names = list(ph.NAME_TO_HEX.keys())
    skill_names.sort()
    eel.setSkillNameDropdown(skill_names)()

    bonus_names = list(ph.GRIMOIRE_BONUS_TYPE_MAP.values())
    bonus_names.sort()
    eel.setGrimoireBonusDropdown(bonus_names)()


@eel.expose
def get_chosen_grimoire():
    return SFM.get_chosen_grimoire()


@eel.expose
def reset_grimoire():
    SFM.reset_chosen_grimoire()


if __name__ == "__main__":
    SFM = SaveFileManager()

    eel.init('web')
    eel.start('index.html')