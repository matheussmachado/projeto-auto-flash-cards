import os
from typing import List


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
