import os
import re

from selenium.webdriver import Firefox, Chrome

from src.clss.assistants import AnkiEditPageHandler
from src.clss.autoFlashCards import AutoFlashCards
from src.clss.cardDeliverers import SeleniumAnkiBot
from src.clss.sourceAdmins import (
                MyCardShelveAdmin, TextSourceAdmin, 
                DictBasedCardWriter
    )

phrases_file = 'frases.txt'
file_path = os.path.join(os.getcwd(), phrases_file)

login_file = 'data.json'
login_path = os.path.join(os.getcwd(), login_file)

writer = DictBasedCardWriter()
sourceAdmin = TextSourceAdmin(file_path, writer)
dbAdmin = MyCardShelveAdmin('db', 'cards')

driver = Chrome
deck_name = 'Default'
web_driver_args = {}
new_deck = False
page_handler = AnkiEditPageHandler(re)
deliver = SeleniumAnkiBot(
                web_driver=driver, 
                login_path=login_path, 
                deck_name=deck_name, 
                web_edit_page_handler=page_handler,
                new_deck=new_deck,
                **web_driver_args
            )

automaton = AutoFlashCards(deliver, sourceAdmin, dbAdmin)

if __name__ == "__main__":
    automaton.run_task()
    if len(automaton.card_list) == 0:
        print('No cards to create.')
