# -*- coding: utf-8 -*-

import textwrap
from biosim.simulation import BioSim

"""A minimal example of a BioSim simulation.
In the first 100 years of the simulation the island only contains herbivores. 
After 100 years the carnivores are introduced.  
"""

__author__ = 'Cassandra Hjortdahl', 'Hanna Lye Moum'
__email__ = 'cassandra.hjortdahl@nmbu.no', 'hanna.lye.moum@nmbu.no'


if __name__ == '__main__':

    geogr = """\
               WWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWHWWWWLLLLLLLW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHHHHHWWLLLLLLWWW
               WHHHHHLLLLLLLLLLLLWWW
               WHHHHHLLLDDLLLHLLLWWW
               WHHLLLLLDDDLLLHHHHWWW
               WWHHHHLLLDDLLLHWWWWWW
               WHHHLLLLLDDLLLLLLLWWW
               WHHHHLLLLDDLLLLWWWWWW
               WWWWWWWWWWWWWWWWWWWWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (5, 5),
                  'pop': [{'species': 'Herbivore',
                           'age': 3,
                           'weight': 25}
                          for _ in range(200)]}]
    ini_carns = [{'loc': (5, 5),
                  'pop': [{'species': 'Carnivore',
                           'age': 2,
                           'weight': 20}
                          for _ in range(60)]}]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs,
                 seed=123456,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}},
                 vis_years=None)

    sim.simulate(num_years=100)
    sim.add_population(population=ini_carns)
    sim.simulate(num_years=100)