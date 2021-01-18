import os

from src.clss.webDriverConfigurator import WebDriverConfigurator
from src.clss.assistants import AnkiEditPageHandler
from src.clss.autoFlashCards import AutoFlashCards
from src.clss.cardDeliverers import SeleniumAnkiBot
from src.clss.sourceAdmins import (
                MyCardShelveAdmin, TextSourceAdmin, 
                DictBasedCardWriter
    )

from src.funcs.textFunc import get_from_json

from . import CONFIG_FILE

file_path = get_from_json(CONFIG_FILE, "phrasesFile")

wdconfig = WebDriverConfigurator(CONFIG_FILE)
writer = DictBasedCardWriter()
sourceAdmin = TextSourceAdmin(file_path, writer)
dbAdmin = MyCardShelveAdmin('db', 'cards')

selenium_anki_bot_args = {
    'web_driver_settings': wdconfig.config_settings(), 
    'user_data': CONFIG_FILE
}

deliver = SeleniumAnkiBot(**selenium_anki_bot_args)

automaton = AutoFlashCards(deliver, sourceAdmin, dbAdmin)
