__author__ = 'aldnav'

__config_file__ = '.season_config.json'

import json

with open(__config_file__) as f:
    config = json.loads(f.read())