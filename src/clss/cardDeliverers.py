from time import sleep
from typing import List, TypeVar

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from .abstractClasses import AbstractCardDeliverer, AbstractWebPageContentHandler
from .cards import MyCard
from src.funcs.textFunc import get_from_json

WebDriver = TypeVar('WebDriver')

class SeleniumAnkiBot(AbstractCardDeliverer):
    def __init__(
            self, web_driver: WebDriver,
            login_path: str,
            deck_name=None,
            web_edit_page_handler=None,
            new_deck=False,
            **web_driver_args
    ):
        super().__init__()
        self.driver = web_driver
        self.login_path = login_path
        self.page_handler = web_edit_page_handler
        self.deck_name = deck_name
        self.new_deck = new_deck
        self.web_driver_args = web_driver_args
        self._URL = 'https://ankiweb.net/account/login'
        self._bot = None

    def deliver(self, card_list: list) -> list:
        self._card_list.extend(card_list)
        em, pw = get_from_json(self.login_path, 'login').values()
        try:
            self._bot = self.driver(
                **self.web_driver_args
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
            if self.deck_name: 
                if not self.page_handler:
                    print('Was not given the web page content handler.')
                    return
                self.page_handler.page_source = self._bot.page_source
                r = self.page_handler.return_resources()
                if self.deck_name in r["deck_names"] or self.new_deck:
                    self._insert_given_deck_name(
                        r["backspace_times"])
                else:
                    print('The given deck name does not exist.')
                    return
            for card in card_list:
                self._insert_card(card)
        finally:
            if self._bot:
                self._bot.quit()            

    def _insert_given_deck_name(self, 
                                backspace_times: int) -> None:
        deck_field = self._bot.find_element_by_css_selector('input[id="deck"]')
        ac = ActionChains(self._bot)
        ac.move_to_element(deck_field).click()
        for _ in range(backspace_times):
            ac.key_down(Keys.BACK_SPACE)
            ac.key_up(Keys.BACK_SPACE)
        ac.perform()
        deck_field.send_keys(self.deck_name)

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
