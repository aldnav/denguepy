__author__ = 'aldnav'


import random
from core.models import Agent
from core.models import states as states
import settings


class Person(Agent):
    """
    The person model
    """
    is_latent = False

    def __init__(self, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)
        #: Identifier of the person
        if 'id' in kwargs:
            self.id = kwargs['id']
        #: The environment the person is currently in
        if 'environment' in kwargs:
            self.environment = kwargs['environment']
        self.infection_duration = random.randint(1, int(settings.config['infection_duration']))

    def run(self):
        # TODO Define another attribute "latent_infection"
        # while biting is ongoing, don't change state
        # assign to latent infection and apply infection state later
        # CASE: Currently infected so infection duration minimized
        if self.state is states.INFECTED:
            if self.infection_duration > 0:
                self.infection_duration -= 1
            # CASE: Infection is done so recover
            else:
                self.state = states.RECOVER
                self.is_latent = False

        # ageing
        self.age += 1


class Mosquito(Agent):
    """
    The mosquito model
    """
    is_dying = False
    is_latent = False

    def __init__(self, *args, **kwargs):
        super(Mosquito, self).__init__(id, *args, **kwargs)
        #: Identifier of the mosquito
        if 'id' in kwargs:
            self.id = kwargs['id']
        #: The environment the mosquito is currently in
        if 'environment' in kwargs:
            self.environment = kwargs['environment']
        #: The probability a mosquito could die by incidence
        self.death_probability = settings.config['death_by_incidence']
        self.biting_time_min = settings.config['biting_time'][0]
        self.biting_time_max = settings.config['biting_time'][1] + 1
        #: Assign definite biting time from biting time range
        self.biting_time = random.randint(self.biting_time_min, self.biting_time_max)

    def run(self):
        if self.is_dying:
            # remove self from mgr queue
            self.environment.mosquito_mgr.queue.remove(self)
            # signal mosquito_mgr to spawn new mosquito
            self.environment.mosquito_mgr.spawn_new_mosquito()
            return

        self.bite_persons()
        self.eval_is_dying()   # where to put this?

        # ageing
        self.age += 1

    def eval_is_dying(self):
        # TODO death by incidence
        # concept, by probability the mosquito dies
        # reports to the mosquito manager to spawn new mosquito
        # die (remove self from mosquito manager queue and return)
        if random.random() < self.death_probability:
            self.is_dying = True

    def bite_persons(self):
        """
        Choose random people to bite
        """
        # TODO change to one person only
        person_infection_probability = settings.config['person_infection_probability']
        mosquito_infection_probability = settings.config['mosquito_infection_probability']
        person_to_bite = random.choice(self.environment.person_mgr.queue)
        # TODO move this to a disease handler probably
        # CASE: Person is not infected yet
        if not person_to_bite.is_latent:
            # CASE: Mosquito is infected, person is susceptible
            if person_to_bite.state is states.SUSCEPTIBLE and self.state is states.INFECTED:
                if random.random() < person_infection_probability:   # can get infected
                    person_to_bite.state = states.INFECTED  # the person gets infected
                    person_to_bite.is_latent = True
                    return
        # CASE: Mosquito is not infected yet
        if not self.is_latent:
            # CASE: Mosquito is susceptible, person is infected
            if person_to_bite.state is states.INFECTED and self.state is states.SUSCEPTIBLE:
                if random.random() < mosquito_infection_probability:
                    self.state = states.INFECTED
                    self.latent = True
                    return
