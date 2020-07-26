import unittest
from unittest.mock import patch
from src.funcs import get_from_txt, img_to_txt, os, testando, vision_api_call
from src.classes import MyCard

SAMPLE_FOLDER = "amostras/"


class TestGetFromTxt(unittest.TestCase):
    def test_obtained_phrases(self):
        """
            TESTA SE É POSSÍVEL OBTER UMA LISTA CONTENDO STRINGS DE UM ARQUÍVO file DE EXTENSÃO .TXT. AS STRINGS DEVEM SER CONFORME AS FRASES CONTIDAS NA LISTA frases."""
        frases = [            
            "Take this time, Francis, to know your other attendees.",
            "Tell me you're not peddling influence with your wife?",
            "The Russian research vessel.",
            "Let's reconvene when you know more.",
        ]
        file = "frasesTestePreenchida.txt"
        path = os.path.join(SAMPLE_FOLDER, file)
        phrases = get_from_txt(path)
        self.assertEqual(phrases, frases)


'''class TestRemoveImgs(unittest.TestCase):
    def setUp(self):
        self.path = SAMPLE_FOLDER

    def test_remove_all_imgs_of_folder(self):
        path = 'imgFolderTest'
        lista = [os.path.join('..', path, img) for img in os.listdir(path) 
                if img.endswith('.png') or img.endswith('.jpg')
        ]
        remove_imgs_list(lista)
        imgs = [img for img in os.listdir(path) 
                if (img.endswith('.png') or img.endswith('.jpg'))]
        self.assertEqual(len(imgs), 0)'''


class TestImgtoTxt(unittest.TestCase):
    ...
#TODO: TESTAR SE O MÉTODO .text_detection FOI CHAMADA

    def setUp(self):
        self.image = os.path.join(SAMPLE_FOLDER, 'imgTeste.jpg')

    @patch('src.funcs.vision_api_call')
    def test_text_detection_of_vision_api_was_called(self, mocked):
        r = img_to_txt(self.image)
        mocked.assert_called_once()     


if __name__ == "__main__":
    unittest.main()
