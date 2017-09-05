import json


def load_config(config_location='apis.config'):
    with open(config_location) as config:
        return json.load(config)
