import numpy as np
from dataclasses import dataclass
from biosim.animals import Herbivore
from biosim.animals import Carnivore
from biosim.lowland import Landscape
import textwrap


@dataclass
class BioSim_param:
    seed: int = None
    codes_for_landscape_types: str = 'WLHD' #Brukes denne?


class BioSim(BioSim_param):
    """Island hosting landscapes with animals.

        Parameters
        ----------
        island_map:
        ini_pop: `list` of `dict`, optional


        Attributes
        ----------

        """

    def __init__(self, island_map, ini_pop = None, seed = None,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):
        self._island_map = self.make_island_map(island_map)
        self._island_map_objects = self.make_island_map_objects()
        self._ini_pop = self.add_population(ini_pop)
            #TODO: Save ini_pop directly from input
            # Add_population returns nothing, it is an action of its' own

    @property
    def island_map(self):
        return self._island_map

    @property
    def island_map_objects(self):
        return self._island_map_objects


    def make_island_map(self, island_map):
        """
        Mapping island with respect to each landscape letter.

        Parameters
        ----------
        island_map: `str`
            Geography of island.

            Made up by the letters 'W', 'D', 'L' and 'H' each representing a landscape.

        Returns
        -------
        _build_map: `ndarray` of `str`
            Array containing landscape letters in their respective positions.
        """
        island_map_list = island_map.split()  # Oppretter liste, splitter ved default på new-line

        if self.validate_island_map(island_map_list):  # IMPLEMENTERT
            row, col = len(island_map_list), len(island_map_list[0]) # Antall rader = antall elementer i lista, antall kolonner = lengden av den første raden
            _build_map = np.empty(shape=(row, col), dtype='str') # Lager tom np.array som skal fylles med bokstaver for hvert landskap

            for row_index, row_string in enumerate(island_map_list): # Går gjennom hver rad
                for col_index, landscape_letter in enumerate(row_string): # Går gjennom hver kolonne (elementene i raden).
                    _build_map[row_index, col_index] = landscape_letter  # Leser bokstaven inn i riktig posisjon i arrayen.

            return _build_map

    def make_island_map_objects(self):
        """
        Mapping island with landscape objects.

        Returns
        -------
        _island_map_objects: `ndarray` of `obj`
            Array containing landscape objects in their respective positions.
        """
        _island_map_objects = np.empty(self.island_map.shape, dtype='object')
        vLandscape = np.vectorize(Landscape)
        _island_map_objects[:, :] = vLandscape(self.island_map)

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
         params = {'f_max': {'Highland': 300.0,'Lowland': 800.0}}
        """
        if landscape == 'L':
            Landscape.set_params({'f_max': {'Lowland': params['f_max']}})
        elif landscape == 'H':
            Landscape.set_params({'f_max': {'Highland': params['f_max']}})
        else:
            raise ValueError('Feil input')

        # Oppdaterer alle eksisterende objekter.f_max. Denne settes normalt kun i __init__, og må oppdateres når klassevariabelen endres.
        # TODO: Sjekk om dette har tilbakevirkende kraft på instansene som allerede finnes.
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
                landscape_obj = element.item()
                for animal in landscape_obj.herb_pop + landscape_obj.carn_pop:
                    animal.has_migrated = False

    def migration(self):
        with np.nditer(self.island_map_objects, flags=['multi_index', 'refs_ok']) as it:
            for element in it:
                landskapsobjekt = element.item()
                current_row, current_col = it.multi_index

                if landskapsobjekt.herb_pop:
                    lovlige_retninger = []  # Lovlige retninger å bevege seg i for dyrene på denne lokasjoner
                    if landskapsobjekt.is_migratable: # Sjekker at vi står på noe annet enn vann
                        row, col = it.multi_index # Blir en tuple, med lokasjon på hvor vi er -------------------------------------------------------
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

                    for herbivore in moved: # TODO: Kanskje dette kan gjøres uten for-løkke. Trekke fra hele moved på en gang
                        landskapsobjekt.herb_pop.remove(herbivore)

                if landskapsobjekt.carn_pop:
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
                    location = element.item() # Landskapsobjekt
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

    def validate_island_map(self, island_map_list):
        #map = textwrap.dedent(island_map)  # Should already be textwrapped
        #island_map = island_map.split() #Endret til input

        length_check = len(island_map_list[0])
        for element in island_map_list:
            # Control all symbols
            for letter in element:
                if letter not in 'WHLD':
                    raise ValueError(
                        f'{letter} is not a defined landscape.\n'
                        f'Defined landscapes are: ["Lowland", "Highland", "Desert", "Water"]\n'
                        'respectively given by their belonging capital letter.')
            # Control size
            if len(element) != length_check:
                raise ValueError('Island map must contain an equal amount of columns.')
            # Control edges
            if not (element[0] and element[-1]) == 'W':
                raise ValueError('All the islands` outer edges must be of landscape Water.')
        # Control edges
        if not (island_map_list[0] and island_map_list[-1]) == 'W' * length_check:
            raise ValueError('All the islands` outer edges must be of landscape Water.')

        return True
        # Raises value error if rules broken.
        # Returns True if all OK.

    def validate_init_population(self, ini_pop):
        pass

    def add_population(self, population): #Sjekk ut hva bruken for
        """
       Initial_population looks like:

        ini_pop = [{'loc': (3,4),
        'pop': [{'species': 'Herbivore',
                'age': 10, 'weight': 12.5},
            {'species': 'Herbivore',
                'age': 9, 'weight': 10.3}]}]
        """

        for dictionary in population: #kan kanskje bare bruke self.ini_pop

            r, c = dictionary['loc'] #Tuple
            r -= 1  # Adjustments
            c -= 1  # Adjustments. Checked.

            landscape_object = self.island_map_objects[r, c]  # henter ut landskapsklasse

            population = dictionary['pop']  # [{},{}]
            landscape_object.add_animals(population)

