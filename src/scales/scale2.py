import os
import re

from selenium.webdriver import Firefox, Chrome, Opera
#from selenium.webdriver.opera.options import Options
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.firefox.options import Options

from src.clss.webDriverConfigurator import WebDriverConfigurator
from src.clss.assistants import AnkiEditPageHandler
from src.clss.autoFlashCards import AutoFlashCards
from src.clss.cardDeliverers import SeleniumAnkiBot
from src.clss.sourceAdmins import (
                MyCardShelveAdmin, TextSourceAdmin, 
                DictBasedCardWriter
    )

phrases_file = 'frases.txt'
file_path = os.path.join(os.getcwd(), phrases_file)

user_data_file = 'data.json'
user_data = os.path.join(os.getcwd(), user_data_file)

wdconfig = WebDriverConfigurator(user_data)
writer = DictBasedCardWriter()
sourceAdmin = TextSourceAdmin(file_path, writer)
dbAdmin = MyCardShelveAdmin('db', 'cards')



#driver = Chrome
#driver = Firefox
#driver = Opera
#wdm = GeckoDriverManager()
#wdm = OperaDriverManager()
#options = Options()
#options.headless = False


web_edit_page_handler = AnkiEditPageHandler(re)
selenium_anki_bot_args = {
    'web_driver_settings': wdconfig.config_settings(), 
    'user_data': user_data,
    'web_edit_page_handler': web_edit_page_handler,
}
#deliver = SeleniumAnkiBot(**selenium_anki_bot_args, **web_driver_args)
#deliver = SeleniumAnkiBot(web_driver_settings, user_data, web_edit_page_handler)
deliver = SeleniumAnkiBot(**selenium_anki_bot_args)

automaton = AutoFlashCards(deliver, sourceAdmin, dbAdmin)
