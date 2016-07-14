import json


def save_json(file_path, dict_obj):
    with open(file_path, 'w+') as f:
        f.write(json.dumps(dict_obj))


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.loads(f.read().replace('\n', ''))
