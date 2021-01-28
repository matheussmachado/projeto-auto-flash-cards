from src.clss.configurators import WebDriverConfigurator
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
    'webdriver_configurator': wdconfig, 
    'user_data': CONFIG_FILE
}

deliver = SeleniumAnkiBot(**selenium_anki_bot_args)

automaton = AutoFlashCards(deliver, sourceAdmin, dbAdmin)
