import textwrap
from biosim.biosim_klasse import BioSim
import matplotlib.pyplot as plt
from graphics import Graphics

#from biosim.lowland import Landscape

#plt.show()
import numpy as np
import seaborn as sns

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

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs + ini_carns,
                 seed=123456,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60.0, 'delta': 2}},
                 vis_years=2,
                 ymax_animals=None,
                 cmax_animals={'Herbivore': 40, 'Carnivore': 10},
                 img_dir='C:/temp/BioSim/figs',
                 img_base='BioSim',
                 img_fmt='png',
                 img_years=None
                 )

    sim.simulate(num_years=10)
    #sim.make_movie()

    #sim.set_landscape_parameters('L', {'f_max': 800})

    # herb_pop_map = sim.get_property_map('v_size_herb_pop')

    # plt.show()
    # print(herbivore_property_array[:, 1])

    # Plotter kartet over øya
    # graf = Graphics(sim.island.base_map)

    #graf.plot_island_map()
    """
    # Plotter begge populasjoner på samme ax
    herb_count = sim.get_yearly_herb_count()
    carn_count = sim.get_yearly_carn_count()
    graf.plotting_population_count(herb_count, carn_count)
    """
    # kube1 = sim.cube_population_herbs
    # kube2 = sim.cube_population_carns
    #graf.plot_heatmap(kube1, species='herbivore')
    #graf.plot_heatmap(kube2, species='carnivore')
    # plt.show()

    """herb_data = sim.cubelist_properties_herbs
    carn_data = sim.cubelist_properties_carns

    graf.plot_histogram(herb_data, carn_data)"""

    # herb_count = sim.get_yearly_herb_count()
    # carn_count = sim.get_yearly_carn_count()
    # kube1 = sim.cube_population_herbs
    # kube2 = sim.cube_population_carns
    # herb_data = sim.cubelist_properties_herbs
    # carn_data = sim.cubelist_properties_carns
    #graf.show_panel(herb_count, carn_count, kube1, 'herbivore', herb_data, carn_data)

    #graf.make_grid(10)

    #sim.graphics.do_graphics(kube1, kube2, herb_count, carn_count, herb_data, carn_data)
    #dash.make_movie()

    # TODO: Bildene blir liggende i C:/temp/figs, og filmene blir liggende i C:/temp. Folderne må finnes på disk fra før, slik det er nå.
    # dash.make_from_files(kube1, kube2, herb_count, carn_count, herb_data, carn_data, 29)
    #dash.make_movie(kube1, kube2, herb_count, carn_count, herb_data, carn_data, 20)
    # dash.make_grid(year=5)
    # dash.make_movie()
    #dash.make_from_files()
    #plt.show()