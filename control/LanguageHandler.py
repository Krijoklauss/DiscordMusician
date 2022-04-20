import json


class LanguageHandler:
    def __init__(self):
        self.languages = self.loadLanguages()

    def loadLanguages(self):

        _json = {}
        with open("./data/languages.json", "r", encoding="UTF-8") as infile:
            _json = json.loads(infile.read())
            infile.flush()
            infile.close()
        return _json

    def code_exists(self, country_code: str):
        try:
            self.languages['languages'][country_code]
            return True
        except (IndexError, KeyError):
            return False

    def get_language(self, country_code: str):
        return self.languages['languages'][country_code]
