from importlib import import_module
from src.funcs.textFunc import get_from_json
from src.clss.error import DataConfigError


class WebDriverConfigurator:
	def __init__(self, web_driver_user_settings: 'JSON File'):
		self._user_settings = get_from_json(
			web_driver_user_settings, 
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
		module = import_module(f'selenium.webdriver.{browser}.options')
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
		install = self._user_settings["auto_executable_path"]
		if not install:
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

	@property
	def install_path(self):
		yield _install_driver_handler()

	def config_settings(self):
		str_methods = [
			method for method in dir(self) 
			if 'handler' in method
		]
		for method in str_methods:
			exec(f"self.{method}()")
		return self.web_driver_settings

