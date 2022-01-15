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

        random.seed(seed)
        # Påvirker potensielt andre script som kjører.
        # Vurder å lage egen Random-instans, slik at BioSIm kan eie sitt eget random seed.

        if self._validate_island_map(island_map):
            self.island = World(island_map)

        self._year = 0
        self._num_animals_per_species = {}
        self._num_animals = 0

        self.add_population(ini_pop)

        # Disse variablene lages under instansiering. De brukes for å lage data som kan sendes til grafikk-klassen.
        self._num_years = 0  # Duration of sim
        self.cube_population_herbs = np.empty(())
        self.cube_population_carns = np.empty(())
        self.cubelist_properties_herbs = []
        self.cubelist_properties_carns = []


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
        self._vis_years = self._set_vis_years(vis_years)
        self._img_years = self._set_img_years(img_years)

        if self._validate_im_dir_im_base(img_dir, img_base):
            self._img_dir = img_dir

    def _set_img_years(self, img_years: int):
        # TODO: Burde også teste for negative verdier, andre datatyper.
        if img_years is None:
            img_years = self._vis_years
        return img_years

    def _set_vis_years(self, vis_years: int)-> int:
        # TODO: Gjøre validering av vis_years
        return vis_years

    def _validate_island_map(self, island_map:str)-> bool:
        """Returns True/False. Checks that the str contains no white space, and that the rows are of the same length"""
        if not type(island_map) is str:
            raise ValueError('island_map must be of type str.')
            return False

        str_list = island_map.split(sep='\n')
        length_check = len(str_list[0])

        for element in str_list:
            if len(element) != length_check:
                raise ValueError('Island map must contain an equal amount of columns.')
                return False
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
                os.makedirs(img_dir) # Sender melding til OS-et om å opprette katalogen. OS-et kan si "ja" eller "nei".
            except OSError: # Om det ikke får raises en OSError
                raise OSError('Making dir failed')
                return False

        return True

    @property
    def year(self):
        """Last year simulated."""
        return self._year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self._num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return self._num_animals_per_species

    def get_yearly_herb_count(self)-> object:
        """Dette er en datagenererings-metode for å finne ut hvor mange herbivores som finnes i verden akk nå.
        Returnerer en np array.shape(1,) 1D"""
        kube =  self.cube_population_herbs
        # kube.sum(rad_dimensjonen).sum(kolonne_dimensjonen) = array med en sum (scalar) per år.
        serie = kube.sum(-1).sum(-1)
        # TODO: Do validation
        # assert len(serie) == self._num_years. Valideringen er logisk feil, kan ikke brukes.
        return serie

    def get_yearly_carn_count(self):
        """Dette er en datagenererings-metode for å finne ut hvor mange carnivores som finnes i verden akk nå."""
        kube =  self.cube_population_carns
        serie = kube.sum(-1).sum(-1)
        # TODO: Do validation
        # assert len(serie) == self._num_years
        return serie

    def set_animal_parameters(self, species:str, params:dict):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == 'Herbivore':
            Herbivore.set_params(params)
        if species == 'Carnivore':
            Carnivore.set_params(params)


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

    def add_population(self, ini_pop:dict): #TODO: Sjekk om begge populasjoner (ini_pop) er tomme. Ikke noe poeng å kjøre simulering.
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

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        if os.listdir(self._img_dir):
            self.graphics.make_movie_from_files()
        else:
            raise FileNotFoundError(f'{self._img_dir} is empty.')

    def simulate(self, num_years:int = 10):
        self._num_years = num_years # Trenger num_years utenfor simulate metoden. Brukes i get_yearly_carn_count og get_yearly_herb_count
        yearly_pop_map_herbs = []
        yearly_pop_map_carns = []

        for year in range(1, self._num_years + 1):
            with np.nditer(self.island.object_map, flags=['multi_index', 'refs_ok']) as it:
                for element in it:
                    landscape = element.item()
                    if landscape.landscape_type in 'LH':
                        landscape.regrowth()
                        landscape.grassing()
                    if landscape.landscape_type in 'LHD':
                        landscape.hunting()
            self.island.do_migration()
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


            yearly_carn_objects_map = self.island.get_property_map_objects('v_carn_properties_objects')
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

            #--------------------------------------------------------------------------------------------------------
            # Graphics for the year
            if not self._vis_years is None:
                if self._vis_years > 0:
                    if num_years % self._vis_years != 0:
                        raise ValueError('num_years must be multiple of vis_years')

            pause = 0.2
            show = False
            save = False

            if self._vis_years == 0:
                show = False
            elif self._vis_years is None:
                if year == self._num_years:
                    pause = 3
                    show = True
            elif self._vis_years >= 1:
                if year % self._vis_years == 0:
                    pause = 1/self._vis_years #TODO: Finn en pause basert på antall år som simuleres og intervall mellom bilder.
                    show = True

            if self._img_years == 0:
                save =False
            if self._img_years is None:
                if year == self._num_years:
                    save = True
            elif self._img_years >= 1:
                if year % self._img_years == 0:
                    save = True

            if any((show, save)):
                self.graphics.show_grid(self.cube_population_herbs,
                                         self.cube_population_carns,
                                         self.get_yearly_herb_count(),
                                         self.get_yearly_carn_count(),
                                         self.cubelist_properties_herbs,
                                         self.cubelist_properties_carns,
                                         pause, year, show, save)
            self._year += 1
            self._num_animals_per_species = {'Herbivores': yearly_pop_map_herbs[-1].sum(),
                                             'Carnivores': yearly_pop_map_carns[-1].sum()}
            self._num_animals = yearly_pop_map_herbs[-1].sum() + yearly_pop_map_carns[-1].sum()

            print('\r',f'Year:{year}  Herbivores:{yearly_pop_map_herbs[-1].sum()}   Carnivores:{yearly_pop_map_carns[-1].sum()}', end = '')

        print()




