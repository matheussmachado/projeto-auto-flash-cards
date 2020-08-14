#!venv/bin/python3

import os

from selenium.webdriver import Firefox

from src.clss.autoFlashCards import AutoFlashCards
from src.clss.cardDeliverers import SeleniumAnkiBot
from src.clss.cardWriter import DictBasedCardWriter
from src.clss.imageSources import OcamlfuseSource
from src.clss.TextExtractors import GoogleVision
from src.clss.sourceAdmins import ImageSourceAdmin
from src.clss.sourceAdmins import ShelveCardAdmin

from src.funcs.textFunc import get_from_txt

path = os.path.join(os.getcwd(), 'data.json')
folder_path = login_path = path

writer = DictBasedCardWriter()
img_source = OcamlfuseSource('Legendas')
text_extractor = GoogleVision()

deliver = SeleniumAnkiBot(Firefox, login_path)
img_admin = ImageSourceAdmin(img_source, writer, text_extractor)
db = ShelveCardAdmin('db', 'cards')

automaton = AutoFlashCards(deliver, img_admin, db)

if __name__ == "__main__":
    automaton.run_task()
    if len(automaton.card_list) == 0:
        print('No cards to create.')
