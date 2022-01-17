# TODO: Move to examples, or delete before delivery (wait until tuesday).
import textwrap
from biosim.simulation import BioSim

if __name__ == '__main__':
    # plt.ion() Når du har skrudd av denne vil ikke figur-viduet dette sammen med en gang
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

    ini_herbs = [{'loc': (9, 9),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}]

    ini_carns = [{'loc': (9, 9),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(40)]}]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs+ini_carns,
                 seed=123456,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60.0, 'delta': 2}},
                 vis_years=None,
                 ymax_animals=None,
                 cmax_animals={'Herbivore': 40, 'Carnivore': 10},
                 img_fmt='png',
                 img_years=0)#,
                 #img_dir='C:/temp/BioSim',
                 #img_base='BioSim'
                 #)

    sim.set_animal_parameters('Herbivore', {'zeta': 3.2, 'xi': 1.8})
    sim.set_animal_parameters('Carnivore', {'a_half': 70, 'phi_age': 0.5,
                                            'omega': 0.3, 'F': 65,
                                            'DeltaPhiMax': 9.})
    sim.set_landscape_parameters('L', {'f_max': 800})

    sim.simulate(num_years=10)
    # sim.add_population(population=ini_carns)
    # sim.simulate(num_years=5)
    # sim.simulate(num_years=3)

    # import cProfile
    # import pstats
    # from pstats import SortKey
    #
    # cProfile.run('sim.simulate(5)', 'restats')
    # p = pstats.Stats('restats')
    # p.sort_stats(SortKey.CUMULATIVE).print_stats('simulation.py')