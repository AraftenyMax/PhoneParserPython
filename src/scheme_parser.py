import json


class SchemeParser:
    def __init__(self, json_scheme:str):
        self.json_scheme = json_scheme
        self.scheme = ""

    def generate_scheme(self):
        try:
            self.scheme = json.loads(self.json_scheme)
        except ValueError as e:
            print(e)

    def get_scheme(self):
        return self.scheme