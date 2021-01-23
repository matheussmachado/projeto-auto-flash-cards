from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class Bot:
    def __init__(self, drive, **options):
        self.drive = drive
        self.options = options
        self.bot = None
        self.bot = self.drive(**self.options)
        url = 'https://stackoverflow.com'
        self.bot.get(url)
        self.bot.maximize_window()
        
    def get_page_source(self):
        p = self.bot.page_source
        return p


drive = Chrome
op = Options()
op.headless = False

drive_op = {
    "options": op,
    "executable_path": ChromeDriverManager().install()
}

#bot = Bot(drive, **drive_op)

#bot = Bot(drive)
#print(bot.get_page_source())
