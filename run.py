#!venv/bin/python3

import os

from src.scales.scale4 import automaton
#from src.scales.scale3 import automaton
#from src.scales.scale2 import automaton
from src.funcs.textFunc import create_json_data_settings, set_json_file


def verify_settings() -> None:
    valid = True
    current_dir = os.getcwd()
    files = os.listdir(current_dir)
    DATA_SETTINGS_FILE = 'data.json'
    if not DATA_SETTINGS_FILE in files:
        valid = False
        set_json_file(DATA_SETTINGS_FILE,
                      {
                          'login': {'email': '', 'password': ''}
                      })
    return valid


def main() -> None:
    valid = verify_settings()
    if not valid:
        print('Insert the data into the created "data.json" file. Then, run this again!')
        return
    automaton.run_task()
    print(f"""
Total created cards: {len(automaton.card_list)}
Total inserted cards: {automaton.card_deliverer.total_inserted}""")
    if len(automaton.card_list) == 0:
        print('No cards to create.')


if __name__ == "__main__":
    main()
