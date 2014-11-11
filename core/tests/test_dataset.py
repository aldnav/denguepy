#!/usr/bin/env python

import dataset

db = dataset.connect('sqlite:///sample.db')
db.begin()

table = db['user']

# table.insert(dict(name='Aldrin Navarro', age=19, country='Philippines', sex='M'))
# table.insert(dict(name='Aireil Navarro', age=17, country='China', sex='F'))
# table.insert(dict(name='Abigail Navarro', age=15, country='India', sex='F'))
# db.commit()

# girls = table.find(sex='F', order_by=['country', '-age'])
#
# for girl in girls:
#     print girl

from core.models import Agent

a = Agent()
print a