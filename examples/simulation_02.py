# -*- coding: utf-8 -*-

import textwrap
from biosim.simulation import BioSim

"""
A minimal example of a BioSim simulation.
The simulation lasts for 50 years with only herbivores.
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
                  WWHHHHLLLLLLLLWWWWWWW
                  WWWHHHHLLLLLLLWWWWWWW
                  WWWWWWWWWWWWWWWWWWWWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (5, 5),
                  'pop': [{'species': 'Herbivore',
                           'age': 3,
                           'weight': 15}
                          for _ in range(150)]}]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs,
                 seed=123456,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}},
                 vis_years=None)
    sim.set_landscape_parameters('L', {'f_max': 800})
    sim.set_animal_parameters('Herbivore', {'F': 20})
    sim.simulate(num_years=50)
