import os
import io
from typing import Union, Dict, List
import pickle

from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

#from src.funcs.imgFuncs import Create_Service


#---------------------- GOOGLE DRIVE ----------------------
SCOPES = ['https://www.googleapis.com/auth/drive']
KEY = 'client_drive_key.json'
API_NAME = 'drive'
API_VERSION = 'v3'

#DOWNLOAD DAS IMAGENS
def get_images_byte(file_id):    
    try:
        request = service.files().get_media(fileId=file_id)
    except HttpError as err:
        print(err)
    else:
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)
        done = False
        while not done:
            status, done = downloader.next_chunk()            
        fh.seek(0)            
        img_bytes = fh.read()
        return img_bytes


#REMOVER id EM UM DIRETÓRIO
def delete_file_by_id(file_id):
    try:
        service.files().delete(fileId=file_id).execute()
    except HttpError as error:
        print('An error occurred: %s' % error)
    else:
        return True


#TODO: OBTER TODOS OS id's DAS IMAGENS DE UM DIRETÓRIO
def get_data_files_from_folder(folder_id):
    page_token = None
    while True:
        response = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",            
            spaces='drive',
            fields='nextPageToken, files(id)',
            pageToken=page_token
            ).execute()        
        result = response.get('files', [])
        data_ids = [d['id'] for d in result]
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return data_ids



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



def create_service(client_secret_file, api_name, api_version, *scopes):    
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    cred = None
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()
        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)        
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

#ENCAPSULAR ISSO DENTRO DE UMA FUNÇÃO E TRATAR A CHAMADA
'''
service = create_service(KEY, API_NAME, API_VERSION, SCOPES)
if not service:
    raise Exception('Unable to create the Google Drive service')
'''

if __name__ == "__main__":
    #get_drive_folder_id('Legendas')
    #create_drive_folder('Teste')
    img = get_data_files_from_folder(get_id_by_folder_name('Legendas'))
    print(img)
    
