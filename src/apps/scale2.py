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

#TODO: remover a operação abaixo após implementar a mesma pela configuração de escala
"""
phrases_file = 'frases.txt'
file_path = os.path.join(os.getcwd(), phrases_file)"""

file_path = get_from_json(CONFIG_FILE, "phrasesFile")

#TODO: remover essa parte após refatorar o WebDriverConfigurator
user_data_file = 'config.json'
user_data = os.path.join(os.getcwd(), user_data_file)

wdconfig = WebDriverConfigurator(user_data)
writer = DictBasedCardWriter()
sourceAdmin = TextSourceAdmin(file_path, writer)
dbAdmin = MyCardShelveAdmin('db', 'cards')

selenium_anki_bot_args = {
    'web_driver_settings': wdconfig.config_settings(), 
    'user_data': user_data
}

deliver = SeleniumAnkiBot(**selenium_anki_bot_args)

automaton = AutoFlashCards(deliver, sourceAdmin, dbAdmin)
