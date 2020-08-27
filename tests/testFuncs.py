import os
from unittest import TestCase, main, mock

from src.funcs.textFunc import get_from_txt
from src.funcs.imgFuncs import get_imgs_path, remove_imgs_list

from . import SAMPLE_FOLDER, IMG_FOLDER

imgs_path = os.path.join(SAMPLE_FOLDER, IMG_FOLDER)

class TestGetFromTxt(TestCase):
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


class TestGetImgsName(TestCase):
    def test__returns_all_two_imgs_path(self):
        
        imgs_name = get_imgs_path(imgs_path)
        expected = len(imgs_name)
        self.assertEqual(expected, 2)

        expected_names = [
            os.path.join(imgs_path, 'img1.jpg'), 
            os.path.join(imgs_path, 'img2.jpg')
            ]
        self.assertEqual(expected_names, imgs_name)



class TestRemoveImgs(TestCase):
    @mock.patch('src.funcs.imgFuncs.os.unlink')
    def test__remove_all_two_imgs(self, mocked):        
        imgs_list = get_imgs_path(imgs_path)
        remove_imgs_list(imgs_list)
        expected = mocked.call_count
        self.assertEqual(expected, 2)



if __name__ == "__main__":
    main()
