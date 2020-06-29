import unittest
from src.classes import AutoCards, AnkiBot
from src.funcs import os, get_from_txt, remove_imgs_list
print()
get_from_txt()

#UMA CLASSE TESTE POR CLASSE E POR FUNÇÃO

class TestGetFromTxt(unittest.TestCase):
    
    def test_get_from_txt_1(self):
        """l
            TESTA SE É POSSÍVEL OBTER UMA LISTA CONTENDO STRINGS DE UM ARQUÍVO file DE EXTENSÃO .TXT. AS STRINGS DEVEM SER CONFORME AS FRASES CONTIDAS NA LISTA frases."""
        frases = [
            'Take this time, Francis, to know your other attendees.',
            "Tell me you're not peddling influence with your wife?",
            'The Russian research vessel.',
            "Let's reconvene when you know more."
        ]
        
        file = os.path.join('amostras', 'frasesTestePreenchida.txt')        
        phrases = get_from_txt(file)
        self.assertEqual(phrases, frases)           
   


class TestRemoveImgs(unittest.TestCase):

    def test_1(self):
        path = os.path.join('.', 'imgFolderTest')
        lista = [os.path.join(path, img) for img in os.listdir(path) 
                if img.endswith('.png') or img.endswith('.jpg')
        ]
        remove_imgs_list(lista)
        imgs = [img for img in os.listdir(path) 
                if (img.endswith('.png') or img.endswith('.jpg'))]
        self.assertEqual(len(imgs), 0)
        

class TestAutoCards(unittest.TestCase):
    
    def setUp(self):
        self.autoCard = AutoCards()
        self.frases_txt = [
            "Take this time, Francis, to know your other attendees.",
            "Tell me you're not peddling influence with your wife?",
            "The Russian research vessel.",
            "Let's reconvene when you know more."
        ]
        self.frases_img = [
            '', '', '', ''
        ]
        self.img_names = [  
            'img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg',
        ]
    
    def test_gen_cards_txt_1(self):
        """
            TESTA SE É POSSÍVEL OBTER UMA LISTA DE OBJETOS FlashCard, SENDO ESTA LISTA O ATRIBUTO cards DO OBJETO AutoCards. O PARÂMETRO front É O ATRIBUTO DE FlashCard QUE POSSUI A STRING CONTEÚDO DO ARQUIVO file. NO CASO, cards É A LISTA CONTENDO ASA STRINGS DE front."""
        file = os.path.join('amostras', 'frasesTestePreenchida.txt')    
        cards = [card.front for card in self.autoCard.gen_cards_txt(file)]
        self.assertEqual(self.frases_txt, cards)

    
    def test_gen_cards_txt_2(self):
        file = os.path.join('amostras', 'frasesTesteVazia.txt')
        self.autoCard.gen_cards_txt(file)
        self.assertEqual(len(self.autoCard.cards), 0)


class TestAnkiBot(unittest.TestCase):

    def setUp(self):
        self.bot = AnkiBot()
        self.frases = os.path.join('amostras', 'frasesTesteVazia.txt')

    #VERIFICA se retorna None caso o parâmetro errado for passado, abortando o início do bot.
    def test_start_1(self):
        self.assertIsNone(
            self.bot.start(gen_type='txt', source=self.frases)
            )


#TODO: TESTE do AnkiBot e suas interações com a web

if __name__ == '__main__':
    unittest.main()
