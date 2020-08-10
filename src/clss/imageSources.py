import shutil
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
