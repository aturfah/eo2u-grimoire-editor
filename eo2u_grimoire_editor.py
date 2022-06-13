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
def get_grimoire_dropdown_options():
    return SFM.get_grimoire_labels()


@eel.expose
def get_skill_names():
    skill_names = list(ph.NAME_TO_HEX.keys())
    skill_names.sort()

    return skill_names


@eel.expose
def get_bonus_types():
    bonus_names = list(ph.GRIMOIRE_BONUS_TYPE_MAP.values())
    bonus_names.sort()

    return bonus_names


@eel.expose
def get_chosen_grimoire():
    return SFM.get_chosen_grimoire()


@eel.expose
def get_chosen_grimoire_idx():
    return SFM.chosen_idx



@eel.expose
def update_chosen_grimoire(new_idx):
    if not isinstance(new_idx, int):
        new_idx = int(new_idx)

    SFM.chosen_idx = new_idx


@eel.expose
def update_grimoire_skill(skill_name):
    SFM.set_grimoire_skill(skill_name)


@eel.expose
def update_grimoire_skill_level(new_level):
    SFM.set_grimoire_skill_level(new_level)


@eel.expose
def update_grimoire_bonus_type(new_bonus):
    SFM.set_grimoire_bonus_type(new_bonus)


@eel.expose
def update_grimoire_bonus_level(new_bonus):
    SFM.set_grimoire_bonus_level(new_bonus)


@eel.expose
def reset_grimoire():
    SFM.reset_chosen_grimoire()


if __name__ == "__main__":
    SFM = SaveFileManager()

    eel.init('web')
    eel.start('index.html')