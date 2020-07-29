import os

from selenium.webdriver import Firefox

from src.clss.autoCards import AutoCards
from src.clss.sourceAdmins import (
    DataBaseAdmin, TextSourceAdmin, DataBaseAdmin, DictBasedCardWriter
    )
from src.clss.cardDeliverers import SeleniumAnkiBot

file = 'frases.txt'
file_path = os.path.join(os.getcwd(), file)

deliver = SeleniumAnkiBot(Firefox, 'login.txt')
writer = DictBasedCardWriter()
sourceAdmin = TextSourceAdmin(file_path, writer)

ac = AutoCards(deliver, sourceAdmin)

if __name__ == "__main__":
    ac.run_task()
