from .cards import MyCard
from .sourceAdmins import DataBaseAdmin

#TODO: realizar verificação de existencia de frases
class AutoCards:
    def __init__(self, card_deliverer, 
                    source_admin,
                    db_admin=DataBaseAdmin('db_cards', 'cards')):
        self.card_deliverer = card_deliverer
        self.source_admin = source_admin
        self.db_admin = db_admin
        self._card_list = []  
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
        self._card_list.extend(sources)
    
    def run_task(self) -> None:
        self.create_cards()
        self.card_deliverer.deliver(self.card_list)
        cards = self.card_deliverer.card_list
        self.source_admin.update_sources()
        self.db_admin.update_sources(cards)
    