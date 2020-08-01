from typing import List
from src.funcs.imgFuncs import get_imgs_path, remove_imgs_list
from src.funcs.textFunc import get_from_json


class MockImageSource:
    def __init__(self, img_path_file: str):
        self.source = get_from_json(img_path_file, 'imgPath')
    
    def get_images(self) -> List[str]:
        return get_imgs_path(self.source)

    def remove_images(self, img_list: List[str]) -> None:
        ...
