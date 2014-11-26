__author__ = 'aldnav'


import logging
import uuid
import glob
import core.environment
import settings
from datetime import datetime

now = datetime.now()
file_name = now.isoformat()

output_file = "/".join(glob.glob(__file__)[0].split('/')[:-1]) + "/results/" + str(file_name) + "-results.csv"
logging.basicConfig(filename=output_file, level=logging.WARNING, format='%(message)s')


class Environment(core.environment.Environment):

    def __init__(self, *args, **kwargs):
        core.environment.Environment.__init__(self, args, kwargs)
        self.person_mgr = kwargs['person_mgr']
        self.mosquito_mgr = kwargs['mosquito_mgr']
        # let the environment be known to all managers
        self.person_mgr.environment = self
        self.mosquito_mgr.environment = self
        # let the environment be known to all agents
        for person in self.person_mgr.queue:
            person.environment = self
        for mosquito in self.mosquito_mgr.queue:
            mosquito.environment = self
        self.current_time_step = 0

    def simulate(self):
        self.log_headers()
        time_steps = int(settings.config['time_steps'])
        self.display_stats(0)   # display for first day
        for time_step in xrange(1, time_steps+1):
            print "Simulating timestep", time_step,"..."
            # self.display_stats(time_step)
            self.current_time_step = time_step        # rough implementation of timeliness > models
            self.log_results(time_step)
            self.mosquito_mgr.run()
            self.person_mgr.run()
            print "\t\t...done."
        # prompt for output results
        print "Results saved to ", output_file
        self.save_config()

    def display_stats(self, time_step):
        prompt = """
        \rtimestep: {day}
        \rtotal persons: {pop_persons}\t\t\ttotal mosquitoes: {pop_mosquitoes}
        \rsusceptible (persons): {sus_persons}\tsusceptible (mosquitoes): {sus_mosquitoes}
        \rinfected (persons): {inf_persons}\t\tinfected (mosquitoes): {inf_mosquitoes}
        \rrecovered (persons): {rec_persons}
        """.format(day=time_step,
                   pop_persons=len(self.person_mgr.queue),
                   pop_mosquitoes=len(self.mosquito_mgr.queue),
                   sus_persons=self.person_mgr.count_susceptible(),
                   sus_mosquitoes=self.mosquito_mgr.count_susceptible(),
                   inf_persons=self.person_mgr.count_infected(),
                   inf_mosquitoes=self.mosquito_mgr.count_infected(),
                   rec_persons=self.person_mgr.count_recovered())
        print prompt

    def log_headers(self):
        line = """{0},{1},{2},{3},{4}""".format(
            "P_Susceptible", "P_Infected",  # person SIR
            "P_Recover",
            "M_Susceptible", "M_Infected"  # mosquito SI
        )
        logging.warning(line)

    def log_results(self, time_step):
        line = """{0},{1},{2},{3},{4}""".format(
            # time_step, len(self.person_mgr.queue), len(self.mosquito_mgr.queue),    # time steps, total counts
            self.person_mgr.count_susceptible(), self.person_mgr.count_infected(),  # person SIR
            self.person_mgr.count_recovered(),
            self.mosquito_mgr.count_susceptible(), self.mosquito_mgr.count_infected()  # mosquito SI
        )
        logging.warning(line)

    def save_config(self):
        import shutil
        shutil.copy2('.season_config.json', "/".join(glob.glob(__file__)[0].split('/')[:-1]) + "/results/" + str(file_name) + "-season_config.json")