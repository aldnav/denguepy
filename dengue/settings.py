__author__ = 'aldnav'

db = 'sqlite:///database.db'
__config_file__ = '.config.json'

import json

with open(__config_file__) as file:
    config = json.loads(file.read())
