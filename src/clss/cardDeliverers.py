import os
from time import sleep
from typing import List, TypeVar

from .abstractClasses import AbstractCardDeliverer, AbstractPageObject
from .cards import MyCard
from .pageObjects import EditPage, DecksPage, LoginHandler
from .error import DataConfigError
from src.funcs.textFunc import get_from_json


class SeleniumAnkiBot(AbstractCardDeliverer):
    _URL_EDIT = 'https://ankiuser.net/edit/'
    _LOCAL_COOKIES = 'login_cookie.pickle'
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

    def deliver(self, card_list) -> list:
        self._card_list.extend(card_list)
        cookies_exists = True
        if not self._LOCAL_COOKIES in os.listdir():
            input('Please manually access your account on the page that will open in your browser. \nPRESS ENTER FOR LOGIN.')
            cookies_exists = False
        try:
            #TODO: melhorar essa parte
            self._driver = self.webdriver_configurator.configure()
            self._driver.implicitly_wait(30)
            self._driver.set_window_size(width=9999, height=9999)
        except Exception as err:
            #TODO: TENTAR JOGAR ESSA EXCEÇÃO PARA O LOGIN_HANDLER
            if self._driver:
                self._driver.close()
            print("UNABLE TO CONNECT.\n", err)            
        else:
            self.init_anki_page_webdriver()
            self.login_handler.access(cookies_exists)
            #-------------------------------------------------
            decks_name = self.decks_page.get_decks_name()
            self._driver.get(self._URL_EDIT)
            self.deck_name_input(decks_name)        
            #-------------------------------------------------
            for card in self.card_list:
                try:
                    self.edit_page.insert_card(card)
                except Exception as err:
                    print(err)
                else:
                    self.total_inserted += 1
                    self._update_card(card)
        finally:
            if self._driver:
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
                
    '''
    from contextlib import contextmanager

    @contextmanager
    def _deliver_this(self):
        self._driver = self.webdriver_configurator.configure()
        try:
            yield self._driver
        finally:
            if self._driver:
                self._driver.quit()
    
    with _deliver_this() as d:...

    '''


class SeleniumAnkiBotDeprecated(AbstractCardDeliverer):
    def __init__(self, webdriver_configurator, user_data: str):
        super().__init__()
        self.user_data = user_data
        self.webdriver_configurator = webdriver_configurator
        self._URL = 'https://ankiweb.net/account/login'
        self._bot = None
    
    @property
    def bot(self):
        return self._bot
    
    @bot.setter
    def bot(self, webdriver):
        self._bot = webdriver

    def deliver(self, card_list: list) -> list:
        self._card_list.extend(card_list)
        em, pw = get_from_json(self.user_data, 'login').values()
        deck = get_from_json(self.user_data, 'deck')
        try:
            self._bot = self.webdriver_configurator.configure()
            self._bot.implicitly_wait(30)
            self._bot.get(self._URL)
            self._bot.set_window_size(width=9999, height=9999)
        except Exception as err:
            if self._bot:
                self._bot.close()
            print("UNABLE TO CONNECT.\n", err)            
        else:
            # LOGIN PAGE
            print('LOGIN PAGE')
            self._bot.find_element_by_css_selector(
                'input[id="email"]').send_keys(em)
            self._bot.find_element_by_css_selector(
                'input[type="password"]').send_keys(pw)
            self._bot.find_element_by_css_selector(
                'input[type="submit"]').click()
            sleep(1)
            # DECKS PAGE
            print('DECK PAGE')
            self._bot.find_elements_by_css_selector(
                'a[class="nav-link"]')[1].click()
            sleep(1)
            # EDIT PAGE
            print('EDIT PAGE')
            if deck["name"]:
                self._insert_given_deck_name(deck["name"])
            for card in card_list:
                self._insert_card(card)
        finally:
            if self._bot:
                self._bot.quit()

    def _insert_given_deck_name(self, deck_name) -> None:
        deck_field = self._bot.find_element_by_css_selector('input[id="deck"]')
        backspace_times = 100
        ac = ActionChains(self._bot)
        ac.move_to_element(deck_field).click()
        for _ in range(backspace_times): #GABIARRAZADA
            ac.key_down(Keys.BACK_SPACE)
            ac.key_up(Keys.BACK_SPACE)
        ac.perform()
        deck_field.send_keys(deck_name)

    def _insert_card(self, card: MyCard) -> None:
        try:
            self._bot.find_element_by_id("f0").send_keys(card.front)
            self._bot.find_element_by_id("f1").send_keys(card.back)
            self._bot.find_element_by_css_selector(
                'button[class$="primary"]').click()
            sleep(1)
        except Exception as err:
            print(err)
        else:
            self.total_inserted += 1
            self._update_card(card)
    
    def _update_card(self, card: MyCard) -> None:
        for i, c in enumerate(self.card_list):
            if c.representation == card.representation:
                break
        self._card_list[i].inserted = True




