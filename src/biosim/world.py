import numpy as np
import random
from dataclasses import dataclass
from biosim.animals import Herbivore
from biosim.animals import Carnivore
from biosim.lowland import Landscape




@dataclass
class BioSim_param:
    seed: int = None
    codes_for_landscape_types: str = 'WLHD' #Brukes denne?


class BioSim(BioSim_param):

    def __init__(self, island_map, ini_pop = None, seed = None,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):

        random.seed(seed)
        self._island_map = self.make_island_map(island_map)
        self._island_map_objects = self.make_island_map_objects()
        self._ini_pop = self.add_population(ini_pop)
            #TODO: Save ini_pop directly from input
            # Add_population returns nothing, it is an action of its' own
        self._num_years = 0 # Duration of sim
        self.cube_population_herbs = np.empty(())
        self.cube_population_carns = np.empty(())
        self.cube_properties_herbs = np.empty(())
        self.cube_properties_carns = np.empty(())
        self.cubelist_properties_herbs = []
        self.cubelist_properties_carns = []

    @property
    def island_map(self):
        return self._island_map

    @property
    def island_map_objects(self):
        return self._island_map_objects

    def get_yearly_herb_count(self):
        kube =  self.cube_population_herbs
        serie = kube.sum(-1).sum(-1)
        # TODO: Do validation
        assert len(serie) == self._num_years
        return serie

    def get_yearly_carn_count(self):
        kube =  self.cube_population_carns
        serie = kube.sum(-1).sum(-1)
        # TODO: Do validation
        assert len(serie) == self._num_years
        return serie

    def make_island_map(self, island_map):
        """
        Mapping island with
        Parameters
        ----------
        island_map

        Returns
        -------

        """
        """Lager kartet som inneholder bokstaver for hver landskapstype ut i fra den geogr-strengen som kommer inn"""
        island_map_list = island_map.split()  # Oppretter liste, splitter ved default på new-line

        if self.validate_island_map(island_map_list):  # IMPLEMENTERT
            row, col = len(island_map_list), len(island_map_list[0]) # Antall rader = antall elementer i lista, antall kolonner = lengden av den første raden
            _build_map = np.empty(shape=(row, col), dtype='str') # Lager tom np.array som skal fylles med bokstaver for hvert landskap

            for row_index, row_string in enumerate(island_map_list): # Går gjennom hver rad
                for col_index, landscape_letter in enumerate(row_string): # Går gjennom hver kolonne (elementene i raden).
                    _build_map[row_index, col_index] = landscape_letter  # Leser bokstaven inn i riktig posisjon i arrayen.

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
                landskapsobjekt = element.item()
                for animal in landskapsobjekt.herb_pop + landskapsobjekt.carn_pop:
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


    def get_property_map(self, fx_map_type):
        return self.__make_property_map(getattr(self, fx_map_type), self.island_map, self.island_map_objects)

    def get_property_map_objects(self, fx_map_type):
        return self.__make_property_map_objects(getattr(self, fx_map_type), self.island_map, self.island_map_objects)

    #------------------------------------------------------------------------------------------------
    # Factory for property_maps
    def v_size_herb_pop(self, location:object):
        """Location er et landskaps-objekt i objekt-kartet, en rute. """
        return len(location.herb_pop)

    def v_size_carn_pop(self, location:object):
        return len(location.carn_pop)

    def __make_property_map(self, fx:object, island_map:object, island_map_objects:object):
        property_map = np.empty(island_map.shape, dtype=float)
        vget_property = np.vectorize(fx)
        property_map[:, :] = vget_property(island_map_objects)
        return property_map

    def v_herb_properties_objects(self, location:object):
        population_list = location.herb_pop
        if len(population_list) > 0:
            liste = []
            for animal in population_list:
                liste.append((animal.age, animal.weight, animal.fitness))
            return liste

    def v_carn_properties_objects(self, location:object):
        population_list = location.carn_pop
        if len(population_list) > 0:
            liste = []
            for animal in population_list:
                liste.append((animal.age, animal.weight, animal.fitness))
            return liste


    def __make_property_map_objects(self, fx:object, island_map:object, island_map_objects:object):
        property_map = np.empty(island_map.shape, dtype=object)
        vget_property = np.vectorize(fx)
        property_map[:, :] = vget_property(island_map_objects)
        return property_map

    #------------------------------------------------------------------------------------------------

    def simulate(self, num_years = 10, vis_years = 1):
        self._num_years = num_years
        yearly_pop_map_herbs = []
        yearly_pop_map_carns = []
        yearly_property_map_herbs = []
        yearly_property_map_carns = []

        for year in range(self._num_years):
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

            # Data for every year
            yearly_pop_map_herbs.append(self.get_property_map('v_size_herb_pop'))
            yearly_pop_map_carns.append(self.get_property_map('v_size_carn_pop'))

            yearly_herb_objects_map = self.get_property_map_objects('v_herb_properties_objects')
            yearly_property_map_herbs.append(yearly_herb_objects_map)

            yearly_carn_objects_map = self.get_property_map_objects('v_carn_properties_objects')
            yearly_property_map_carns.append(yearly_carn_objects_map)

            acc_list_herb = []
            with np.nditer(yearly_herb_objects_map, flags=['multi_index', 'refs_ok']) as it:
                for element in it:
                    list_on_location = element.item()
                    if type(list_on_location) == list:
                        acc_list_herb += list_on_location
            yearly_herbivore_property_array = np.asarray(acc_list_herb)
            self.cubelist_properties_herbs.append(yearly_herbivore_property_array)


            acc_list_carn = []
            with np.nditer(yearly_carn_objects_map, flags=['multi_index', 'refs_ok']) as it:
                for element in it:
                    list_on_location = element.item()
                    if type(list_on_location) == list:
                        acc_list_carn += list_on_location
            yearly_carnivore_property_array = np.asarray(acc_list_carn)
            self.cubelist_properties_carns.append(yearly_carnivore_property_array)



        # Data at end of simulation
        # TODO: Add evaluation. Check shape and size. Raises valueerror
        self.cube_population_herbs = np.stack(yearly_pop_map_herbs)
        self.cube_population_carns = np.stack(yearly_pop_map_carns)

        self.cube_properties_herbs = np.stack(yearly_property_map_herbs)
        self.cube_properties_carns = np.stack(yearly_property_map_carns)





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

