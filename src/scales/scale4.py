#!venv/bin/python3

import os
import re

from selenium.webdriver import Chrome

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
handler = AnkiEditPageHandler(re)

deliver = SeleniumAnkiBot(
                            Chrome, 
                            login_path,
                            "my deck",
                            handler
                             )
img_admin = ImageSourceAdmin(img_source, writer, text_extractor)
db = MyCardShelveAdmin('db', 'cards')

automaton = AutoFlashCards(deliver, img_admin, db)
