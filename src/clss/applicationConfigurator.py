import os
from importlib import import_module
from src.funcs.textFunc import get_from_json
from src.clss.error import DataConfigError



class appConfigurator:
    def __init__(self, configurated_file_path: str):
        self.config_file = configurated_file_path
        self.key = "application_file_name"
        self.app_config = get_from_json(self.config_file, self.key)
    
    def import_app(self, package_name_path: str) -> 'Module':
        """
        package_name: deve ser obtido como os.path.join('pkg', 'supkg')
        """
        module_name = package_name_path.replace(os.sep, ".")
        try:
            app = import_module(f'{module_name}.{self.app_config}')
        except ModuleNotFoundError:
            raise DataConfigError
        return app
