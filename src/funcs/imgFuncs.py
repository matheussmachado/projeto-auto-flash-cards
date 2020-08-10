import os
from typing import List
import pickle

from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request


def get_imgs_path(folder_path: str) -> List[str]:
    if not os.path.isdir(folder_path):
        print(f'"{folder_path}" não é um diretório.')
    files = []
    for file in os.listdir(folder_path):
        if file.endswith(".png") or file.endswith(".jpg"):
            files.append(os.path.join(folder_path, file))
    return files



def remove_imgs_list(imgs_list: List[str]) -> None:
    for img_path in imgs_list:
        if os.path.isfile(img_path) and (
            img_path.endswith(".png") or 
            img_path.endswith(".jpg")
        ):
            os.unlink(img_path)



def Create_Service(client_secret_file, api_name, api_version, *scopes):    
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]    

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

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
