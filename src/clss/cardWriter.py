from typing import List, Dict, Union
from .cards import MyCard


class DictBasedCardWriter:
    """
        Classe auxiliar que recebe conteúdos(frase, path) de um SourceAdmin e os organiza em uma estrutura de dicionários, e escreve-os em objetos MyCard e retorna uma lista com esses objetos."""
    def __init__(self):        
        self._contents: List[Dict[str:str, str:str]] = []
        self._card_list: List[Union[MyCard, None]] = []

    @property
    def contents(self):        
        return self._contents.copy()
    
    @property
    def card_list(self):
        return self._card_list.copy()

    def update_contents(self, phrase: str, source: str) -> None:
        self._contents.append(
            {'phrase': phrase, 
            'path': source}
        )

    def return_written_cards(self) -> list:
        if len(self.contents) > 0:
            for c in self.contents:
                self._card_list.append(
                    MyCard(c['phrase'], c['path'])
                    )
        return self.card_list