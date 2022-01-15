import numpy as np
import random
import os
from dataclasses import dataclass
from biosim.animals import Herbivore
from biosim.animals import Carnivore
from biosim.landscape import Landscape
from world import World
from graphics import Graphics



@dataclass
class BioSim_param:
    codes_for_landscape_types: str = 'WLHD' #Brukes denne?
    hist_spec_pattern = {'fitness': {'max': float, 'delta': int},
                      'age': {'max': float, 'delta': int},
                      'weight': {'max': float, 'delta': int}}


class BioSim(BioSim_param):
    """Island hosting landscapes with animals.

        Parameters
        ----------
        island_map:
        ini_pop: `list` of `dict`, optional


        Attributes
        ----------

        """

    def __init__(self, island_map, ini_pop=None, seed=None,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):

        random.seed(seed) # Påvirker potensielt andre script som kjører. Vurder å lage egen Random-instans, slik at BioSIm kan eie sitt eget random seed.

        if self._validate_island_map(island_map): # ikke sjekk hele her, fordeles ned til animals
            self.island = World(island_map) #Bare opprette self.island direkte

        self.add_population(ini_pop)

    def _validate_island_map(self, island_map:str)-> bool:
        """Returns True/False. Checks that the str contains no white space, and that the rows are of the same length"""
        str_list = island_map.split(sep='\n')
        length_check = len(str_list[0])

        for element in str_list:
            if len(element) != length_check:
                raise ValueError('Island map must contain an equal amount of columns.')
                return False
        return True


        # Disse variablene lages under instansiering. De brukes for å lage data som kan sendes til grafikk-klassen.
        self._num_years = 0  # Duration of sim
        self.cube_population_herbs = np.empty(())
        self.cube_population_carns = np.empty(())
        self.cubelist_properties_herbs = []
        self.cubelist_properties_carns = []

        # self.cube_properties_herbs = np.empty(())
        # self.cube_properties_carns = np.empty(())

        if all((self._validate_hist_specs(hist_specs),
                self._validate_cmax_animals(cmax_animals),
                self._validate_im_dir_im_base(img_dir, img_base))):
            self.graphics = Graphics(self.island.base_map,
                                     hist_specs,
                                     ymax_animals,
                                     cmax_animals,
                                     vis_years,
                                     img_dir,
                                     img_base,
                                     img_fmt,
                                     img_years)

    def _validate_island_map(self, island_map_list: list) -> bool:
        # Should already be textwrapped
        length_check = len(island_map_list[0])
        for element in island_map_list:

            for letter in element:
                if letter not in 'WHLD':
                    raise ValueError(
                        f'{letter} is not a defined landscape.\n'
                        f'Defined landscapes are: ["Lowland", "Highland", "Desert", "Water"]\n'
                        'respectively given by their belonging capital letter.')

            if len(element) != length_check:
                raise ValueError('Island map must contain an equal amount of columns.')

            if not (element[0] and not element[-1]) == 'W':
                raise ValueError('All the islands` outer edges must be of landscape Water.')

        if not (island_map_list[0] and not island_map_list[-1]) == 'W' * length_check:
            raise ValueError('All the islands` outer edges must be of landscape Water.')

        return True

    def _validate_hist_specs(self, hist_specs:dict)-> bool:
        """
        hist_specs = {'fitness': {'max': 1.0, 'delta': 0.05},
                      'age': {'max': 60.0, 'delta': 2},
                      'weight': {'max': 60, 'delta': 2}},
        """
        error_main_key = False
        error_sub_key = False
        for key in hist_specs:
            if key not in self.hist_spec_pattern:
                error_main_key = True
                break
            for sub_key in hist_specs[key]:
                if sub_key not in self.hist_spec_pattern[key]:
                    error_sub_key = True

        if any((error_main_key, error_sub_key)):
            raise KeyError(f'Not is not allowed in hist_specs. Valid keys are: {self.hist_spec_pattern}')
        else:
            return True

    def _validate_cmax_animals(selfself, cmax_animals:dict)-> bool:
        for key, value in cmax_animals.items():
            if key not in ['Herbivore', 'Carnivore']:
                raise KeyError(f'{key} is not a legal key in cmax_animals. Legal keys are Herbivore and Carnivore')
            else:
                return True

    def _validate_im_dir_im_base(self, img_dir:str, img_base:str):
        if any((all((type(img_dir) == str, type(img_base) == 'str')),
                    all((type(img_dir) == None, type(img_base) == None)))):
            raise ValueError('Error. Both must be str or None')
            return None

        if not os.path.isdir(img_dir): # Returnerer true om dir finnes.
            try:
                os.makedirs(img_dir)
            except OSError:
                raise OSError('Making dir failed')
                return False

        return True



    def get_yearly_herb_count(self)-> object:
        """Dette er en datagenererings-metode for å finne ut hvor mange herbivores som finnes i verden akk nå.
        Returnerer en np array.shape(1,) 1D"""
        kube =  self.cube_population_herbs
        # kube.sum(rad_dimensjonen).sum(kolonne_dimensjonen) = array med en sum (scalar) per år.
        serie = kube.sum(-1).sum(-1)
        # TODO: Do validation
        assert len(serie) == self._num_years
        return serie

    def get_yearly_carn_count(self):
        """Dette er en datagenererings-metode for å finne ut hvor mange carnivores som finnes i verden akk nå."""
        kube =  self.cube_population_carns
        serie = kube.sum(-1).sum(-1)
        # TODO: Do validation
        assert len(serie) == self._num_years
        return serie

    def set_animal_parameters(self, species:str, params:dict): # TODO: må oppdatere for carnivore også
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == 'Herbivore':
            Herbivore.set_params(params)
        if species == 'Carnivore':
            Carnivore.set_params(params)

        #Evt: type(species).set_params(params)

    def set_landscape_parameters(self, landscape:str, params:dict):
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

        # # Oppdaterer alle eksisterende objekter.f_max. Denne settes normalt kun i __init__, og må oppdateres når klassevariabelen endres.
        # # TODO: Sjekk om dette har tilbakevirkende kraft på instansene som allerede finnes.
        # with np.nditer(self.island.object_map, flags=['multi_index', 'refs_ok']) as it:
        #     for element in it:
        #         landskapsobjekt = element.item()
        #         if landskapsobjekt.landscape_type == 'H':
        #             landskapsobjekt.f_max = landskapsobjekt.params['f_max']['Highland']
        #         elif landskapsobjekt.landscape_type == 'L':
        #             landskapsobjekt.f_max = landskapsobjekt.params['f_max']['Lowland']
        #         else:
        #             landskapsobjekt.f_max = 0

    # def migration_preparation(self):
    #     with np.nditer(self.island.object_map, flags=['multi_index', 'refs_ok']) as it:
    #         for element in it:
    #             landscape_obj = element.item()
    #             landscape_obj.migration_prep()  # Better hierarcy
    #             # for animal in landscape_obj.herb_pop + landscape_obj.carn_pop:
    #             #     animal.has_migrated = False

    # def migration(self):
    #     """."""
    #     with np.nditer(self.island.object_map, flags=['multi_index', 'refs_ok']) as it:
    #         for element in it:
    #             landscape_obj = element.item()
    #             #current_row, current_col = it.multi_index
    #             row, col = it.multi_index
    #
    #             migrate_herbs, migrate_carns = landscape_obj.migrate() #-> {herb: (r,c)}
    #
    #             def method_2(landscape_pop, migrate_dict, current_row, current_col, species):
    #                 moved = []
    #                 for animal, location in migrate_dict.items():
    #                     r, c = location
    #                     new_row = current_row + r
    #                     new_col = current_col + c
    #
    #                     if self.island.object_map[new_row, new_col].is_migratable:
    #                         self.island.object_map[new_row, new_col].population.append(animal)
    #                         # if species == 'Herbivore':
    #                         #     self.island.object_map[new_row, new_col].herb_pop.append(animal) #Still not good...
    #                         # if species == 'Carnivore':
    #                         #     self.island.object_map[new_row, new_col].carn_pop.append(animal)
    #
    #                         moved.append(animal)
    #
    #                 for migrated_animal in moved:
    #                     landscape_pop.remove(migrated_animal)
    #
    #             if landscape_obj.is_migratable:
    #                 method_2(landscape_obj.population, {**migrate_herbs, **migrate_carns}, row, col, 'dummy')
    #                 # method_2(landscape_obj.herb_pop, migrate_herbs, row, col, 'Herbivore')
    #                 # method_2(landscape_obj.carn_pop, migrate_carns, row, col, 'Carnivore')



    def simulate(self, num_years:int = 10):
        self._num_years = num_years # Trenger num_years utenfor simulate metoden. Brukes i get_yearly_carn_count og get_yearly_herb_count
        yearly_pop_map_herbs = []
        yearly_pop_map_carns = []
        #yearly_property_map_herbs = []
        #yearly_property_map_carns = []

        current_year = 0
        for year in range(self._num_years):
            current_year += 1
            with np.nditer(self.island.object_map, flags=['multi_index', 'refs_ok']) as it:
                for element in it:
                    landscape = element.item()
                    if landscape.landscape_type in 'LH':
                        landscape.regrowth()
                        landscape.grassing()
                    if landscape.landscape_type in 'LHD':
                        landscape.hunting()
            self.island.do_migration()
            #self.migration_preparation()
            #self.migration()
            with np.nditer(self.island.object_map, flags=['multi_index', 'refs_ok']) as it:
                for element in it:
                    landscape = element.item()
                    if landscape.landscape_type in 'LHD':
                        landscape.give_birth()
                        landscape.aging()
                        landscape.do_death()
            #-------------------------------------------------------------------------------------
            # Data for every year. Her genereres data for hvert år. Dataene pakkes på slutten av simuleringen til kuber eller lister av tabeller.

            # Herbivore populasjonsstørrelse for alle lokasjoner per år
            yearly_pop_map_herbs.append(self.island.get_property_map('v_size_herb_pop'))
            # Carnivore populasjonsstørrelse for alle lokasjoner per år
            yearly_pop_map_carns.append(self.island.get_property_map('v_size_carn_pop'))

            #---------------------------------------------------------------------

            yearly_herb_objects_map = self.island.get_property_map_objects('v_herb_properties_objects')
            # Standard akkumulering i numpy fungerte ikke fordi vi hadde en array full av None verdier, der det ikke var noen dyr.
            # Måtte derfor skrive egen akkumulerings funksjon som legger sammen alle populasjonslistene på landskapene på øya, til en liste med alle dyr på øya.
            acc_list_herb = []
            with np.nditer(yearly_herb_objects_map, flags=['multi_index', 'refs_ok']) as it:
                for element in it:
                    list_on_location = element.item()
                    if type(list_on_location) == list:
                        acc_list_herb += list_on_location
            yearly_herbivore_property_array = np.asarray(acc_list_herb)
            self.cubelist_properties_herbs.append(yearly_herbivore_property_array)
            # Brukes ikke nå, men ikke slett!
            #yearly_property_map_herbs.append(yearly_herb_objects_map)

            yearly_carn_objects_map = self.island.get_property_map_objects('v_carn_properties_objects')
            acc_list_carn = []
            with np.nditer(yearly_carn_objects_map, flags=['multi_index', 'refs_ok']) as it:
                for element in it:
                    list_on_location = element.item()
                    if type(list_on_location) == list:
                        acc_list_carn += list_on_location
            yearly_carnivore_property_array = np.asarray(acc_list_carn)
            self.cubelist_properties_carns.append(yearly_carnivore_property_array)
            # Brukes ikke nå, men ikke slett!
            #yearly_property_map_carns.append(yearly_carn_objects_map)

            print('\r',f'Year:{current_year}  Herbivores:{yearly_pop_map_herbs[-1].sum()}   Carnivores:{yearly_pop_map_carns[-1].sum()}', end = '')

        # Data at end of simulation
        # TODO: Add evaluation. Check shape and size. Raises valueerror
        self.cube_population_herbs = np.stack(yearly_pop_map_herbs)
        self.cube_population_carns = np.stack(yearly_pop_map_carns)

        # Disse brukes ikke akkurat nå, men ikke slett!
        #self.cube_properties_herbs = np.stack(yearly_property_map_herbs)
        #self.cube_properties_carns = np.stack(yearly_property_map_carns)

        self.graphics.show(self.cube_population_herbs,
                           self.cube_population_carns,
                           self.get_yearly_herb_count(),
                           self.get_yearly_carn_count(),
                           self.cubelist_properties_herbs,
                           self.cubelist_properties_carns)

    def add_population(self, ini_pop:dict):
        """Validates input dict befor sending calling add_population method in
        the world class
        Initial_population looks like:

        ini_pop = [{'loc': (3,4),
        'pop': [{'species': 'Herbivore',
                'age': 10, 'weight': 12.5},
            {'species': 'Herbivore',
                'age': 9, 'weight': 10.3}]}]
        """
        self.island.add_population(ini_pop)
        #pass

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        self.graphics.make_from_files(self.cube_population_herbs,
                                      self.cube_population_carns,
                                      self.get_yearly_herb_count(),
                                      self.get_yearly_carn_count(),
                                      self.cubelist_properties_herbs,
                                      self.cubelist_properties_carns)