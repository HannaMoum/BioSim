import textwrap
from world import BioSim_param, BioSim, Graphics_param, Graphics
import matplotlib.pyplot as plt

if __name__ == '__main__':
    plt.ion()
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

    ini_herbs = [{'loc': (10, 10),
                'pop': [{'species': 'Herbivore',
                'age': 5,
                'weight': 20}
                for _ in range(150)]}]

    ini_carns = [{'loc': (10, 10),
                'pop': [{'species': 'Carnivore',
                'age': 5,
                'weight': 20}
                for _ in range(40)]}]

    ini_herb_pop = [{'species': 'Herbivore', 'age': 5, 'weight': 6} for _ in range(10)]
    ini_carn_pop = [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(50)]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs+ini_carns,
                 seed=123456,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                'age': {'max': 60.0, 'delta': 2},
                'weight': {'max': 60, 'delta': 2}},
                )
    graf = Graphics(sim.island_map)

    #print(sim.island_map)
    #print(graf.island_plot)
    #graf.plot_island_map()


    sim.simulate()
    #print(sim.yearly_population)
    #graf.plot_population_development(sim.yearly_population)
    print(sim.island_map_objects[7,10].herb_pop)
    #print(sim.island_map_objects[7,10].herb_pop[0].migration_direction())



