"""DEVE HAVER NA RAIZ DO PROJETO O ARQUIVO serviceAccountToken.json, COMO MENCIONADO NA DOCUMENTAÇÃO, PARA PODER RODAR ESSES TESTES
"""
import os
import io
from unittest import TestCase, mock, main
from src.clss.TextExtractors import GoogleVision
from src.clss.mocks import MockImageSource
from src.clss.cardWriter import DictBasedCardWriter
from src.clss.sourceAdmins import ImageSourceAdmin

from . import SAMPLE_FOLDER, IMG_FOLDER

imgs_path = os.path.join(SAMPLE_FOLDER, IMG_FOLDER)


class TestGoogleVision(TestCase):
    @mock.patch('src.clss.TextExtractors.vision.ImageAnnotatorClient.text_detection')
    def test_text_detection_of_vision_api_was_called(self, mocked):
        img = os.path.join(imgs_path, 'img1.jpg')
        extractor = GoogleVision()
        with io.open(img, 'rb') as f:
            content = f.read()
        extractor.img_to_str(content)
        mocked.assert_called_once()



class TestImageSourceAdmin(TestCase):
    def setUp(self):
        path = os.path.join(SAMPLE_FOLDER, 'config(sample).json')
        self.mockImgSource = MockImageSource(path)
        self.writer = DictBasedCardWriter()


    @mock.patch('src.clss.TextExtractors.vision.ImageAnnotatorClient.text_detection')       
    def test__return_source_method_call_text_detection_method(self, mocked):
        extractor = GoogleVision()
        imgAdmin = ImageSourceAdmin(self.mockImgSource, self.writer, extractor)
        imgAdmin.return_sources()
        expected = mocked.call_count
        self.assertEqual(expected, 2)


if __name__ == "__main__":
    main()