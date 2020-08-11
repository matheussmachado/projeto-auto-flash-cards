import os
import io
from typing import List

from google.cloud import vision
from google.cloud.vision import types

from .interfaces import TextExtractorInterface


class GoogleVision(TextExtractorInterface):
    _AUTH_FILE = 'serviceAccountToken.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = _AUTH_FILE

    def __init__(self):
        self._client = vision.ImageAnnotatorClient()        

    #def img_to_str(self, img_path: str) -> List[str]:
    def img_to_str(self, img: bytes) -> List[str]:
        image = vision.types.Image(content=img)
        response = self._client.text_detection(image=image)
        texts = response.text_annotations
        text = texts[0].description
        text = text.replace('\n', ' ').strip()
        return text