class SeleniumAnkiBotCRASHED(AbstractCardDeliverer):
    """
    def __init__(
            self, web_driver: WebDriver,
            user_data: str,
            web_edit_page_handler=None,
            **web_driver_args
    ):
    """
    def __init__(
            self, web_driver_settings,
            user_data: str,
            web_edit_page_handler=None,
            
    ):
        super().__init__()
        #self.driver = web_driver
        self.user_data = user_data
        self.web_driver_settings = web_driver_settings
        self.page_handler = web_edit_page_handler
        #self.web_driver_args = web_driver_args
        self._URL = 'https://ankiweb.net/account/login'
        self._bot = None

    def deliver(self, card_list: list) -> list:
        self._card_list.extend(card_list)
        em, pw = get_from_json(self.user_data, 'login').values()
        deck = get_from_json(self.user_data, 'deck')
        try:
            """
            self._bot = self.driver(
                **self.web_driver_args
                )
            """
            self._bot = self.web_driver_settings["driver"](
                    **self.web_driver_settings["web_driver_args"]
                )
            self._bot.implicitly_wait(30)
            self._bot.get(self._URL)
            self._bot.set_window_size(width=1366, height=747)
        except Exception as err:
            if self._bot:
                self._bot.close()
            print("UNABLE TO CONNECT.\n", err)            
        else:
            # LOGIN PAGE
            print('LOGIN PAGE')
            self._bot.find_element_by_css_selector(
                'input[id="email"]').send_keys(em)
            self._bot.find_element_by_css_selector(
                'input[type="password"]').send_keys(pw)
            self._bot.find_element_by_css_selector(
                'input[type="submit"]').click()
            sleep(1)
            # DECKS PAGE
            print('DECK PAGE')
            self._bot.find_elements_by_css_selector(
                'a[class="nav-link"]')[1].click()
            sleep(1)
            # EDIT PAGE
            print('EDIT PAGE')
            if deck["name"]:
                if not self.page_handler:
                    print('Was not given the web page content handler.')
                    return
                self.page_handler.page_source = self._bot.page_source
                r = self.page_handler.return_resources()
                if deck["name"] in r["deck_names"] or deck["new_deck"]:
                    self._insert_given_deck_name(
                        r["backspace_times"], deck["name"])
                else:
                    print('The given deck name does not exist.')
                    return
            for card in card_list:
                self._insert_card(card)
        finally:
            if self._bot:
                self._bot.quit()            

    def _insert_given_deck_name(self, 
                                backspace_times: str,
                                deck_name) -> None:
        deck_field = self._bot.find_element_by_css_selector('input[id="deck"]')
        ac = ActionChains(self._bot)
        ac.move_to_element(deck_field).click()
        for _ in range(backspace_times):
            ac.key_down(Keys.BACK_SPACE)
            ac.key_up(Keys.BACK_SPACE)
        ac.perform()
        deck_field.send_keys(deck_name)

    def _insert_card(self, card: MyCard) -> None:
        try:
            self._bot.find_element_by_id("f0").send_keys(card.front)
            self._bot.find_element_by_id("f1").send_keys(card.back)
            self._bot.find_element_by_css_selector(
                'button[class$="primary"]').click()
            sleep(1)
        except Exception as err:
            print(err)
        else:
            self.total_inserted += 1
            self._update_card(card)
    
    def _update_card(self, card: MyCard) -> None:
        for i, c in enumerate(self.card_list):
            if c.representation == card.representation:
                break
        self._card_list[i].inserted = True
