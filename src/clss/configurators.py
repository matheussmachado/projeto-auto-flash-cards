import os
from importlib import import_module
from .interfaces import ConfiguratorInterface
from .error import DataConfigError
from src.funcs.textFunc import get_from_json



class AppConfigurator(ConfiguratorInterface):
    def __init__(self, config_file_path: str):
        self.app_config = get_from_json(config_file_path, "application_file_name")
    
    def configure(self, package_name_path: str) -> 'Python Module':
        """
        package_name: os.path.join('pkg', 'supkg')
        """
        module_name = package_name_path.replace(os.sep, ".")
        try:
            app = import_module(f'{module_name}.{self.app_config}')
        except ModuleNotFoundError:
            raise DataConfigError(self.app_config)
        return app



class WebDriverConfigurator(ConfiguratorInterface):
	def __init__(self, config_file_path: str):
		self._user_settings = get_from_json(
			config_file_path, 
			"web_driver_user_settings"
			)
		self.web_driver_settings = {
			"web_driver_args": {}
		}

	def _browser_import_handler(self):
		browser = self._user_settings["browser"].lower()
		try:
			module = import_module(f'selenium.webdriver.{browser}.webdriver')
		except ModuleNotFoundError:
			raise DataConfigError(browser)
		else:
			driver = module.WebDriver
			self.web_driver_settings.update(driver=driver)

	def _web_driver_options_handler(self):
		browser = self._user_settings["browser"]
		try:
			module = import_module(f'selenium.webdriver.{browser}.options')
		except ModuleNotFoundError:
			raise DataConfigError(browser)
		else:
			opt = module.Options()
			user_options = self._user_settings["web_driver_options"]
			for k, v in user_options.items():
				setattr(opt, k, v)
			self.web_driver_settings["web_driver_args"].update(options=opt)
	
	def _set_web_drive_args_handler(self):
		web_driver_args = self._user_settings["web_driver_args"]
		self.web_driver_settings["web_driver_args"].update(
			web_driver_args
		)
		
	def _install_driver_handler(self):
		auto_executable_path = self._user_settings["auto_executable_path"]
		if not auto_executable_path:
			return
		driver_collections = {
			"chrome": "ChromeDriverManager",
			"firefox": "GeckoDriverManager",
			"opera": "OperaDriverManager"
		}
		browser = self._user_settings["browser"]
		driver_manager_name = driver_collections.get(browser)
		try:
			module = import_module(f'webdriver_manager.{browser}')
		except ModuleNotFoundError:
			raise DataConfigError(browser)
		else:
			driver_manager = getattr(module, driver_manager_name)
			exe_path_installed = driver_manager().install()
			self.web_driver_settings["web_driver_args"].\
				update(executable_path=exe_path_installed)

	def config_settings(self) -> dict:
		for attr in dir(self):
			if 'handler' in attr:
				method = getattr(self, attr)
				method.__call__()
		return self.web_driver_settings

	def configure(self) -> 'Selenium WebDriver':
		settings = self.config_settings()
		driver = settings.get('driver')
		args = settings.get('web_driver_args')
		webdriver = driver(**args)
		bot = driver(**args)
		return bot
