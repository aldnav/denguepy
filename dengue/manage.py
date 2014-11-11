#!/usr/bin/env python
"""
Manages the whole simulation.
Reads and execute terminal commands with optional
commands.
"""

import sys
import settings
from models import Person, Mosquito
from managers import PersonManager, MosquitoManager
from environment import Environment

commands = ('help', 'simulate', 'setconfig')


def show_help(command=None):
    """
    Show usage instructions
    """
    if command and command in commands:
        # show help on the following command
        # create a docs folder and show the file
        # with the command
        print '\tShowing help for', command
        return
    print 'usage: ./manage.py [help] [command]'
    print '                   <command> [<args>]'
    print '\nThese are the following commands available:'
    print '   simulate\tRun a simulation'
    print '   setconfig\tSet *.conf file as configuration for simulation'


def simulate():
    # read the config file
    assert settings.config['time_steps'] != 0
    assert settings.config['no_of_persons'] != 0
    assert settings.config['no_of_mosquitoes'] != 0

    person_mgr = init_persons(settings.config['no_of_persons'])
    mosquito_mgr = init_mosquitoes(settings.config['no_of_mosquitoes'])
    assert person_mgr is not None
    assert mosquito_mgr is not None
    # TODO init_environment
    # person_mgr.run()
    # mosquito_mgr.run()
    environment = Environment(person_mgr=person_mgr, mosquito_mgr=mosquito_mgr)
    environment.simulate()


def init_environment():
    pass


def init_persons(no_of_persons):
    """
    Initialize persons and return person admin
    """
    return PersonManager([Person(id=x) for x in xrange(no_of_persons)])


def init_mosquitoes(no_of_mosquitoes):
    """
    Initialize mosquitoes and return mosquito admin
    """
    return MosquitoManager([Mosquito(id=x) for x in xrange(no_of_mosquitoes)])


if __name__ == "__main__":
    # input = sys.argv[1:]
    # if len(input) == 0:
    #     show_help()
    #     exit()
    # if input[0] == "help":
    #     try:
    #         show_help(input[1])
    #     except Exception, e:
    #         show_help()
    # if input[0] == "simulate":
    #     simulate()
    simulate()