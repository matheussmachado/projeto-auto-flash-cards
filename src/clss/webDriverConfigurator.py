from src.funcs.textFunc import get_from_json


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
		drive_import = self._user_settings["browser"].capitalize()
		exec(f"from selenium.webdriver import {drive_import}")
		exec(f"self.web_driver_settings.update(driver={drive_import})")

	def _web_driver_options_handler(self):
		browser = self._user_settings["browser"]
		exec(f"from selenium.webdriver.{browser}.options import Options")
		exec("opt = Options()")
		user_options = self._user_settings["web_driver_options"]
		for k, v in user_options.items():
			exec(f"opt.{k} = {v}")
		exec(
			f'self.web_driver_settings["web_driver_args"].update(options=opt)'
		)

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
		driver_manager = driver_collections.get(browser)
		exec(f"from webdriver_manager.{browser} import {driver_manager}")
		exec(f"exe_path_installed = {driver_manager}().install()")
		exec(
			f'''self.web_driver_settings["web_driver_args"].update(
					executable_path=exe_path_installed
			)'''
		)

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

