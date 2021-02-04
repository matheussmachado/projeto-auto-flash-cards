import os
import pickle
from time import sleep

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import url_to_be

from .abstractClasses import AbstractPageObject, AbstractElementFinder
from .cards import MyCard


class EditPage(AbstractElementFinder):
    deck = (By.CSS_SELECTOR, 'input[id="deck"]')
    front_side = (By.ID, 'f0')
    back_side = (By.ID, 'f1')
    save = (By.CSS_SELECTOR, 'button[class$="primary"]')

    def insert_card(self, card: MyCard):
        self.find_element(*self.back_side).send_keys(card.back)
        self.find_element(*self.front_side).send_keys(card.front)
        self.find_element(*self.save).click()
        sleep(1)
    
    def insert_given_deck_name(self, deck_name, backspace_times=100):
        deck_field = self.find_element(*self.deck)
        ac = ActionChains(self.webdriver)
        ac.move_to_element(deck_field).click()
        for _ in range(backspace_times):
            ac.key_down(Keys.BACK_SPACE)
            ac.key_up(Keys.BACK_SPACE)
        ac.perform()
        deck_field.send_keys(deck_name)
        


class LoginPage(AbstractElementFinder):
    email = (By.CSS_SELECTOR, 'input[id="email"]')
    password = (By.CSS_SELECTOR, 'input[type="password"]')
    log_in = (By.CSS_SELECTOR, 'input[type="submit"]')

    def login(self, em, pw):
        self.find_element(*self.email).send_keys(em)
        self.find_element(*self.password).send_keys(pw)
        self.find_element(*self.log_in).click()
        sleep(1)



class DecksPage(AbstractElementFinder):
    decks_name = (By.CLASS_NAME, "pl-0")

    def get_decks_name(self):
        elements = self.find_elements(*self.decks_name)
        return [element.text.strip() for element in elements]
    


class LoginHandler(AbstractPageObject):
    _URL_DECK = 'https://ankiweb.net/decks/'

    def __init__(self, local_cookies_path: str):
        super().__init__()
        self.local_cookies_path = local_cookies_path

    def _save_login_cookie(self):
        new_cookie = self.webdriver.get_cookies()
        pickle.dump(new_cookie, open(self.local_cookies_path, "wb"))
    
    def _wait_for_manual_login(self):
        while True:
            if self.webdriver.current_url == self._URL_DECK:
                break
        self._save_login_cookie()

    def access(self, cookies_exists: bool) -> None:
        _URL_LOGIN = 'https://ankiweb.net/account/login'
        self.webdriver.get(_URL_LOGIN)
        #SE NÃO HOUVER O COOKIE GUARDADO -> PRIMEIRO ACESSO
        if not cookies_exists:
            self._wait_for_manual_login()
            return
        #SE HOUVER OS COOKIES DE LOGIN
        cookies = pickle.load(open(self.local_cookies_path, "rb"))
        for cookie in cookies:
            self.webdriver.add_cookie(cookie)
        try:
            self.webdriver.get(self._URL_DECK)
            wdw = WebDriverWait(self.webdriver, timeout=10)    
            wdw.until(url_to_be(self._URL_DECK))
        except TimeoutException:
            #AGUARDANDO LOGAR MANUALMENTE, CASO O COOKIE ESTEJA INVÁLIDO
            self._wait_for_manual_login()
        else:
            self._save_login_cookie()

        
