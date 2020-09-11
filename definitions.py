import requests
import json
import re
import os.path
import pathlib

GOOGLE_URL = 'http://api.dictionaryapi.dev/api/v2/entries'
ADDON_PATH = pathlib.Path(__file__).parent


class GoogleDefinition:
    def __init__(self, word):
        payload = {'define': word, 'lang': 'en'}
        r = requests.get(GOOGLE_URL + '/' + payload['lang'] + '/' + payload['define'])
        self.j = r.json()

    def format_def(self) -> str:
        whole_def = ''
        # print(self.j[0]['meanings'][0]['definitions'])
        if type(self.j) == list:
            for item in self.j[0]['meanings']:
                whole_def += item['partOfSpeech'] + '\n'
                for i, definition in enumerate(item['definitions'], 1):
                    whole_def += str(i) + '. ' + definition['definition'] + '\n'
                    if 'example' in definition:
                        whole_def += definition['example'] + '\n'
                whole_def += '\n'
        whole_def = whole_def.rstrip()
        return whole_def





class WebstersDefinition:
    def __init__(self, word):
        with open(ADDON_PATH / 'websters.json', 'r', encoding='utf-8') as dictionary:
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
        return whole_def



