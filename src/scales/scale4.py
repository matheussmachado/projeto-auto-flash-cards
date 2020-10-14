#!venv/bin/python3
import os
import re

from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.chrome.options import Options

from src.clss.autoFlashCards import AutoFlashCards
from src.clss.assistants import AnkiEditPageHandler
from src.clss.cardDeliverers import SeleniumAnkiBot
from src.clss.cardWriter import DictBasedCardWriter
from src.clss.imageSources import GoogleDriveSource
from src.clss.TextExtractors import GoogleVision
from src.clss.sourceAdmins import ImageSourceAdmin
from src.clss.sourceAdmins import MyCardShelveAdmin
from src.clss.sourceAdmins import DriveFileIdShelveAdmin


user_data_file = os.path.join(os.getcwd(), 'data.json')
drive_folder_target = 'Legendas'

writer = DictBasedCardWriter()
id_admin = DriveFileIdShelveAdmin('db', 'drive_file_id')
img_source = GoogleDriveSource(drive_folder_target, id_admin)
text_extractor = GoogleVision()

#driver = Firefox
driver = Chrome
web_driver_options = Options()
web_driver_options.headless = False
web_driver_args = {
	"options": web_driver_options
}
web_edit_page_handler = AnkiEditPageHandler(re)
selenium_anki_bot_args = {
    'web_driver': driver, 
    'user_data': user_data_file,
    'web_edit_page_handler': web_edit_page_handler,
}
deliver = SeleniumAnkiBot(**selenium_anki_bot_args, **web_driver_args)

img_admin = ImageSourceAdmin(img_source, writer, text_extractor)
db = MyCardShelveAdmin('db', 'cards')

automaton = AutoFlashCards(deliver, img_admin, db)
