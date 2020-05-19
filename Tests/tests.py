import unittest
#from Classes.classes import AutoDeck
#from Functions.functions import get_from_file
from src.classes import AutoDeck
from src.funcs import get_from_file

#UMA CLASSE PARA TESTAR TODAS AS FUNÇÕES OU UMA CLASSE POR FUNÇÃO?
class TestGetFromFile(unittest.TestCase):
    
    def test_1(self):
        frases = [
            'Take this time, Francis, to know your other attendees.',
            "Tell me you're not peddling influence with your wife?",
            'The Russian research vessel.',
            "Let's reconvene when you know more."
        ]
        file = 'frasesTeste.txt'
        phrases = get_from_file(file)
        self.assertEqual(phrases, frases)        
    


class TestAutoDeck(unittest.TestCase):
    
    def setUp(self):
        self.deck = AutoDeck()
        self.frases = [
            "Take this time, Francis, to know your other attendees.",
            "Tell me you're not peddling influence with your wife?",
            "The Russian research vessel.",
            "Let's reconvene when you know more."
        ]
        
    def test_get_cards_1(self):
        file = 'frasesTeste.txt'
        cards = [card.front for card in self.deck.get_cards(file)]
        self.assertEqual(self.frases, cards)

    #TODO: Testar se o método get_cards obtém as frases de frasesTeste -> uma coleção de cards que chama as mesmas frases cumpre a mesma função de get_cards. TESTAR OS FRONT DOS CARDS OBTIDOS COM AS FRASES

    #TODO: Testar se get_cards retorna none caso o file não tiver frases

if __name__== '__main__':
    unittest.main()