__author__ = 'aldnav'


from core.managers import Manager
import models
import settings


class PersonManager(Manager):

    def __init__(self, queue, *args, **kwargs):
        # super(Manager, self).__init__(queue, *args, **kwargs)
        Manager.__init__(self, queue, *args, **kwargs)
        if 'environment' in kwargs:
            self.environment = kwargs['environment']
        self.queue = queue
        self.init_states()

    def init_states(self):
        initially_infected_persons = int(settings.config['initially_infected_persons'] * settings.config['no_of_persons'])
        initially_recovered_persons = int(settings.config['initially_recovered_persons'] * settings.config['no_of_persons'])
        infected_count = initially_infected_persons
        recovered_count = initially_recovered_persons
        for person in self.queue:
            if infected_count > 0:
                person.state = models.states.INFECTED  # infected
                person.is_latent = True
                infected_count -= 1
            else:
                if recovered_count > 0:
                    person.state = models.states.RECOVER
                    recovered_count -= 1
                else:
                    break

    def count_susceptible(self):
        return len([p for p in self.queue if p.state == models.states.SUSCEPTIBLE])

    def count_infected(self):
        return len([p for p in self.queue if p.state == models.states.INFECTED])

    def count_recovered(self):
        return len([p for p in self.queue if p.state == models.states.RECOVER])

    def run(self):
        for person in self.queue:
            person.run()


class MosquitoManager(Manager):

    def __init__(self, queue, *args, **kwargs):
        # super(Manager, self).__init__(queue, *args, **kwargs)
        Manager.__init__(self, queue, *args, **kwargs)
        if 'environment' in kwargs:
            self.environment = kwargs['environment']
        self.queue = queue
        self.init_states()

    def init_states(self):
        # config = json.loads(open(settings.config).read())
        initially_infected_mosquitoes = int(settings.config['initially_infected_mosquitoes'] * settings.config['no_of_mosquitoes'])
        infected_count = initially_infected_mosquitoes
        for mosquito in self.queue:
            if infected_count > 0:
                mosquito.state = models.states.INFECTED
                mosquito.is_latent = True
                infected_count -= 1
            else:
                break

    def count_susceptible(self):
        return len([m for m in self.queue if m.state == models.states.SUSCEPTIBLE])

    def count_infected(self):
        return len([m for m in self.queue if m.state == models.states.INFECTED])

    def run(self):
        for mosquito in self.queue:
            mosquito.run()

    def spawn_new_mosquito(self):
        new_born_mosquito = models.Mosquito(len(self.queue))
        new_born_mosquito.environment = self.environment
        new_born_mosquito.state = models.states.SUSCEPTIBLE
        self.queue.append(new_born_mosquito)