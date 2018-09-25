import os
import json


def load_config_file(filename: str):
    base_path = get_base_folder_path()
    path = os.path.join(base_path, 'configs/{}.json'.format(filename))
    try:
        with open(path) as config_data:
            config = json.load(config_data)
    except FileNotFoundError as e:
        print(e)
    else:
        return config


def get_base_folder_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def dump_json(filename, data: dict):
    with open(filename, 'a+') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


def dump_csv(filename, data: dict):
    with open(filename, 'a+') as outfile:
        outfile.write(','.join(data.values()))
