import json


def load_sample_data(file_path="sample.json"):
    data = None
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data