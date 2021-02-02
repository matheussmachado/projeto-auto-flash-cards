from typing import List, Any
import shelve
from abc import ABC, abstractmethod

from .cards import MyCard


class AbstractWebPageContentHandler(ABC):
    """
        Filtrar conteúdos de páginas web para fornecer os recursos necessários à uma outra classe que o necessita para realizar seus objetivos."""    
    def __init__(self):
        self.page_source = None

    @abstractmethod
    def return_resources(self):
        ...
        



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



class AbstractSeleniumObject(ABC):
    def find_element(self, *locator):
        return self.webdriver.find_element(*locator)
    
    def find_elements(self, *locator):
        return self.webdriver.find_elements(*locator)



class AbstractPageObject(AbstractSeleniumObject, ABC):
    def __init__(self, webdriver=None):
        self.webdriver = webdriver