__author__ = 'aldnav'

import settings
import threading


class Enum(set):
    def __getattr__(self, item):
        if item in self:
            return item
        raise AttributeError
#: the state of infection
states = Enum(["SUSCEPTIBLE", "INFECTED", "RECOVER"])


class Agent(object):
    """
    Base model for an agent.
    """
    #: The age of the agent at the current time step
    age = 0
    id = 0

    def __init__(self, *args, **kwargs):
        # threading.Thread.__init__(self)
        #: State refers to the current state of the agent. Default state is susceptible
        self.state = states.SUSCEPTIBLE
        #: State refers to the previous state before the change
        self.latent_state = None
        #: The environment the agent is currently in
        if 'environment' in kwargs:
            self.environment = kwargs['environment']

    def run(self):
        pass

    def __repr__(self):
        return str(self.id)