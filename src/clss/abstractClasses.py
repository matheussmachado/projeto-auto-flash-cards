from typing import List
from abc import ABC, abstractmethod
from .cards import MyCard


class AbstractCardDeliverer(ABC):
    
    def __init__(self):
        self._card_list: List[MyCard] = []

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


'''class AbstractImageSource(ABC):    
    @abstractmethod
    def get_images(self):
        ...
    
    def remove_images(self):
        ...'''

