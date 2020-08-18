import shelve
from typing import List, Dict

from .cards import MyCard
from .cardWriter import DictBasedCardWriter
from . abstractClasses import AbstractShelveKeyAdmin
from .interfaces import (SourceAdminInterface,
                            ImageSourceInterface, 
                            TextExtractorInterface)

from src.funcs.textFunc import get_from_txt





class MyCardShelveAdmin(AbstractShelveKeyAdmin):
    def __init__(self, db_cards: str, db_key: str) -> None:
        super().__init__(db_cards, db_key)
        
    def update_sources(self, cards: list) -> None:
        """
            Método resposável pela atualização da estrutura de persistência, de acordo com o status de inserido do objeto MyCard.

            Args:
                cards (list): lista e objetos MyCard a serem submetido por avaliação e comparação com objetos MyCard eventualmente estocados na estrutura de db."""
        if len(cards) == 0:
            return
        self._verify_key()        
        cards_temp = self.return_sources()
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
        self._insert(cards_temp)    



class DriveFileIdShelveAdmin(AbstractShelveKeyAdmin): 
    def __init__(self, db_cards, db_key):
        super().__init__(db_cards, db_key)
    
    def update_sources(self, _id_list: list) -> None:
        self._insert(_id_list)


class TextSourceAdmin(SourceAdminInterface):
    """
        Classe que herda de AbstractSourceAdmin e implementa os contratos de retorno e atualização de fontes de conteúdo para a criação de cartões, no contexto de criação através de um arquivo de texto."""
    def __init__(self, text_source: str, writer: DictBasedCardWriter) -> None:
        self.source = text_source
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
    


class ImageSourceAdmin(SourceAdminInterface):    
    def __init__(self, image_source: ImageSourceInterface, 
                    writer: DictBasedCardWriter,
                    text_extractor: TextExtractorInterface) -> None:
        self.source = image_source
        self.writer = writer
        self.extractor = text_extractor

    def return_sources(self):    
        imgs_data = self.source.get_images()
        for data in imgs_data:
            try:
                phrase = self.extractor.img_to_str(data['bytes'])
            except Exception as err:
                print(err)
            else:
                if phrase:
                    self.writer.update_contents(phrase, data['source'])
        return self.writer.return_written_cards()
    
    def update_sources(self):
        imgs_src = [src['source'] for src in self.writer.contents]
        self.source.remove_images(imgs_src)
        