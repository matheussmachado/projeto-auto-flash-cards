from typing import List
from src.funcs.imgFuncs import get_imgs_path, remove_imgs_list
from src.funcs.textFunc import get_from_json


class MockImageSource:
    def __init__(self, img_path_file: str):
        self.source = get_from_json(img_path_file, 'imgPath')
    
    def get_images(self) -> List[str]:        
        imgs_data = []
        paths = get_imgs_path(self.source)
        for path in paths:            
            _bytes = bytes(path, encoding='utf-8')
            imgs_data.append(
                {'bytes': _bytes, 'source': path}
            )
        return imgs_data

    def remove_images(self, img_list: List[str]) -> None:
        ...


class MockWebDriverConfigurator:
    def __init__(self):
        self._user_settings = None
        self.web_driver_settings = {
            "web_driver_args": {}
        }

    def _mock_install_driver_handler(self):
        install = self._user_settings["auto_executable_path"]
        if not install:
            return
        driver_collections = {
            "chrome": "ChromeDriverManager"
        }
        browser = self._user_settings["browser"]
        driver_manager = driver_collections.get(browser)
        exec(f"from webdriver_manager.{browser} import {driver_manager}")
        mock_driver_manager = {"manager": None}
        exec(f"mock_driver_manager['manager'] = {driver_manager}")
        path = '/home/user/.wdm/drivers/chromedriver/plataform/chromedriver_version/chromedriver'
        self.web_driver_settings["web_driver_args"].update(executable_path=path)
        return mock_driver_manager["manager"]


class MockGoogleVision:
    def img_to_str(self, img: bytes) -> None:
        ...
    
