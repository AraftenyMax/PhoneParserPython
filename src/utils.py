import os
import json


def load_config_file(filename: str):
    base_path = get_base_folder_path()
    path = os.path.join(base_path, f'configs\\{filename}.json')
    try:
        with open(path) as config_data:
            config = json.load(config_data, encoding='win1251')
    except FileNotFoundError as e:
        print(e)
    else:
        return config


def get_base_folder_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
