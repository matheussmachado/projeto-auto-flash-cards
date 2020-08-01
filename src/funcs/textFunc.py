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