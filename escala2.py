import os

from selenium.webdriver import Firefox, Chrome

from src.clss.autoCards import AutoCards
from src.clss.sourceAdmins import (
    DataBaseAdmin, TextSourceAdmin, DataBaseAdmin, DictBasedCardWriter
    )
from src.clss.cardDeliverers import SeleniumAnkiBot

file = 'frases.txt'
file_path = os.path.join(os.getcwd(), file)

#deliver = SeleniumAnkiBot(Firefox, 'login.txt')
deliver = SeleniumAnkiBot(Chrome, 'login.txt')
writer = DictBasedCardWriter()
sourceAdmin = TextSourceAdmin(file_path, writer)
dbAdmin = DataBaseAdmin('db_cards', 'cards')

ac = AutoCards(deliver, sourceAdmin, dbAdmin)

if __name__ == "__main__":
    ac.run_task()
    if len(ac.card_list) == 0:
        print('No cards to create.')
