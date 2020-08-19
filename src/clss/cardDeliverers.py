from time import sleep
from typing import List, TypeVar

from .abstractClasses import AbstractCardDeliverer
from .cards import MyCard
from src.funcs.textFunc import get_from_json

WebDriver = TypeVar('WebDriver')

class SeleniumAnkiBot(AbstractCardDeliverer):
    def __init__(self, web_driver: WebDriver, login_path: str) -> None:
        super().__init__()
        self.driver = web_driver
        self.login_path = login_path        
        self._url = 'https://ankiweb.net/account/login'    

    def deliver(self, card_list: list) -> list:
        self._card_list.extend(card_list)
        em, pw = get_from_json(self.login_path, 'login').values()
        try:            
            self._bot = self.driver.__call__()
            self._bot.implicitly_wait(30)
            self._bot.get(self._url)
        except Exception as err:
            self._bot.close()
            print("NÃO FOI POSSÍVEL CONECTAR\n", err)
            input("\n\nPressione a tecla enter.")
            print("\nFINALIZANDO...")
        else:
            # LOGIN
            self._called_driver = True
            self._bot.find_element_by_css_selector(
                'input[id="email"]').send_keys(em)
            self._bot.find_element_by_css_selector(
                'input[type="password"]').send_keys(pw)
            self._bot.find_element_by_css_selector(
                'input[type="submit"]').click()
            sleep(1)
            # ADD BUTTON
            self._bot.find_elements_by_css_selector(
                'a[class="nav-link"]')[1].click()
            sleep(1)            
            # INPUT FLASHCARDS
            for card in card_list:
                self._insert_card(card)
        finally:
            self._bot.quit()
            
    
    def _insert_card(self, card: MyCard) -> None:
        if self._bot:
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
