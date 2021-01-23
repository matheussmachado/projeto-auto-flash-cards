import os

from src.clss.webDriverConfigurator import WebDriverConfigurator
from src.clss.assistants import AnkiEditPageHandler
from src.clss.autoFlashCards import AutoFlashCards
from src.clss.cardDeliverers import SeleniumAnkiBot
from src.clss.sourceAdmins import (
                MyCardShelveAdmin, TextSourceAdmin, 
                DictBasedCardWriter
    )

from . import CONFIG_FILE

wdconfig = WebDriverConfigurator(CONFIG_FILE)
writer = DictBasedCardWriter()
sourceAdmin = TextSourceAdmin(CONFIG_FILE, writer)
dbAdmin = MyCardShelveAdmin('db', 'cards')

selenium_anki_bot_args = {
    'web_driver_settings': wdconfig.config_settings(), 
    'user_data': CONFIG_FILE
}

deliver = SeleniumAnkiBot(**selenium_anki_bot_args)

automaton = AutoFlashCards(deliver, sourceAdmin, dbAdmin)
