from typing import List, Any
import shelve
from abc import ABC, abstractmethod

from .cards import MyCard


class AbstractCardDeliverer(ABC):
    
    def __init__(self):
        self._card_list: List[MyCard] = []
        self.total_inserted = 0

    @property
    def card_list(self):
        return self._card_list.copy()

    @abstractmethod
    def deliver(self):
        ...
    
    @abstractmethod
    def _insert_card(self):
        ...

    @abstractmethod
    def _update_card(self):
        ...


class AbstractShelveKeyAdmin(ABC):
    def __init__(self, db_cards: str, db_key: str) -> None:
        super().__init__()
        self.db_cards = db_cards
        self.db_key = db_key
        self._database = shelve

    @abstractmethod
    def update_sources(self): 
        """
            Método a ser especializado pela subclasse."""
        ...

    def _verify_key(self) -> None:
        """
            Método que realiza a verificação de existencia da key/coluna que eventualmente está estocado objetos MyCard."""
        with self._database.open(self.db_cards) as db:
            if not self.db_key in db.keys():
                db[self.db_key] = []        

    def return_sources(self) -> list:
        """
            Método que retorna uma lista de objetos MyCard estocados na estrutura de persistencia."""
        self._verify_key()
        with self._database.open(self.db_cards) as db:
            cards_list = db[self.db_key]
        return cards_list

    def _insert(self, this: Any) -> None:
        with self._database.open(self.db_cards) as db:
            db[self.db_key] = this