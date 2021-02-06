from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

driver = Chrome()

_URL_LOGIN = 'https://ankiweb.net/account/login'
_URL_EDIT = 'https://ankiuser.net/edit/'

driver.get(_URL_LOGIN)

while True:
    if driver.current_url != _URL_LOGIN:
        break

driver.get(_URL_EDIT)

deck_locator = (By.CSS_SELECTOR, 'input[id="deck"]')

deck_element = driver.find_element(*deck_locator)

deck_element.clear()

deck_element.send_keys('tudo certo')

