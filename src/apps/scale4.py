from src.clss.webDriverConfigurator import WebDriverConfigurator
from src.clss.autoFlashCards import AutoFlashCards
from src.clss.cardDeliverers import SeleniumAnkiBot
from src.clss.cardWriter import DictBasedCardWriter
from src.clss.imageSources import GoogleDriveSource
from src.clss.TextExtractors import GoogleVision
from src.clss.sourceAdmins import ImageSourceAdmin
from src.clss.sourceAdmins import MyCardShelveAdmin
from src.clss.sourceAdmins import DriveFileIdShelveAdmin

from . import CONFIG_FILE

#drive_folder_target = 'Legendas'

wdconfig = WebDriverConfigurator(CONFIG_FILE)
writer = DictBasedCardWriter()
id_admin = DriveFileIdShelveAdmin('db', 'drive_file_id')
img_source = GoogleDriveSource(CONFIG_FILE, id_admin)
text_extractor = GoogleVision()

selenium_anki_bot_args = {
    'web_driver_settings': wdconfig.config_settings(), 
    'user_data': CONFIG_FILE
}
deliver = SeleniumAnkiBot(**selenium_anki_bot_args)

img_admin = ImageSourceAdmin(img_source, writer, text_extractor)
db = MyCardShelveAdmin('db', 'cards')

automaton = AutoFlashCards(deliver, img_admin, db)
