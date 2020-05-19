import unittest
from src.classes import AutoDeck
from src.funcs import get_from_file

#UMA CLASSE TESTE POR CLASSE E POR FUNÇÃO

class TestGetFromFile(unittest.TestCase):
    
    def test_1(self):
        """
            TESTA SE É POSSÍVEL OBTER UMA LISTA CONTENDO STRINGS DE UM ARQUÍVO file DE EXTENSÃO .TXT. AS STRINGS DEVEM SER CONFORME AS FRASES CONTIDAS NA LISTA frases.
        """
        frases = [
            'Take this time, Francis, to know your other attendees.',
            "Tell me you're not peddling influence with your wife?",
            'The Russian research vessel.',
            "Let's reconvene when you know more."
        ]
        file = 'frasesTestePreenchida.txt'
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
        """
            TESTA SE É POSSÍVEL OBTER UMA LISTA DE OBJETOS AutoCard, SENDO ESTA LISTA O ATRIBUTO cards DO OBJETO AutoDeck. O PARÂMETRO front É O ATRIBUTO DE AutoCard QUE POSSUI A STRING CONTEÚDO DO ARQUIVO file. NO CASO, cards É A LISTA CONTENDO ASA STRINGS DE front."""
        file = 'frasesTestePreenchida.txt'
        cards = [card.front for card in self.deck.get_cards(file)]
        self.assertEqual(self.frases, cards)

    
    #Testa se get_cards retorna None caso o file não tiver frases
    def test_get_cards_2(self):
        file = 'frasesTesteVazia.txt'
        cards = self.deck.get_cards(file)
        self.assertIsNone(cards)


if __name__== '__main__':
    unittest.main()
