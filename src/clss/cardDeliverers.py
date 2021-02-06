import os
from time import sleep
from typing import List, TypeVar

from .abstractClasses import AbstractCardDeliverer, AbstractPageObject
from .cards import MyCard
from .pageObjects import EditPage, DecksPage, LoginHandler
from .error import DataConfigError
from src.funcs.textFunc import get_from_json


class SeleniumAnkiBot(AbstractCardDeliverer):
    _LOCAL_COOKIES = 'login_cookie.pickle'
    _URL_EDIT = 'https://ankiuser.net/edit/'
    _URL_LOGIN = 'https://ankiweb.net/account/login'
    _driver = None
    login_handler = LoginHandler(_LOCAL_COOKIES)
    decks_page = DecksPage()
    edit_page = EditPage()

    def __init__(self, webdriver_configurator, user_data: str):
        super().__init__()
        self.user_data = user_data
        self.webdriver_configurator = webdriver_configurator
    
    def init_anki_page_webdriver(self):
        for attr in dir(self):
            a = getattr(self, attr)
            if isinstance(a, AbstractPageObject):
                a.webdriver = self._driver

    def set_driver_configurations(self):
        self._driver.implicitly_wait(30)
        self._driver.set_window_size(width=9999, height=9999)

    def deliver(self, card_list) -> list:
        self._card_list.extend(card_list)
        cookies_exists = True
        if not self._LOCAL_COOKIES in os.listdir():
            input('Please manually access your account on the page that will open in your browser. \nPRESS ENTER FOR LOGIN.')
            cookies_exists = False
        self._driver = self.webdriver_configurator.configure()
        self.set_driver_configurations()
        try:
            self._driver.get(self._URL_LOGIN)
        except Exception as err:
            self._driver.close()
            print("UNABLE TO CONNECT.\n", err)            
        else:
            self.init_anki_page_webdriver()
            self.login_handler.access(cookies_exists)
            decks_name = self.decks_page.get_decks_name()
            self._driver.get(self._URL_EDIT)
            self.deck_name_input(decks_name)
            for card in self.card_list:
                try:
                    self.edit_page.insert_card(card)
                except Exception as err:
                    print(err)
                else:
                    self.total_inserted += 1
                    self._update_card(card)
        finally:
            self._driver.quit()
    
    def deck_name_input(self, decks_name):
        deck_data = get_from_json(self.user_data, 'deck')
        if deck_data.get('name') and deck_data.get('new_deck') == False:
            if not deck_data.get('name') in decks_name:
                print(f"{deck_data.get('name')} name does not exist in the deck collection.")
                raise DataConfigError(deck_data.get('name'))
            self.edit_page.insert_given_deck_name(deck_data.get('name'))
        elif deck_data.get('name'):
            self.edit_page.insert_given_deck_name(deck_data.get('name'))
        
    def _update_card(self, card: MyCard) -> None:
        for i, c in enumerate(self.card_list):
            if c.representation == card.representation:
                break
        self._card_list[i].inserted = True
