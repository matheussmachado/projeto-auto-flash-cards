#!venv/bin/python3
import os
import re

from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.firefox.options import Options


from src.clss.autoFlashCards import AutoFlashCards
from src.clss.assistants import AnkiEditPageHandler
from src.clss.cardDeliverers import SeleniumAnkiBot
from src.clss.cardWriter import DictBasedCardWriter
from src.clss.imageSources import GoogleDriveSource
from src.clss.TextExtractors import GoogleVision
from src.clss.sourceAdmins import ImageSourceAdmin
from src.clss.sourceAdmins import MyCardShelveAdmin
from src.clss.sourceAdmins import DriveFileIdShelveAdmin


path = os.path.join(os.getcwd(), 'data.json')
folder_path = login_path = path
drive_folder_target = 'Legendas'

writer = DictBasedCardWriter()
id_admin = DriveFileIdShelveAdmin('db', 'drive_file_id')
img_source = GoogleDriveSource(drive_folder_target, id_admin)
text_extractor = GoogleVision()

#driver = Firefox
driver = Chrome
#driver_options = Options()
driver_options = None
#driver_options.headless = True
#driver_options.headless = False
handler = AnkiEditPageHandler(re)
deck_name = 'Teste'
new_deck = True
deliver = SeleniumAnkiBot(
                            web_driver=driver, 
                            login_path=login_path,
                            deck_name=deck_name,
                            web_edit_page_handler=handler,
                            web_driver_options=driver_options,
                            new_deck=new_deck
                            )

img_admin = ImageSourceAdmin(img_source, writer, text_extractor)
db = MyCardShelveAdmin('db', 'cards')

automaton = AutoFlashCards(deliver, img_admin, db)
