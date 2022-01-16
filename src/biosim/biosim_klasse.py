"""Implements a complete simulation"""

import numpy as np
import random
import os
from dataclasses import dataclass
from biosim.animals import Herbivore
from biosim.animals import Carnivore
from biosim.landscape import Landscape
from biosim.world import World
from biosim.graphics import Graphics


@dataclass
class BioSimParam:
    hist_spec_pattern = {'fitness': {'max': float, 'delta': int},
                         'age': {'max': float, 'delta': int},
                         'weight': {'max': float, 'delta': int}}

    default_img_dir: str = 'C:/temp/BioSim'
    default_img_base: str = 'BioSim'
    default_img_fmt: str = 'png'


class BioSim(BioSimParam):
    """Define and perform a simulation.

        Parameters
        ----------
        island_map: `str`
            Multilinestring of {'W', 'D', 'L', 'H'} mapping the entire island's geography, see Notes.
        ini_pop: `list` of `dict`, optional
            Population to be placed on island, see Notes.
        seed: `int`, optional
            Random seed
        vis_years: `int`, optional
            Years between visualization updates (if 0, disable graphics)
        ymax_animals: `int` or `float`, optional
            Number specifying y-axis limit for graph showing animal numbers
        cmax_animals: `dict`, optional
            Dict specifying color-code limits for animal densities
        hist_specs: `dict`, optional
            Specifications for histograms, see Notes
        img_dir: `str` optional
            String with path to directory for figures
        img_base: `str`, optional
            String with beginning of file name for figures
        img_fmt: `str`, optional
            String with file type for figures, e.g. 'png'
        img_year: `int`, optional
            Years between visualizations saved to files (default: vis_years)
        log_file: `str`, optional
            If given, write animal counts to this file

        Attributes
        ----------
        island: `obj`
            Object of class :py:class:`.World`
        _initial_num_year: None or `int`
            How many years you simulate at once.

            Provides opportunity to simulate in intervals with pauses.
        _num_years: `int`
            Simulation duration in years
        hist_spec_pattern: `dict`
            Default pattern of input hist_spec
        default_img_dir: `str`
            Default path to directory for figures, 'C:/temp/BioSim'.
        default_img_base: `str`
            Default beginning of file name for figures, 'BioSim'.
        default_img_fmt: `str`
            Default image format, 'png'.

        Notes
        -----

        :math:`\mathtt{island\_map}` should be created the following way:
            >>> create_map = \"""\\
                                  WLW
                                  WWW
                                  WWW\"""
            >>> island_map = textwrap.dedent(create_map)

        :math:`\mathtt{ini\_pop}` should be created by the following set-up:
            >>> ini_pop = [{'loc': (2, 2),
            >>>             'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 5},
            >>>                     {'species': 'Carnivore', 'age': 6, 'weight': 6.5}]}]

        :math:`\mathtt{hist\_specs}` is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
            >>> {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
        Permitted properties are 'weight', 'age' and 'fitness'.

        :math:`\mathtt{img\_dir}` and :math:`\mathtt{img\_base}` must either both be None or both be strings.

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

        self._initial_num_year = None

        # Disse variablene lages under instansiering. De brukes for å lage data som kan sendes til grafikk-klassen.
        self._num_years = 0  # Duration of sim
        self.population_map_herbivore = np.empty(())
        self.population_map_carnivore = np.empty(())
        self.population_size_herbivore = []
        self.population_size_carnivore = []
        self.herbivore_age_weight_fitness = []
        self.carnivore_age_weight_fitness = []


        self._img_dir = img_dir
        self._img_base = img_base
        self._img_fmt = img_fmt

        if all((self._validate_hist_specs(hist_specs),
                self._validate_cmax_animals(cmax_animals),
                self._validate_im_params(img_dir, img_base, img_fmt))):
            self.graphics = Graphics(self.island.base_map,
                                     hist_specs,
                                     ymax_animals,
                                     cmax_animals,
                                     vis_years,
                                     self._img_dir,
                                     self._img_base,
                                     self._img_fmt,
                                     img_years)
        self._vis_years = self._set_vis_years(vis_years)
        self._img_years = self._set_img_years(img_years)

        # if self._validate_im_dir_im_base(img_dir, img_base):
        #     self._img_dir = img_dir

    def _set_img_years(self, img_years: int):
        """Private setter method for img_years.

        If input provided, set img_years to input value,
        else set to default value :py:attr:`.vis_years`.

        Parameters
        ----------
        img_years: `int` or None
            Years between visualizations saved to files

        Returns
        -------
        img_years: `int`
            If input provided, set img_years to input value,
            else set to default value :py:attr:`.vis_years`.
        """
        # TODO: Burde også teste for negative verdier, andre datatyper.
        if img_years is None:
            img_years = self._vis_years
        return img_years

    def _set_vis_years(self, vis_years: int)-> int:
        """Private setter method for vis_years.

        Validates correct input.

        Parameters
        ----------
        vis_years: `int`
            Years between visualization updates.

        Raises
        ------
        ValueError
            vis_years must a positive whole number.

        Returns
        -------
        vis_years: `int`
        """
        # TODO: Gjøre validering av vis_years. Må komme inn som 0, int eller None. Hvis det er en int så må den være 0 eller større.
        return vis_years

    def _validate_island_map(self, island_map:str)-> bool:
        """Validate input type island_map before sending to World class.

        Parameters
        ----------
        island_map: `str`
            String of {'W', 'D', 'L', 'H'} mapping the entire island's geography.

        Raises
        ------
        ValueError
            Island_map must be a string, and contain an equal amount of columns.

        Returns
        -------
        `bool`
            True, if island map passes validation.
        """
        if not type(island_map) is str:
            raise ValueError('Island map must be be a string.')
            return False #REMOVE

        str_list = island_map.split(sep='\n')
        length_check = len(str_list[0])

        for element in str_list:
            if len(element) != length_check:
                raise ValueError('Island map must contain an equal amount of columns.')
                return False #REMOVE
        return True

    def _validate_hist_specs(self, hist_specs:dict)-> bool:
        """Private validation of provided input hist_specs.

        Parameters
        ----------
        hist_specs: `dict`
            Specifications for histograms

        Raises
        ------
        KeyError
            Provided key in :py:attr:`.hist_specs` is not valid.

        Returns
        -------
        `bool`
            True if hist_specs passes validation.
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
            raise KeyError(f'Provided key is not allowed in hist_specs. Valid keys are: {self.hist_spec_pattern}')
        else:
            return True

    def _validate_cmax_animals(selfself, cmax_animals:dict)-> bool:
        """Private validation of provided input cmax_animals.

        Parameters
        ----------
        cmax_animals: `dict` or None
            Dict specifying color-code limits for animal densities.

        Raises
        ------
        KeyError
            Provided key is not valid.

        Returns
        -------
        `bool`
            True, if cmax_animals passes validation.
        """
        if cmax_animals is None:
            return True
        for key, value in cmax_animals.items():
            if key not in ['Herbivore', 'Carnivore']:
                raise KeyError(f'{key} is not a legal key in cmax_animals. Legal keys are Herbivore and Carnivore.')
            else:
                return True

    def _validate_im_params(self, img_dir:str, img_base:str, img_fmt:str):
        """Private validation of provided image parameters.

        Parameters
        ----------
        img_dir: `str`
            Path to directory for figures
        img_base: `str`
            Beginning of file name for figures
        img_fmt: `str`
            File format for figures

        Raises
        ------
        ValueError
            Either both :math:`\mathtt{img\_dir}` and :math:`\mathtt{img\_base}` must be specified,
            or none at all
        ValueError
            Unsupported image format provided.
        OSError
            The making of directory path failed.

        Returns
        -------
        `bool`
            True if all the method's input parameters passes validation.
        """
        if not any((
                all((type(img_dir) is str, type(img_base) is str)),
                all((img_dir is None, img_base is None))
                )):
            raise ValueError('Either both img_dir and img_base must specified or neither of them can be specified.')

        if img_dir is None:
            self._img_dir = self.default_img_dir
        if img_base is None:
            self._img_base = self.default_img_base
        if img_fmt is None:
            self._img_fmt = self.default_img_fmt
        else:
            if img_fmt not in ['jpeg', 'jpg', 'png', 'tif', 'tiff']:
                raise ValueError(f'Image format {img_fmt} not supported. '
                                 f'Valid formats are: jpeg, jpg, png, tif, tiff')

        if not os.path.isdir(self._img_dir):
            try:
                os.makedirs(self._img_dir)
            except OSError:
                raise OSError('Making directory failed')
                raise OSError('Making directory failed')

        return True

    @property
    def year(self):
        """Last year simulated (`int`)."""
        return self._year

    @property
    def num_animals(self):
        """Total number of animals on island (`int`)."""
        return self._num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species on island (`dict`)."""
        return self._num_animals_per_species

    def set_animal_parameters(self, species:str, params:dict):
        """Set parameters for animal species.

        Parameters
        ----------
        species: {'Herbivore', 'Carnivore'}
        params

        Returns
        -------

        """
        """Set parameters for animal species.

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

    def add_population(self, population): #TODO: Sjekk om begge populasjoner (ini_pop) er tomme. Ikke noe poeng å kjøre simulering.
        #TODO: men skal vel være mulig å opprette øya for det, og deretter plassere ut dyr...
        """Add population on island.

        Parameters
        ----------
        population: `list` of `dict
            Population of animals to be placed in specified locations on the island.

        Returns
        -------
        None
            Return None if no initial population is given.

            Otherwise add population on island.

        See Also
        --------
        :py:meth:`.add_population_in_location`
            Relationship
        """
        """Validates input dict befor sending calling add_population method in
        the world class
        Initial_population looks like:

        ini_pop = [{'loc': (3,4),
        'pop': [{'species': 'Herbivore',
                'age': 10, 'weight': 12.5},
            {'species': 'Herbivore',
                'age': 9, 'weight': 10.3}]}]
        """
        if population:
            self.island.add_population_in_location(population)
        else:
            return None

    def make_movie(self):
        """Create MPEG4 movie from visualizing images saved.

        Raises
        -------
        FileNotFoundError
            No saved figures to create movie from found.
        """
        if os.listdir(self._img_dir):
            self.graphics.make_movie_from_files()
        else:
            raise FileNotFoundError(f'{self._img_dir} is empty. Need figures to create movie.')


    def simulate(self, num_years:int = 10):

        # simulate er tricky fordi den skal kunne startes, stoppes, og deretter fortsette fra forrige kjøring.
        # Start-stopp logikk
        if self._initial_num_year is None:
            self._initial_num_year = num_years
            self._num_years = num_years
            start_loop = 1
        else:
            start_loop = self.year + 1
            self._num_years = self.year + num_years

        for current_year in range(start_loop, self._num_years + 1):
            self._year += 1
            self._annual_cycle()
            self._collect_annual_data()
            self._do_annual_graphics(current_year)

            self._num_animals_per_species = {'Herbivores': self.population_map_herbivore.sum(),
                                             'Carnivores': self.population_map_carnivore.sum()}
            self._num_animals = self.population_map_herbivore.sum() + self.population_map_carnivore.sum()

            print('\r',f'Year:{current_year}  Herbivores:{self.population_map_herbivore.sum()}   Carnivores:{self.population_map_carnivore.sum()}', end ='')

        print()

    def _annual_cycle(self):
        """All steps in annual cycle on the island"""
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

    def _collect_annual_data(self):
        # Data for every year. Her genereres data for hvert år.

        # Data for heatmaps
        self.population_map_herbivore = self.island.get_property_map('v_size_herb_pop')
        self.population_map_carnivore = self.island.get_property_map('v_size_carn_pop')

        # Data for population size
        self.population_size_herbivore.append(self.population_map_herbivore.sum())
        self.population_size_carnivore.append(self.population_map_carnivore.sum())

        # Data for histograms
        herbivore_object_map = self.island.get_property_map_objects('v_herb_properties_objects')
        carnivore_object_map = self.island.get_property_map_objects('v_carn_properties_objects')
        object_maps = [herbivore_object_map, carnivore_object_map]
        for species in object_maps:
            # Standard akkumulering i numpy fungerte ikke fordi vi hadde en array full av None verdier, der det ikke var noen dyr.
            # Måtte derfor skrive egen akkumulerings funksjon som legger sammen alle populasjonslistene på landskapene på øya, til en liste med alle dyr på øya.
            acc_list = []
            with np.nditer(species, flags=['multi_index', 'refs_ok']) as it:
                for element in it:
                    list_on_location = element.item()
                    if type(list_on_location) == list:
                        acc_list += list_on_location
            if species is herbivore_object_map:
                self.herbivore_age_weight_fitness = np.asarray(acc_list)
            if species is carnivore_object_map:
                self.carnivore_age_weight_fitness = np.asarray(acc_list)

    def _do_annual_graphics(self, current_year:int):
        # Graphics for the year
        if self._vis_years is not None:
            if self._vis_years > 0:
                if self._initial_num_year % self._vis_years != 0:
                    raise ValueError('num_years must be multiple of vis_years')

        pause = 0.2
        show = False
        save = False

        if self._vis_years == 0:
            show = False
        elif self._vis_years is None:
            if current_year == self._num_years:
                pause = 3
                show = True
        elif self._vis_years >= 1:
            if current_year % self._vis_years == 0:
                pause = 1 / self._vis_years  # TODO: Finn en pause basert på antall år som simuleres og intervall mellom bilder.
                show = True

        if self._img_years == 0:
            save = False
        if self._img_years is None:
            if current_year == self._num_years:
                save = True
        elif self._img_years >= 1:
            if current_year % self._img_years == 0:
                save = True

        if any((show, save)):
            self.graphics.show_grid(self.population_map_herbivore,
                                    self.population_map_carnivore,
                                    np.asarray(self.population_size_herbivore),
                                    np.asarray(self.population_size_carnivore),
                                    self.herbivore_age_weight_fitness,
                                    self.carnivore_age_weight_fitness,
                                    pause, current_year, show, save)




