import unittest
from src.funcs import get_from_txt, remove_imgs_list, os
from src.classes import MyCard

SAMPLE_FOLDER = 'amostras/'

class TestGetFromTxt(unittest.TestCase):
    
    def test_obtained_phrases(self):
        """
            TESTA SE É POSSÍVEL OBTER UMA LISTA CONTENDO STRINGS DE UM ARQUÍVO file DE EXTENSÃO .TXT. AS STRINGS DEVEM SER CONFORME AS FRASES CONTIDAS NA LISTA frases."""
        frases = ["The Russian research vessel."
            "Take this time, Francis, to know your other attendees.",
            "Tell me you're not peddling influence with your wife?",
            "The Russian research vessel.",
            "Let's reconvene when you know more."
        ]        
        file = 'frasesTestePreenchida.txt'
        path = os.path.join(SAMPLE_FOLDER, file)
        phrases = get_from_txt(path)
        self.assertEqual(phrases, frases)        
    

class TestCardRepresentation(unittest.TestCase):

    def setUp(self):
        self.file = 'frasesTestePreenchida.txt'
        self.path = os.path.join(SAMPLE_FOLDER, self.file)
        self.front = get_from_txt(self.path)[0]

    def test_card_represent_equals_to_a_card_attributes(self):
        myCard = MyCard(self.front, self.path)
        


'''class TestRemoveImgs(unittest.TestCase):

    def test_1(self):
        path = 'imgFolderTest'
        lista = [os.path.join('..', path, img) for img in os.listdir(path) 
                if img.endswith('.png') or img.endswith('.jpg')
        ]
        remove_imgs_list(lista)
        imgs = [img for img in os.listdir(path) 
                if (img.endswith('.png') or img.endswith('.jpg'))]
        self.assertEqual(len(imgs), 0)'''


if __name__ == '__main__':
    unittest.main()