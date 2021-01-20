import os
from importlib import import_module
from src.funcs.textFunc import get_from_json
from src.clss.error import DataConfigError



class appConfigurator:
    def __init__(self, config_file_path: str):
        self.app_config = get_from_json(config_file_path, "application_file_name")
    
    def import_app(self, package_name_path: str) -> 'Python Module':
        """
        package_name: deve ser obtido como os.path.join('pkg', 'supkg')
        """
        module_name = package_name_path.replace(os.sep, ".")
        try:
            app = import_module(f'{module_name}.{self.app_config}')
        except ModuleNotFoundError:
            raise DataConfigError(self.app_config)
        return app
