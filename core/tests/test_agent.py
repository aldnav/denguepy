
import logging
logger = logging.getLogger('tests')
from core.models import Agent

a = Agent()
# print a


class Person(Agent):

    def __init__(self, id=None, *args, **kwargs):
        super(Person, self).__init__(id, *args, **kwargs)

b = Person()
# print b

print isinstance(a, Agent)  # a is an Agent
print isinstance(b, Agent)  # b is an Agent too
print isinstance(a, Person)  # but a is not a Person
print isinstance(b, Person)  # while b is a Person

logger.info("Hello world!")