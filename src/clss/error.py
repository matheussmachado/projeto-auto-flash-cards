class DataConfigError(Exception):
    def __init__(self):
        MESSAGE = "Configuration data not provided or incorrect. Please check the config.json file in the application's root directory."
        super().__init__(MESSAGE)
       