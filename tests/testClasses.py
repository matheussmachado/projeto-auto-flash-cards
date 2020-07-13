import sys
from myPaths import SOURCE_PATH, SAMPLE_FOLDER 
sys.path.insert(0, SOURCE_PATH)

import unittest
from src.classes import AutoCards, AnkiBot, ContextManager,TextSourceAdmin, DataBaseAdmin
from src.funcs import os


class TestTextSourceAdmin(unittest.TestCase):

    def setUp(self):
        self.file = os.path.join(SAMPLE_FOLDER, 'frasesTestePreenchidaWriter.txt')


    def test_upadate_source(self):
        ...

class TestContextManager(unittest.TestCase):

    def setUp(self):
        self.frases = [
            "Take this time, Francis, to know your other attendees.",
            "Tell me you're not peddling influence with your wife?",
            "The Russian research vessel.",
            "Let's reconvene when you know more."
        ]
        self.source = os.path.join(SAMPLE_FOLDER, 'frasesTestePreenchida.txt')
    
    def test_writer_1(self):
        manager = ContextManager('text', self.source)
        #manager.write()
        manager.create_card()
        cards_front = [card.front for card in manager.cards]
        self.assertEqual(cards_front, self.frases)



#TODO: TESTE do AnkiBot e suas interações com a web



if __name__== '__main__':
    unittest.main()
