import requests
import json
import re
import os.path
import pathlib

GOOGLE_URL = 'https://googledictionaryapi.eu-gb.mybluemix.net'
ADDON_PATH = pathlib.Path(__file__).parent


class GoogleDefinition:
    def __init__(self, word):
        payload = {'define': word, 'lang': 'en'}
        r = requests.get(GOOGLE_URL, params=payload)
        self.j = r.json()

    def format_def(self) -> str:
        whole_def = ''
        for item in self.j:
            for speech, definitions in item['meaning'].items():
                whole_def += speech + '\n'
                for i, definition in enumerate(definitions, 1):
                    whole_def += str(i) + '. ' + definition['definition'] + '\n'
                    if 'example' in definition:
                        whole_def += definition['example'] + '\n'
            whole_def += '\n'
        whole_def = whole_def.rstrip()
        return whole_def


class WebstersDefinition:
    def __init__(self, word):
        with open(ADDON_PATH / 'websters.json', 'r', encoding="utf-8") as dictionary:
            self.definitions = []
            self.j = json.load(dictionary)

            for item in self.j:
                if word.upper() in item['word'].split(';'):
                    self.definitions.append(item)

    def format_def(self) -> str:

        whole_def = ''
        for item in self.definitions:
            whole_def += item['pos'] + '\n'
            for i, definition in enumerate(item['definitions'], 1):
                whole_def += str(i) + '. ' + definition + '\n'
            whole_def += '\n'
        whole_def = whole_def.rstrip()
        # print(whole_def)

        return whole_def

        # x = re.sub(r'(\b\d\b.)', r'\n\1', self.definition)
        # print(self.definition)

# WebstersDefinition('wqwqwqwq').format_def()
