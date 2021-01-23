#!venv/bin/python3

import os

from src.clss.autoFlashCards import AutoFlashCards
from src.clss.webDriverConfigurator import WebDriverConfigurator
from src.clss.cardDeliverers import SeleniumAnkiBot
from src.clss.cardWriter import DictBasedCardWriter
from src.clss.imageSources import LocalFolderSource
from src.clss.TextExtractors import GoogleVision
from src.clss.sourceAdmins import ImageSourceAdmin
from src.clss.sourceAdmins import MyCardShelveAdmin

from . import CONFIG_FILE



path = os.path.join(os.getcwd(), 'data.json')
folder_path = login_path = path

writer = DictBasedCardWriter()
img_source = LocalFolderSource(CONFIG_FILE)
text_extractor = GoogleVision()

wdconfig = WebDriverConfigurator(CONFIG_FILE)
selenium_anki_bot_args = {
    'web_driver_settings': wdconfig.config_settings(), 
    'user_data': CONFIG_FILE
}
deliver = SeleniumAnkiBot(**selenium_anki_bot_args)

#deliver = SeleniumAnkiBot(Firefox, login_path)
img_admin = ImageSourceAdmin(img_source, writer, text_extractor)
db = MyCardShelveAdmin('db', 'cards')

automaton = AutoFlashCards(deliver, img_admin, db)

if __name__ == "__main__":
    automaton.run_task()
    if len(automaton.card_list) == 0:
        print('No cards to create.')
