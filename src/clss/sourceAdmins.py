import shelve
from typing import List, Dict
from .interfaces import SourceAdminInterface
from .cards import MyCard
from .cardWriter import DictBasedCardWriter
from src.funcs import get_from_txt



class ShelveAdmin(SourceAdminInterface):
    """
        Classe que herda de AbstraticSourceAdmin e que implementa seus contratos, tornando-a responsável por gerenciar a estrutura de persistência shelve, que estoca objetos MyCard gerados durante a tarefa principal."""
    def __init__(self, db_cards: str, db_key: str) -> None:
        super().__init__()
        self.db_cards = db_cards
        self.db_key = db_key
        self._database = shelve

    def _verify_key(self) -> None:
        """
            Método que realiza a verificação de existencia da key/coluna que eventualmente está estocado objetos MyCard."""
        with self._database.open(self.db_cards) as db:
            if not self.db_key in db.keys():
                db[self.db_key] = []

    def update_sources(self, cards: list) -> None:
        """
            Método resposável pela atualização da estrutura de persistência, de acordo com o status de inserido do objeto MyCard.

            Args:
                cards (list): lista e objetos MyCard a serem submetido por avaliação e comparação com objetos MyCard eventualmente estocados na estrutura de db."""
        if len(cards) == 0:
            return
        self._verify_key()
        with self._database.open(self.db_cards) as db:
            cards_temp = db[self.db_key]            
            c_temp_repr = [card.representation for card in cards_temp]            

            for card in cards:
                if card.inserted == False:
                    if not card.representation in c_temp_repr:
                        cards_temp.append(card)

                if card.inserted == True:
                    c_temp = card
                    c_temp.inserted = False
                    for i, c in enumerate(cards_temp):                    
                        if c.representation == c_temp.representation:
                            cards_temp.pop(i)
                            break
            db[self.db_key] = cards_temp

    def return_sources(self) -> list:
        """
            Método que retorna uma lista de objetos MyCard estocados na estrutura de persistencia."""
        self._verify_key()
        with self._database.open(self.db_cards) as db:
            cards_list = db[self.db_key]
        return cards_list        



class TextSourceAdmin(SourceAdminInterface):
    """
        Classe que herda de AbstractSourceAdmin e implementa os contratos de retorno e atualização de fontes de conteúdo para a criação de cartões, no contexto de criação através de um arquivo de texto."""
    def __init__(self, source: str, writer: DictBasedCardWriter) -> None:
        self.source = source
        self.writer = writer
        self._card_list = []
        
    @property
    def card_list(self):
        return self._card_list.copy()

    def return_sources(self) -> str:
        """
            Obtém o conteúdo, organiza e retorna os cards gerados."""        
        phrases = get_from_txt(self.source)
        if len(phrases) == 0:            
            return phrases
        for phrase in phrases:
           self.writer.update_contents(phrase, self.source)        
        return self.writer.return_written_cards()

    def update_sources(self) -> None:
        """
            Atualiza a fonte de conteúdo após a escrita de objetos MyCard e posterior inserção no banco de dados."""
        contents = self.writer.contents
        if len(contents) == 0:
            return
        phrases = [card['phrase'] for card in contents]
        source = get_from_txt(self.source)
        update = [phrase for phrase in source if phrase not in phrases]
        with open(self.source, "w") as source:
            for phrase in update:
                source.write(f"{phrase}\n")
    