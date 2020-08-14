import shutil
import os
import io
from typing import List

from .interfaces import ImageSourceInterface
from .sourceAdmins import ShelveIdAdmin
from src.funcs.imgFuncs import get_imgs_path, remove_imgs_list
from src.funcs.textFunc import get_from_json
from drive import (
    create_drive_folder, delete_file_by_id, get_data_files_from_folder, get_id_by_folder_name, get_images_byte
    )



class OcamlfuseSource(ImageSourceInterface):    
    _LOCAL_PATH = 'imgPath'

    def __init__(self, drive_folder_name: str):
        self.folder_target = drive_folder_name
    
        
    @property
    def _total_path(self) -> str:
        return self._return_mount_folder()

    def _return_mount_folder(self) -> str:
        if not self._LOCAL_PATH in os.listdir(os.getcwd()):
            try:
                os.mkdir(self._LOCAL_PATH)
            except Exception as err:
                print(err)
            else:
                os.system(f'google-drive-ocamlfuse {self._LOCAL_PATH}')
        return os.path.join(self._LOCAL_PATH, self.folder_target)
    
    def get_images(self) -> List[str]:
        imgs_data = []
        paths = get_imgs_path(self._total_path)
        for path in paths:
            with io.open(path, 'rb') as image_file:
                _bytes = image_file.read()
            imgs_data.append(
                {'bytes': _bytes, 'source': path}
            )
        return imgs_data

    def remove_images(self, imgs_path: List[str]) -> None: 
        remove_imgs_list(imgs_path)
        os.system(f'fusermount -u {self._LOCAL_PATH}')
        if not self.folder_target in os.listdir(self._LOCAL_PATH):
            try:
                os.rmdir(self._LOCAL_PATH)
            except Exception as err:
                print(err)



class GoogleDriveSource(ImageSourceInterface):
    def __init__(self, drive_folder_name, 
    id_admin: ShelveIdAdmin):
        self.folder = drive_folder_name
        self.id_admin = id_admin
        self._failed_rm_id = None
    
    @property
    def failed_rm_id(self):
        if self._failed_rm_id == None:
            self._failed_rm_id = self.id_admin.return_sources()
        return self._failed_rm_id


    def get_images(self):
        imgs_data = []
        _id = get_id_by_folder_name(self.folder)
        if not _id:
            raise Exception(f'{self.folder} folders not exists.')
        imgs_id = get_data_files_from_folder(_id)
        for data_id in imgs_id:
            if data_id in self.failed_rm_id:
                continue
            _bytes = get_images_byte(data_id)
            if _bytes:
                imgs_data.append(
                {'bytes': _bytes, 'source': data_id}
            )
        return imgs_data
    
    def remove_images(self, data_list: list) -> None:
        data_list.extend(self.failed_rm_id)
        failed = []
        for _id in data_list:
            removed = delete_file_by_id(_id)
            if not removed:
                failed.append(_id)
        self.id_admin.update_sources(failed)
