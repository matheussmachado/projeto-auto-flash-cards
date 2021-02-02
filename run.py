#!venv/bin/python3
import os

from src.funcs.textFunc import create_json_config_file, get_from_json

from src.clss.configurators import AppConfigurator



def verify_settings() -> None:
    valid = True
    current_dir = os.getcwd()
    files = os.listdir(current_dir)
    DATA_SETTINGS_FILE = 'config.json'
    if not DATA_SETTINGS_FILE in files:
        valid = False
        create_json_config_file(DATA_SETTINGS_FILE)
    return valid



def main() -> None:
    valid = verify_settings()
    if not valid:
        print('Insert the data into the created "config.json" file. Then, run this again!')
        return
    CONFIG_FILE = 'config.json'
    PACKAGE_PATH = os.path.join('src', 'apps')
    app_conf = AppConfigurator(CONFIG_FILE)
    app_module = app_conf.configure(PACKAGE_PATH)
    automaton = app_module.automaton
    automaton.run_task()
    print(f"""
Total created cards: {len(automaton.card_list)}
Total inserted cards: {automaton.card_deliverer.total_inserted}""")
    if len(automaton.card_list) == 0:
        print('No cards to create.')



if __name__ == "__main__":
    main()
