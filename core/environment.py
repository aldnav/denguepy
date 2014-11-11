__author__ = 'aldnav'


class Environment(object):
    """

    """
    agents = None
    time_steps = 10

    def __init__(self, *args, **kwargs):
        if 'agents' in kwargs:
            self.agents = kwargs['agents']
        if 'time_steps' in kwargs:
            self.time_steps = kwargs['time_steps']

    # def simulate(self):
    #     if self.agents is None:
    #         return
    #
    #     for time_step in xrange(0, self.time_steps):
    #         print 'time step:', time_step
    #         for agent in self.agents:
    #             agent.run()
    def simulate(self):
        pass