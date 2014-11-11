__author__ = 'aldnav'

import dataset
import settings

models = []
tables = {}


def register(model):
    models.append(model)
    db = dataset.connect(settings.db)
    tables[model.__name__] = db[model.__name__]
    # TODO state changes as attributes for each agent model
    # TODO tricky state changes for mosquito agent. includes birth and death