import textwrap
from world import BioSim_param, BioSim
from graphics import Graphics, Graphics_param
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

    sim.simulate(num_years=50)

    sim.set_landscape_parameters('L', {'f_max': 800})

    herb_pop_map = sim.get_property_map('v_size_herb_pop')
    kube = sim.cube_population_herbs
    #kube_last_year = kube[-1, :, :]

    #herb_property_map = sim.get_property_map_objects('v_herb_properties_objects')
    #samlet_liste = []
    #with np.nditer(herb_property_map, flags=['multi_index', 'refs_ok']) as it:
    #    for element in it:
    #        lista = element.item()
    #        if type(lista) == list:
    #            samlet_liste += lista
    #herbivore_property_array = np.asarray(samlet_liste)

    #fig, ax = plt.subplots(2)
    #ax[0].hist(herbivore_property_array[:, 0])
    #ax[1].hist(herbivore_property_array[:, 1])

    #plt.show()
    #print(herbivore_property_array[:, 1])


    herb_count = kube.sum(-1).sum(-1)
    #print(herb_count)
    def plotting_herb_count():
        fig,ax = plt.subplots()
        ax.plot(herb_count, label = 'herbs')
        #ax.plot(carn_count, label = 'carns')
        ax.set_title('Population size', loc = 'left')
        ax.set_xlabel('Years')
        ax.set_ylabel('Number of herbs')
        leg = ax.legend(loc = 'center left')
        plt.show()
        #fig.savefig('Test_plot.pdf')
        return ax




    # def size_herb_pop(location):
    #     """Location er et landskaps-objekt i objekt-kartet, en rute. """
    #     return len(location.herb_pop)
    #
    def size_carn_pop(location):
        return len(location.carn_pop)
    #
    def make_property_map(fx):
        property_map = np.empty(sim.island_map.shape, dtype=float)
        vget_property = np.vectorize(fx)
        property_map[:, :] = vget_property(sim.island_map_objects)
        return property_map

    #herb_pop_map = make_property_map(size_herb_pop)
    carn_pop_map = make_property_map(size_carn_pop)


    graf = Graphics(sim.island_map)
    graf.plot_island_map()


    def show_herb_pop(year):
         sns.heatmap(kube[year, :, :], annot = True, cmap = 'Greens')
         plt.show()
    def show_carn_pop():
        sns.heatmap(carn_pop_map, annot = True, cmap = 'Reds')
        plt.show()

    #for year in range(30):
    show_herb_pop(29)
    show_carn_pop()
    plotting_herb_count()










