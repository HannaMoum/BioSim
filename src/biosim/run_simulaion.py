import textwrap
from world import BioSim_param, BioSim, Graphics_param, Graphics
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

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
                'weight': {'max': 60, 'delta': 2}},
                )

    sim.simulate(num_years=30)

    def size_herb_pop(location):
        """Location er et landskaps-objekt i objekt-kartet, en rute. """
        return len(location.herb_pop)

    def size_carn_pop(location):
        return len(location.carn_pop)

    def make_property_map(fx):
        property_map = np.empty(sim.island_map.shape, dtype=float)
        vget_property = np.vectorize(fx)
        property_map[:, :] = vget_property(sim.island_map_objects)
        return property_map

    herb_pop_map = make_property_map(size_herb_pop)
    carn_pop_map = make_property_map(size_carn_pop)

    graf = Graphics(sim.island_map)
    graf.plot_island_map()


    def show_herb_pop():
        sns.heatmap(herb_pop_map, annot = True, cmap = 'Greens')
        plt.show()
    def show_carn_pop():
        sns.heatmap(carn_pop_map, annot = True, cmap = 'Reds')
        plt.show()

    show_herb_pop()
    show_carn_pop()










