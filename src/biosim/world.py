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
        self._ini_pop = self.add_population(ini_pop)


    @property
    def island_map(self):
        return self._island_map

    @property
    def island_map_objects(self):
        return self._island_map_objects


    def make_island_map(self, island_map):
        """Lager kartet som inneholder bokstaver for hver landskapstype ut i fra den geogr-strengen som kommer inn"""
        if self.validate_island_map(island_map): # Denne gir kun true enn så lenge.
            island_map_list = list(island_map.split('\n')) # Lager en liste av geogr-strengen som kommer inn ved å splitte på new-line.
            row, col = len(island_map_list), len(island_map_list[0]) # Antall rader = antall elementer i lista, antall kolonner = lengden av den første raden
            _build_map = np.empty(shape=(row, col), dtype='str') # Lager tom np.array som skal fylles med bokstaver for hvert landskap

            for row_index, row_string in enumerate(island_map_list): # Går gjennom hver rad
                for col_index, codes_for_landscape_types in enumerate(row_string): # Går gjennom hver kolonne (elementene i raden)
                    _build_map[row_index, col_index] = codes_for_landscape_types  # Leser bokstaven inn i riktig posisjon i arrayen.

            return _build_map

    def make_island_map_objects(self):
        """Denne lager kartet med objekt referanser for hvert landskap basert på island_map"""
        _island_map_objects = np.empty(self.island_map.shape, dtype='object')
        vLandscape = np.vectorize(Landscape)
        _island_map_objects[:,:] = vLandscape(self.island_map)

        return _island_map_objects

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == 'Herbivore':
            Herbivore.set_params(params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape == 'L':
            Landscape.set_params({'f_max': {'Lowland': params['f_max']}})
        elif landscape == 'H':
            Landscape.set_params({'f_max': {'Highland': params['f_max']}})
        else:
            raise ValueError('Feil input')

        # Oppdaterer alle eksisterende objekter.f_max. Denne settes normalt kun i __init__, og må oppdateres når klassevariabelen endres.
        with np.nditer(self.island_map_objects, flags=['multi_index', 'refs_ok']) as it:
            for element in it:
                landskapsobjekt = element.item()
                if landskapsobjekt.landscape_type == 'H':
                    landskapsobjekt.f_max = landskapsobjekt.params['f_max']['Highland']
                elif landskapsobjekt.landscape_type == 'L':
                    landskapsobjekt.f_max = landskapsobjekt.params['f_max']['Lowland']
                else:
                    landskapsobjekt.f_max = 0


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
                current_row, current_col = it.multi_index

                if landskapsobjekt.herb_pop !=[]:
                    lovlige_retninger = []  # Lovlige retninger å bevege seg i for dyrene på denne lokasjoner
                    if landskapsobjekt.is_migratable: # Sjekker at vi står på noe annet enn vann
                        row, col = it.multi_index # Blir en tuple, med lokasjon på hvor vi er
                        if self.island_map_objects[row-1, col].is_migratable:
                            lovlige_retninger.append((-1, 0))
                        if self.island_map_objects[row+1, col].is_migratable:
                            lovlige_retninger.append((1,0))
                        if self.island_map_objects[row, col-1].is_migratable:
                            lovlige_retninger.append((0, -1))
                        if self.island_map_objects[row, col+1].is_migratable:
                            lovlige_retninger.append((0, 1))

                    moved = []
                    for herbivore in landskapsobjekt.herb_pop:
                        if not herbivore.has_migrated:
                            row_direction, col_direction = herbivore.migration_direction()
                            if (row_direction, col_direction) in lovlige_retninger:
                                new_row = current_row+row_direction
                                new_col = current_col+col_direction

                                self.island_map_objects[new_row, new_col].herb_pop.append(herbivore)

                                moved.append(herbivore)
                                herbivore.has_migrated = True

                    for herbivore in moved:
                        landskapsobjekt.herb_pop.remove(herbivore)

                if landskapsobjekt.carn_pop != []:
                    lovlige_retninger = []  # Lovlige retninger å bevege seg i for dyrene på denne lokasjoner
                    if landskapsobjekt.is_migratable:  # Sjekker at vi står på noe annet enn vann
                        row, col = it.multi_index  # Blir en tuple, med lokasjon på hvor vi er
                        if self.island_map_objects[row - 1, col].is_migratable:
                            lovlige_retninger.append((-1, 0))
                        if self.island_map_objects[row + 1, col].is_migratable:
                            lovlige_retninger.append((1, 0))
                        if self.island_map_objects[row, col - 1].is_migratable:
                            lovlige_retninger.append((0, -1))
                        if self.island_map_objects[row, col + 1].is_migratable:
                            lovlige_retninger.append((0, 1))

                    moved = []
                    for carnivore in landskapsobjekt.carn_pop:
                        if not carnivore.has_migrated:
                            row_direction, col_direction = carnivore.migration_direction()

                            if (row_direction, col_direction) in lovlige_retninger:
                                new_row = current_row + row_direction
                                new_col = current_col + col_direction

                                self.island_map_objects[new_row, new_col].carn_pop.append(carnivore)

                                moved.append(carnivore)
                                carnivore.has_migrated = True

                    for carnivore in moved:
                        landskapsobjekt.carn_pop.remove(carnivore)

    def simulate(self, num_years = 10, vis_years = 1):
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
                        location.death()


    def validate_island_map(self, island_map):
        return True
        # Raises value error if rules broken.
        # Returns True if all OK.

    def validate_init_population(self, ini_pop):
        pass

    def add_population(self, population):
        for sp_dict in population:
            for key in sp_dict:
                if key == 'loc':
                    r, c = sp_dict[key]
                    r -= 1
                    c -= 1
                    landscape = self.island_map_objects[r, c]
                if key == 'pop':
                    for animal in sp_dict[key]:
                        if animal['species'] == 'Herbivore':
                            landscape.herb_pop.append(Herbivore(animal['age'], animal['weight']))
                        if animal['species'] == 'Carnivore':
                            landscape.carn_pop.append(Carnivore(animal['age'], animal['weight']))



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
    """Denne klassen skal spørre BioSim, om data og fremstille det grafisk"""

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















