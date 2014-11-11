__author__ = 'aldnav'


class Manager(object):

    def __init__(self, queue, *args, **kwargs):
        self.queue = queue

    def run(self):
        for agent in self.queue:
            agent.start()