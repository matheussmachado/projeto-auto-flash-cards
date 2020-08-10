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
    while True:
        if os.path.isfile(file) and str(file).endswith(".txt"):
            with open(file, "r") as f:
                phrases = [
                    line.strip() for line in f.read().split("\n") if line.strip() != ""
                ]
                return phrases
        else:
            print(f'\n\n"{file}" não é um arquivo ou um path de arquivo válido.')
            file = input(
                "\nInsira um arquivo existente no mesmo path da VENV ou insira um path de arquivo válido: "
            )



def get_from_json(path: str, query: str) -> str:
    with open(path) as j:
        content = j.read()
    result = json.loads(content)
    return result[query]



def create_json_data_settings() -> None:
    with open('data1.json', 'w') as f:
        f.write(
'''{
    "login": {
        "email": "",
        "password":""
    },
    "imgPath": "imgFolder"
}
'''
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
