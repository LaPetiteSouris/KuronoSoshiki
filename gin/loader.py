import json


def load_sample_data(file_path="sample.json"):
    """Load sample data

    Args:
        file_path (str): path to json file
    Returns:
        data load from given file
    """
    data = None
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data