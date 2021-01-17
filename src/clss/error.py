class DataConfigError(Exception):
    def __init__(self, data=""):
        text = "Configuration data not provided."
        if data:
            text = f"Configuration data '{data}' incorrect."
        MESSAGE = f"{text} Please check the config.json file in the application's root directory."
        super().__init__(MESSAGE)
       