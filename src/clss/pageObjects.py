from time import sleep

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .abstractClasses import AbstractPageObject
from .cards import MyCard


class EditPage(AbstractPageObject):
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
        


class LoginPage(AbstractPageObject):
    email = (By.CSS_SELECTOR, 'input[id="email"]')
    password = (By.CSS_SELECTOR, 'input[type="password"]')
    log_in = (By.CSS_SELECTOR, 'input[type="submit"]')

    def login(self, em, pw):
        self.find_element(*self.email).send_keys(em)
        self.find_element(*self.password).send_keys(pw)
        self.find_element(*self.log_in).click()
        sleep(1)



class DecksPage(AbstractPageObject):
    decks_name = (By.CLASS_NAME, "pl-0")

    def get_decks_name(self):
        elements = self.find_elements(*self.decks_name)
        return [element.text.strip() for element in elements]
    
    