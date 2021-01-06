from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

class Bot:
    def __init__(self, drive, **options):
        self.drive = drive
        self.options = options
        self.bot = None
        
    def get_page_source(self):
        self.bot = self.drive(**self.options)
        url = 'https://stackoverflow.com'
        self.bot.get(url)
        p = self.bot.page_source
        return p


drive = Chrome
op = Options()
op.headless = True

drive_op = {
    "options": op
}

bot = Bot(drive, **drive_op)
#bot = Bot(drive)
print(bot.get_page_source())
