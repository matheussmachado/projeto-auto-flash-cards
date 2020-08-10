#!venv/bin/python3

import os

#from src.scales.scale3 import automaton
from src.scales.scale2 import automaton
from src.funcs.textFunc import create_json_data_settings, set_json_file


def verify_settings() -> None:
    valid = True
    current_dir = os.getcwd()
    files = os.listdir(current_dir)
    IMG_FOLDER = 'imgFolder'
    DATA_SETTINGS_FILE = 'data.json'
    if not IMG_FOLDER in files:
        os.mkdir(os.path.join(current_dir, IMG_FOLDER))
    if not DATA_SETTINGS_FILE in files:
        valid = False
        set_json_file(DATA_SETTINGS_FILE,
            {
                'login': {'email': '', 'password': ''}, 
                'folder_name': IMG_FOLDER
            })
    return valid



def main() -> None:            
    valid = verify_settings()
    if not valid:
        print('Insert the data into the created "data.json" file. Then, run this again!')
        return
    automaton.run_task()
    if len(automaton.card_list) == 0:
        print('No cards to create.')
    

if __name__ == "__main__":
    main()
