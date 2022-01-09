import numpy as np
from dataclasses import dataclass
from biosim.animals import Herbivore
from biosim.animals import Carnivore
from biosim.lowland import Landscape



@dataclass
class BioSim_param:
    seed: int = None
    codes_for_landscape_types: str = 'WLHD'


class BioSim(BioSim_param):

    def __init__(self, island_map, ini_pop = None, seed = None,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):
        self._island_map = self.make_island_map(island_map)
        self._island_map_objects = self.make_island_map_objects()
        self.ini_pop = ini_pop
        self._yearly_population = []

    @property
    def yearly_population(self):
        return self._yearly_population

    def add_to_yearly_population(self, value):
        self._yearly_population.append(value)

    def migration_preparation(self):
        with np.nditer(self.island_map_objects, flags=['multi_index', 'refs_ok']) as it:
            for element in it:
                landskapsobjekt = element.item()
                for animal in landskapsobjekt.herb_pop + landskapsobjekt.carn_pop:
                    animal.has_migrated = False

    def migration(self):
        with np.nditer(self.island_map_objects, flags=['multi_index', 'refs_ok']) as it:
            for element in it:
                landskapsobjekt = element.item()

                lovlige_retninger = []  # Lovlige retninger å bevege seg i for dyrene på denne lokasjoner
                if landskapsobjekt.landscape_type != 'W': # Sjekker at vi står på noe annet enn vann
                    row, col = it.multi_index # Blir en tuple, med lokasjon på hvor vi er
                    if self.island_map[row-1, col] != 'W':
                        lovlige_retninger.append((-1, 0))
                    if self.island_map[row+1, col] != 'W':
                        lovlige_retninger.append((1,0))
                    if self.island_map[row, col-1] != 'W':
                        lovlige_retninger.append((0, -1))
                    if self.island_map[row, col+1] != 'W':
                        lovlige_retninger.append((0, 1))

                moved = []
                for herbivore in landskapsobjekt.herb_pop:
                    new_row, new_col = herbivore.migration_direction()
                    if (new_row, new_col) in lovlige_retninger:
                        self.island_map_objects[new_row, new_col].herb_pop.append(herbivore)
                        moved.append(herbivore)
                        herbivore.has_migrated = True

                for herbivore in moved:
                    landskapsobjekt.herb_pop.remove(herbivore)


    def create_herb_list(self):
        # Turning initial list of information into list of Herbivores
        # NOW: Assuming we only have herbivores
        herb_list = []
        for animal in self.ini_pop:
            if animal['species'] == 'Herbivore':
                herb_list.append(Herbivore(animal['age'], animal['weight']))
        return herb_list

    def cycle(self, location):
        location.regrowth()
        location.grassing()
        location.hunting()
        # Migration
        location.give_birth()
        location.aging()
        location.death()

    def simulate(self, num_years = 1, vis_years = 1):
        # Husk oppsett som plasserer alle dyr ved initsiering
        self.island_map_objects[7, 10].herb_pop = [Herbivore(10, 500)]
        for year in range(num_years):
            with np.nditer(self.island_map_objects, flags=['multi_index', 'refs_ok']) as it:
                for element in it:
                    location = element.item()
                    if location.landscape_type in 'LH':
                        location.regrowth()
                        location.grassing()
                    if location.landscape_type in 'LHD':
                        location.hunting()
            self.migration_preparation()
            self.migration()
            with np.nditer(self.island_map_objects, flags=['multi_index', 'refs_ok']) as it:
                for element in it:
                    location = element.item()
                    if location.landscape_type in 'LHD':
                        location.give_birth()
                        location.aging()
                        #location.death()
                        self.add_to_yearly_population(len(location.herb_pop)) # Dette er bare en dumy property.


                    #self.cycle(location)


    def validate_island_map(self, island_map):
        return True
        # Raises value error if rules broken.
        # Returns True if all OK.

    def make_island_map(self, island_map):
        if self.validate_island_map(island_map):
            island_map_list = list(island_map.split('\n'))
            row, col = len(island_map_list), len(island_map_list[0])
            _build_map = np.empty(shape=(row, col), dtype='str')

            for row_index, row_string in enumerate(island_map_list):
                for col_index, codes_for_landscape_types in enumerate(row_string):
                    _build_map[row_index, col_index] = codes_for_landscape_types  # Leser bokstaven inn i riktig posisjon i arrayen.

            return _build_map

    @property
    def island_map(self):
        return self._island_map

    def make_island_map_objects(self):
        """Denne lager kartet med objekt referanser for hvert landskap basert på island_map"""
        _island_map_objects = np.empty(self.island_map.shape, dtype='object')
        vLandscape = np.vectorize(Landscape)
        _island_map_objects[:,:] = vLandscape(self.island_map)

        return _island_map_objects

    @property
    def island_map_objects(self):
        return self._island_map_objects



# ------------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib import colors

@dataclass
class Graphics_param:
    codes_for_landscape_types: str = 'WLHD'

    def code_landscape(self, value): # Finn mer beskrivende funksjonsnavn
        # Funksjonen må oppdateres med å sjekke at input value er lovlig.
        plot_values_for_landscape_types = '0123'
        # Vurder å ha de som parametere, sånn at de kan brukes globalt
        if value in self.codes_for_landscape_types:
            replacement_values = list(zip(self.codes_for_landscape_types, plot_values_for_landscape_types))
            for letter,number in replacement_values:
                if value == letter:
                    return int(number)


class Graphics(Graphics_param):

    def __init__(self, numpy_island_map):
        self._island_plot = self.make_plot_map(numpy_island_map)

    @property
    def island_plot(self):
        return self._island_plot

    def make_plot_map(self, numpy_island_map):
        island_map_plot = np.copy(numpy_island_map) # Lager intern kopi, for å unngå å ødelegge opprinnelig array. Hadde bare blitt et view om man ikke hadde gjort det.
        vcode_landscape = np.vectorize(self.code_landscape) # Vektoriserer funksjonen. Funksjonen kan da benyttes celle for celle i arrayen (eller et utvalg av arrayen).
        island_map_plot[:, :] = vcode_landscape(island_map_plot) # Bruker den vektoriserte funksjonen element for element i slicen som er laget (her alle celler).
        island_map_plot = np.array(island_map_plot, dtype=int)  # Konverterer fra siffer (tall som str) til tall (int).

        return island_map_plot
        # Returnerer np array med verdiene 0 til 3, som kan brukes til plotting.

    def plot_island_map(self, plot_map=None, scale = 3):
        if plot_map == None:
            plot_map = self.island_plot
        row, col = plot_map.shape
        with plt.style.context('seaborn-whitegrid'): # Konfigurerbar? Skal dette være en input?
            colormap = colors.ListedColormap(['blue', 'darkgreen', 'lightgreen', 'yellow']) # Skal dette være en input
            fig, ax = plt.subplots(figsize=(col / scale, row / scale))
            ax.imshow(plot_map, cmap=colormap, extent=[1, col + 1, row + 1, 1])
            ax.set_xticks(list(range(1, col + 1)))
            ax.set_yticks(list(range(1, row + 1)))
            plt.show()

        return ax # Returnerer grafen

    def plot_population_development(self, yearly_population_size):
        with plt.style.context('seaborn-whitegrid'): # Konfigurerbar? Skal dette være en input?
            fig, ax = plt.subplots()
            ax.plot(yearly_population_size)
            plt.show()


    def plot_panel(self):
        pass
        # Skal plotte det ferdige panelet, med de ulike plottene i en figur (grid).
        # En fig med mange axes.















