import os
from typing import List
from .interfaces import ImageSourceInterface

from src.funcs.imgFuncs import get_imgs_path, remove_imgs_list
from src.funcs.textFunc import get_from_json

class OcamlfuseSource(ImageSourceInterface):
    _FOLDER_TARGET = 'Legendas'

    def __init__(self, data_path: str):        
        self._path = get_from_json(data_path, 'imgPath')
        
    @property
    def _total_path(self) -> str:
        return self._return_mount_folder()

    def _return_mount_folder(self) -> str:
        
        if not self._FOLDER_TARGET in os.listdir(self._path):
            os.system(f'google-drive-ocamlfuse {self._path}')
        return os.path.join(self._path, self._FOLDER_TARGET)
    
    def get_images(self) -> List[str]:
        return get_imgs_path(self._total_path)
        
    def remove_images(self, imgs_path: List[str]) -> None:
        remove_imgs_list(imgs_path)    
        os.system(f'fusermount -u {self._path}')
