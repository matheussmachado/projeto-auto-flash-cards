import os

from selenium.webdriver import Firefox, Chrome

from src.clss.autoFlashCards import AutoFlashCards
from src.clss.sourceAdmins import (
                ShelveAdmin, TextSourceAdmin, 
                ShelveAdmin, DictBasedCardWriter
    )
from src.clss.cardDeliverers import SeleniumAnkiBot

phrases_file = 'frases.txt'
file_path = os.path.join(os.getcwd(), phrases_file)

login_file = 'data.json'
login_path = os.path.join(os.getcwd(), login_file)


#deliver = SeleniumAnkiBot(Firefox, 'login.txt')
deliver = SeleniumAnkiBot(Chrome, login_path)
writer = DictBasedCardWriter()
sourceAdmin = TextSourceAdmin(file_path, writer)
dbAdmin = ShelveAdmin('db_cards', 'cards')

ac = AutoFlashCards(deliver, sourceAdmin, dbAdmin)

if __name__ == "__main__":
    ac.run_task()
    if len(ac.card_list) == 0:
        print('No cards to create.')
