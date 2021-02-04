import os
import json
from typing import List

def get_from_txt(file: str) -> List[str]:
    """
        Função que obtém frases de um arquivo .txt. Essa obtenção se dá orientada ao caractere de quebra de linha \\n. A função também realiza tratamento de espaços em branco a cada frase obtida e, se houver no arquivo apenas espaços em branco, o retorno será uma lista vazia.

        Args:
            file (str) - nome do arquivo que contém as frases. 
            (default: 'frases.txt')

        Returns:
            list - lista contendo as frases obtidas do arquivo."""
    phrases = []
    if os.path.isfile(file) and str(file).endswith(".txt"):
        with open(file, "r") as f:
            phrases = [
                line.strip() for line in f.read().split("\n") if line.strip() != ""
            ]
    else:
        print(f'\n\n"{file}" is not a valid file or file path.')
    return phrases
        



def get_from_json(path: str, query: str) -> str:
    with open(path) as j:
        content = j.read()
    result = json.loads(content)
    return result[query]



def create_json_data_settings(file_name: str) -> None:
    with open(file_name, 'w') as f:
        f.write(
'''{
    "login": {
        "email": "",
        "password":""
    },
    "deck": {
        "name": "",
        "new_deck": false
    },
    "imgPath": "imgFolder"
}
'''
        )


def create_json_config_file(file_name: str) -> None:
    with open(file_name, 'w') as file:
        file.write(
'''{
    "deck": {
    	"deck_name": "",
    	"new_deck": true
    },
    "application_file_name": "",
    "web_driver_user_settings": {
		"browser": "",
		"web_driver_args": {
			
		},
		"web_driver_options": {
			"headless": false
		},
		"auto_executable_path": true
	},
	"phrasesFile": "frases.txt",
	"imgPath": "",
    "drive_folder_name": ""
}'''
        )

def get_json(file) -> dict:
    with open(file, 'r') as f:
        content = f.read()
    deserialized = json.loads(content)
    return deserialized



def set_json_file(file, content: dict) -> None:
    serialized = json.dumps(content, indent=4)
    with open(file, 'w') as f:
        f.write(serialized)
    


'''def verify_in_json(file, key, value):
    with open(file, 'r') as f:
        content = f.read()
    load_content = json.loads(content)
    if not key in load_content.keys():
        load_content.update({key: value})
    elif not load_content[key]:
        load_content[key] = value
    dump_content = json.dumps(load_content, indent=4)
    with open(file, 'w') as f:
        f.write(dump_content)
'''
