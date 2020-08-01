from time import sleep
from typing import List, TypeVar
from .abstractClasses import AbstractCardDeliverer
from .cards import MyCard
from src.funcs.textFunc import get_from_json

WebDriver = TypeVar('WebDriver')

class SeleniumAnkiBot(AbstractCardDeliverer):
    def __init__(self, browser: WebDriver, login_path: str) -> None:
        super().__init__()
        self.browser = browser
        self.login_path = login_path
        self.url = 'https://ankiweb.net/account/login'

    def deliver(self, card_list: list) -> list:
        self._card_list.extend(card_list)
        em, pw = get_from_json(self.login_path, 'login').values()
        try:
            self.browser = self.browser.__call__()
            self.browser.implicitly_wait(30)
            self.browser.get(self.url)
        except Exception as err:
            self.browser.close()
            print("NÃO FOI POSSÍVEL CONECTAR\n", err)
            input("\n\nPressione a tecla enter.")
            print("\nFINALIZANDO...")
        else:
            # LOGIN
            self.browser.find_element_by_css_selector(
                'input[id="email"]').send_keys(em)
            self.browser.find_element_by_css_selector(
                'input[type="password"]').send_keys(pw)
            self.browser.find_element_by_css_selector(
                'input[type="submit"]').click()
            sleep(1)
            # ADD BUTTON
            self.browser.find_elements_by_css_selector(
                'a[class="nav-link"]')[1].click()
            sleep(1)
            # INPUT FLASHCARDS
            for card in card_list:
                self._insert_card(card)             
        finally:
            self.browser.quit()
    
    def _insert_card(self, card: MyCard) -> None:
        try:
            self.browser.find_element_by_id("f0").send_keys(card.front)
            self.browser.find_element_by_id("f1").send_keys(card.back)
            self.browser.find_element_by_css_selector(
                'button[class$="primary"]').click()
            sleep(1)
        except Exception as err:
            print(err)
        else:
            self._update_card(card)
    
    def _update_card(self, card: MyCard) -> None:
        for i, c in enumerate(self.card_list):
            if c.representation == card.representation:
                break
        self._card_list[i].inserted = True
