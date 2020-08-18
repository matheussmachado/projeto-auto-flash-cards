from typing import List, TypeVar
from .cards import MyCard
from .sourceAdmins import MyCardShelveAdmin
from .abstractClasses import AbstractCardDeliverer
from .interfaces import SourceAdminInterface


class AutoFlashCards:
    def __init__(self, card_deliverer: AbstractCardDeliverer,
                    source_admin: SourceAdminInterface,
                    db_admin: MyCardShelveAdmin):
        self.card_deliverer = card_deliverer
        self.source_admin = source_admin
        self.db_admin = db_admin
        self._card_list: List[MyCard] = []

    @property
    def card_list(self) -> list:
        return self._card_list.copy()
    
    def _verify_cards(self) -> None:
        """
            Método que realiza a verificação de possiveis cards estocados na estrutura de persistência."""
        cards = self.db_admin.return_sources()
        self._card_list.extend(cards)

    def create_cards(self) -> None:                
        self._verify_cards()
        sources = self.source_admin.return_sources()
        self.db_admin.update_sources(sources)
        self.source_admin.update_sources()
        self._card_list.extend(sources)
    
    def run_task(self) -> None:
        self.create_cards()
        if len(self.card_list) == 0:
            return
        self.card_deliverer.deliver(self.card_list)
        cards = self.card_deliverer.card_list
        self.db_admin.update_sources(cards)
    