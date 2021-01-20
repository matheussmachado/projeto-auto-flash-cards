import os
import json

SAMPLE_FOLDER = "samples"
IMG_FOLDER = 'imgFolder'
PG_SOURCE = 'page_source.html'
CONFIG_FILE = 'config(sample).json'
FILLED_TEXT = 'frasesTestePreenchidaWriter.txt'
EMPTY_TEXT = 'frasesTesteVazia.txt'

filled_text_path = os.path.join(SAMPLE_FOLDER, FILLED_TEXT)
empty_text_path = os.path.join(SAMPLE_FOLDER, EMPTY_TEXT)
img_folder_path = os.path.join(SAMPLE_FOLDER, IMG_FOLDER)
config_file_path = os.path.join(SAMPLE_FOLDER, CONFIG_FILE)


with open(config_file_path, 'r') as f:
    config_file_str = f.read()

config_file_dict = json.loads(config_file_str)
config_file_dict.update(phrasesFile=filled_text_path)
config_file_dict.update(imgPath=img_folder_path)

with open(config_file_path, 'w') as f:
    f.write(json.dumps(config_file_dict, indent=4))
