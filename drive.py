import os
import io
from typing import Union, Dict, List
#from Google import Create_Service
from google.cloud import vision
from google.cloud.vision import types

from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from src.funcs.imgFuncs import Create_Service

_AUTH_FILE = 'serviceAccountToken.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = _AUTH_FILE

client = vision.ImageAnnotatorClient()


SCOPES = ['https://www.googleapis.com/auth/drive']
KEY = 'client_drive_key.json'
API_NAME = 'drive'
API_VERSION = 'v3'

service = Create_Service(KEY, API_NAME, API_VERSION, SCOPES)


#DOWNLOAD DAS IMAGENS
def download_files(local_folder, data_files):
    
    for file in data_files:
        try:
            request = service.files().get_media(fileId=file['id'])
        except HttpError as err:
            print(err)
        else:
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fd=fh, request=request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f'download progress {status.progress() * 100}')
            fh.seek(0)
            '''content = fh.read()
            image = vision.types.Image(content=content)
            response = client.text_detection(image=image)
            texts = response.text_annotations
            text = texts[0].description
            text = text.replace('\n', ' ').strip()
            print(text)'''
            '''with open(os.path.join(local_folder, file['name']), 'wb') as f:
                f.write(fh.read())'''



#REMOVER id EM UM DIRETÓRIO
def delete_file_by_id(file_id):
  try:
    service.files().delete(fileId=file_id).execute()
  except HttpError as error:
    print('An error occurred: %s' % error)


#TODO: OBTER TODOS OS id's DAS IMAGENS DE UM DIRETÓRIO
def get_data_files_from_folder(folder_id):
    page_token = None
    while True:
        response = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",            
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=page_token
            ).execute()        
        result = response.get('files', [])        
        print(result)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return result



#CRIAR O DIRETÓRIO
def create_drive_folder(folder_name: str) -> None:
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    service.files().create(body=file_metadata).execute()


#VALIDAÇÃO DA PASTA
def get_id_by_folder_name(folder_name: str) -> str:
    _id = ''
    page_token = None
    while True:
        response = service.files().list(
            q="mimeType='application/vnd.google-apps.folder'",
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=page_token,
            ).execute()        
        result = response.get('files', [])        
        file_names = [f['name'] for f in result]
        if folder_name in file_names:
            filtr = [
                f['id'] for f in result if f['name'] == folder_name
            ]
            _id = filtr[0]
        page_token = response.get('nextPageToken', None)                
        if page_token is None:
            break
    return _id



if __name__ == "__main__":
    #get_drive_folder_id('Legendas')
    #create_drive_folder('Teste')
    img = get_data_files_from_folder(get_id_by_folder_name('Legendas'))
    print(img)
    download_files('./imgFolder', img)
    #delete_file_by_id(get_id_by_folder_name('Teste'))

'''

#FLUXO DO IMAGESOURCE

- verificar se há o id
- verificar se há 



- verificar se há o campo id no arquivo data.json
    - se houver:
    Validar se há o diretório
        - se houver
            - obter o id; fim
        - se não,
            - criar o diretório
            - obter o id e gravar em data.json
            - finaliza
    - se não houver;
            - criar o diretório
            - obter o id e gravar em data.json na key id


- verificar se há o id da pasta em data.json:
    - se não houver;        
        - Validar se há o diretório
        - se houver
            - obter o id
        - se não,
            - criar o diretório
            - obter o id e gravar em data.json
'''
