import os
import sys
SOURCE_FOLDER = os.path.join(os.getcwd(), 'src', 'clss', 'autoCards')
sys.path.insert(0, SOURCE_FOLDER)

from src.clss.autoCards import AutoCards
'''from src.clss.autoCards import AutoCards
from src.clss.sourceAdmins import (
    DataBaseAdmin, TextSourceAdmin, DataBaseAdmin)
from src.clss.cardDeliverers import SeleniumAnkiBot'''


file = 'frases.txt'
folder = '..'
print(os.path.join(folder, file))
print(sys.path)

