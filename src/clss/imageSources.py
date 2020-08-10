import os
import io
from typing import List
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
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
        folder_files = os.listdir(self._path)
        if not self._FOLDER_TARGET in folder_files:
            os.system(f'google-drive-ocamlfuse {self._path}')
        return os.path.join(self._path, self._FOLDER_TARGET)
    
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
        os.system(f'fusermount -u {self._path}')




class GoogleDrive(ImageSourceInterface):
    SCOPE = 'https://www.googleapis.com/auth/drive'
    KEY = 'client_drive_key.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'


"""class GoogleDrive(ImageSourceInterface):    

    SCOPES = 'https://www.googleapis.com/auth/drive.readonly.metadata'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
        creds = tools.run_flow(flow, store)
    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

    files = DRIVE.files().list().execute().get('files', [])
    for f in files:
        print(f['name'], f['mimeType'])"""
