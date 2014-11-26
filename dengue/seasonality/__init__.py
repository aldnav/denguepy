__author__ = 'aldnav'

import settings

"""
year, person inf prob, mos inf prob
"""
infection_probability_map = list()
infection_probability_map.append(None)

for i in xrange(settings.config["environment"]["time_steps"]):
    for time_season in settings.config["environment"]["time_season"]:
        if i >= time_season[0] and i <= time_season[1]:
            season = time_season[2]
            infection_probability_map.append([i,
                                    settings.config["seasons"][season]["disease"]["person_infection_probability"],
                                    settings.config["seasons"][season]["disease"]["mosquito_infection_probability"]]
                                    )

infection_probability_map[0] = infection_probability_map[1]
# print infection_probability_map
# print len(infection_probability_map)