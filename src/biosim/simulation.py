"""Implements a complete simulation"""

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU

import numpy as np
import random
import os
from dataclasses import dataclass
from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Landscape
from biosim.island import Island
from biosim.graphics import Graphics
from biosim.base_logger import logger


@dataclass
class BioSimParam:
    """Provide default pattern for hist_spec for :py:class:`.BioSim`."""
    hist_spec_pattern = {'fitness': {'max': float, 'delta': int},
                         'age': {'max': float, 'delta': int},
                         'weight': {'max': float, 'delta': int}}


class BioSim(BioSimParam):
    """Define and perform a simulation.

        Parameters
        ----------
        island_map: `str`
            Multilinestring of {'W', 'D', 'L', 'H'} mapping the entire island's geography,
            see Notes.
        ini_pop: `list` of `dict`, optional
            Population to be placed on island, see Notes.
        seed: `int`, optional
            Random seed
        vis_years: `int`, optional
            Years between visualization updates (if 0, disable graphics)
        ymax_animals: `int` or `float`, optional
            Number specifying y-axis limit for graph showing animal numbers
        cmax_animals: `dict`, optional
            Dictionary specifying color-code limits for animal densities
        hist_specs: `dict`, optional
            Specifications for histograms, see Notes
        img_dir: `str` optional
            String with path to directory for figures
        img_base: `str`, optional
            String with beginning of file name for figures
        img_fmt: `str`, optional
            String with file type for figures, e.g. 'png'
        img_years: `int`, optional
            Years between visualizations saved to files (default: vis_years)
        log_file: `str`, optional
            See Notes

        Attributes
        ----------
        island: `obj`
            Object of class :py:class:`.Island`
        _initial_num_year: None or `int`
            How many years you simulate at once.

            Controls that the modulus between simulating years and
            visualizing years are equal to zero.
        _num_years: `int`
            Simulation duration in years.
        hist_spec_pattern: `dict`
            Default pattern of input hist_spec.
        default_img_fmt: `str`
            Default image format, 'png'.
        population_map_herbivore: `ndarray`
            Array containing herbivore population for each cell.
        population_map_carnivore: `ndarray`
            Array containing carnivore population for each cell.
        population_size_herbivore: `list`
            List containig total herbivore population size for every simulated year.
        population_size_carnivore: `list`
            List containig total carnivore population size for every simulated year.
        herbivore_age_weight_fitness: `ndarray`
            Array containing information about every herbivore's age, weight and fitness.
        carnivore_age_weight_fitness: `ndarray`
            Array containing information about every carnivore's age, weight and fitness.

        Notes
        -----

        :math:`\mathtt{island\_map}` should be created one of the following ways:
            >>> # Possibility 1
            >>> create_map = \"""\\
                                  WLW
                                  WWW
                                  WWW\"""
            >>> island_map = textwrap.dedent(create_map)
            >>>
            >>> # Possibility 2
            >>> island_map = "WWW\\nWLW\\nWWW"

        :math:`\mathtt{ini\_pop}` should be created by the following set-up:
            >>> ini_pop = [{'loc': (2, 2),
            >>>             'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 5},
            >>>                     {'species': 'Carnivore', 'age': 6, 'weight': 6.5}]}]

        :math:`\mathtt{hist\_specs}` is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
            >>> {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
        Permitted properties are 'weight', 'age' and 'fitness'.

        Valid specification of :math:`\mathtt{cmax\_animals}` are as following:
            >>> #Provide cmax as a dictionary with one or both keys
            >>> {'Herbivore': 50, 'Carnivore': 20}

        :math:`\mathtt{img\_dir}` and :math:`\mathtt{img\_base}` must either both be None
        or both be strings.

        :math:`\mathtt{log\_file}` is created under the biosim repository whether input
        is given or not. Input has no affection to this.
        """

    def __init__(self, island_map, ini_pop=None, seed=None,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):
        random.seed(seed)

        # Create island object
        if self._validate_island_map(island_map):
            self.island = Island(island_map)

        # Initial property values
        self._year = 0
        self._num_animals_per_species = {'Herbivore': 0, 'Carnivore': 0}
        self._num_animals = 0

        # Add population
        self.add_population(ini_pop)

        # Control simulate procedure
        self._initial_num_year = None
        self._num_years = 0

        # Generate data
        self.population_map_herbivore = np.empty(())
        self.population_map_carnivore = np.empty(())
        self.population_size_herbivore = []
        self.population_size_carnivore = []
        self.herbivore_age_weight_fitness = []
        self.carnivore_age_weight_fitness = []

        # Control graphics
        self._img_dir = img_dir
        self._img_base = img_base
        self._img_fmt = img_fmt
        if all((self._validate_hist_specs(hist_specs),
                self._validate_cmax_animals(cmax_animals),
                self._validate_im_params(img_dir, img_base, img_fmt, img_years)
                )):
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
        self._img_years = self._set_img_years(img_years, img_dir)

        logger.info('BioSim initialized')

    def _set_img_years(self, img_years, img_dir):
        """Private setter method for img_years.

        If input provided, set img_years to input value,
        else set to default value :py:attr:`.vis_years`.

        Parameters
        ----------
        img_years: `int` or None
            Years between visualizations saved to files.

        Returns
        -------
        img_years: `int`
            If input provided, set img_years to input value,
            else set to default value :py:attr:`.vis_years`.
        """
        if img_years:
            if img_years < 0:
                raise ValueError('input value img_years must be positive or equal to zero.')

        if img_dir is None:
            img_years = 0

        if img_dir:
            if img_years is None:
                img_years = self._vis_years

        return img_years

    def _set_vis_years(self, vis_years):
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
        if isinstance(vis_years, int):
            if vis_years < 0:
                raise ValueError('vis_years needs to be larger than or equal to zero, or None')
        if isinstance(vis_years, (str, float)):
            raise ValueError('Invalid input was provided: '
                             'vis_years must be a whole positive number or None.')

        return vis_years

    def _validate_island_map(self, island_map):
        """Validate input type island_map before sending to Island class.

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

        str_list = island_map.split()
        length_check = len(str_list[0])

        for element in str_list:
            if len(element) != length_check:
                raise ValueError('Island map must contain an equal amount of columns.')

        return True

    def _validate_hist_specs(self, hist_specs):
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
        if hist_specs is None:
            return True

        error_main_key = False
        error_sub_key = False

        for key in hist_specs:
            if key not in self.hist_spec_pattern:
                error_main_key = True
                break

            for sub_key in hist_specs[key]:
                if sub_key not in self.hist_spec_pattern[key]:
                    error_sub_key = True
                    break

        if any((error_main_key, error_sub_key)):
            raise KeyError(f'Provided key is not allowed in hist_specs. '
                           f'Valid keys are: {self.hist_spec_pattern}')
        else:
            return True

    def _validate_cmax_animals(self, cmax_animals):
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
                raise KeyError(f'{key} is not a legal key in cmax_animals. '
                               f'Legal keys are Herbivore and Carnivore.')

        return True

    def _validate_im_params(self, img_dir, img_base, img_fmt, img_years):
        """Private validation of provided image parameters.

        Parameters
        ----------
        img_dir: `str`
            Path to directory for figures
        img_base: `str`
            Beginning of file name for figures
        img_fmt: `str`
            File format for figures
        img_years: `int`
            Years between visualizations saved to files

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
                all((isinstance(img_dir, str), isinstance(img_base, str))),
                all((img_dir is None, img_base is None))
        )):
            raise ValueError('Either both img_dir and img_base must specified or '
                             'neither of them can be specified.')

        if all((img_dir is None, img_years is not None)):
            print('image directory (img_dir) not given. No files will be saved.')

        if img_fmt not in ['jpeg', 'jpg', 'png', 'tif', 'tiff']:
            raise ValueError(f'Image format {img_fmt} not supported. '
                             f'Valid formats are: jpeg, jpg, png, tif, tiff')

        if img_dir is not None:
            if not os.path.isdir(self._img_dir):
                try:
                    os.makedirs(self._img_dir)
                except OSError:
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

    def set_animal_parameters(self, species, params):
        """Set parameters for animal species.

        Parameters
        ----------
        species: {'Herbivore', 'Carnivore'}
            Animal subclass to get its' parameters changed.
        params: `dict`
            Parameter specification for species

        Examples
        -----
        Adjustment of the default parameters are done the following way:
            >>> # Create dictionary for new parameters
            >>> new_params = {'omega': 0.6, 'beta': 1, 'a_half': 35}
            >>>
            >>> # Create a simulation object with necessary input
            >>> sim = BioSim(map_str)
            >>>
            >>> # Set new parameters
            >>> sim.set_animal_parameters('Herbivore', new_params)

        See module for :py:class:`.Animal` for valid parameters.
        """
        if species == 'Herbivore':
            Herbivore.set_params(params)
        elif species == 'Carnivore':
            Carnivore.set_params(params)
        else:
            raise ValueError(f'Cannot specify parameters for animal species {species}: '
                             f'Provided species must be in ["Herbivore", "Carnivore"]')

        msg = f'set_animal_parameters{species, params}'
        logger.info(msg)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape types.

        Parameters
        ----------
        landscape: {'L', 'H'}
            Landscape letter describing :py:attr:`.landscape_type`.
        params: `dict`
            Parameter specification for landscape type.

        Examples
        -----
        Adjustment of the default parameters are done the following way:
            >>> # Create dictionary for new parameter
            >>> new_params = {'f_max': 700}
            >>>
            >>> # Create a simulation object with necessary input
            >>> sim = BioSim(map_str)
            >>>
            >>> # Set new parameters
            >>> sim.set_animal_parameters('L', new_params)

        Parameters can only be set for lowland ('L') and highland ('H') landscape types.
        See module for :py:class:`.Landscape` for valid parameters.
        """
        if landscape == 'L':
            Landscape.set_params({'f_max': {'Lowland': params['f_max']}})
        elif landscape == 'H':
            Landscape.set_params({'f_max': {'Highland': params['f_max']}})
        else:
            raise ValueError(f'Cannot specify parameters for landscape type {landscape}: '
                             f'Provided landscape type must be in ["L", "H"]')

        msg = f'set_landscape_parameters {landscape, params}'
        logger.info(msg)

    def add_population(self, population):
        """Add population on island.

        Parameters
        ----------
        population: `list` of `dict`
            Population of animals to be placed in specified locations on the island.

        Returns
        -------
        None
            Return None if no initial population is given.

            Otherwise add population on island.

        See Also
        --------
        :py:class:`.BioSim`: for correct making of :math:`\mathtt{population}` (see parameter :math:`\mathtt{ini\_pop}`)
        :py:meth:`.add_population_in_location`: Relationship
        """
        if not isinstance(population, (list, type(None))):
            raise TypeError('Explicitly added population must be provided as a list. '
                            'For more information see documentation.')
        if population:
            self.island.add_population_in_location(population)
            num_animals, num_herbivores, num_carnivores = 0, 0, 0

            for dictionary in population:
                num_animals += len(dictionary['pop'])

                for animal in dictionary['pop']:
                    if animal['species'] == 'Herbivore':
                        num_herbivores += 1
                    if animal['species'] == 'Carnivore':
                        num_carnivores += 1

            self._num_animals += num_animals
            self._num_animals_per_species['Herbivore'] += num_herbivores
            self._num_animals_per_species['Carnivore'] += num_carnivores
        else:
            return None

        msg = f'add_population {population}'
        logger.info(msg)

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

        logger.info('make_movie started')

    def simulate(self, num_years=10):
        """Run simulation and gather information.

        Notes
        -----
        The simulation takes all animals trough the :py:meth:`._annual_cycle`,
        gathers data using :py:meth:`_collect_annual_data`, and sends requested data
        to the :py:class:`.Graphics` module, performed by method :py:meth:`_do_annual_graphics`.

        Parameters
        ----------
        num_years: `int`
            Number of years to simulate.
        """
        logger.info('Simulation started')

        if self._initial_num_year is None:
            self._initial_num_year = num_years
            self._num_years = num_years
            start_loop = 0
        else:
            self._initial_num_year = num_years
            start_loop = self.year
            self._num_years = self.year + num_years

        if self._vis_years is not None:
            if self._vis_years > 0:
                if self._initial_num_year % self._vis_years != 0:
                    raise ValueError('Number of simulated years must be a multiple of vis_years')

        for current_year in range(start_loop, self._num_years):
            self._year += 1
            self._annual_cycle()
            msg = f'Annual cycle for {current_year} completed'
            logger.info(msg)

            self._collect_annual_data()
            msg = f'Collection of annual data for {current_year} completed '
            logger.info(msg)

            self._do_annual_graphics(current_year)
            msg = f'Production of annual graphics for {current_year} completed'
            logger.info(msg)

            self._num_animals_per_species = {'Herbivore': self.population_map_herbivore.sum(),
                                             'Carnivore': self.population_map_carnivore.sum()}
            self._num_animals = self.population_map_herbivore.sum() + \
                                self.population_map_carnivore.sum()

            msg = f'Completed year:{current_year} ' \
                  f'Herbivores:{self.population_map_herbivore.sum()}   ' \
                  f'Carnivores:{self.population_map_carnivore.sum()}'
            logger.info(msg)

            print('\r',
                  f'Year:{current_year}  Herbivores:{self.population_map_herbivore.sum()}   '
                  f'Carnivores:{self.population_map_carnivore.sum()}',
                  end='')

        print()

    def _annual_cycle(self):
        """Simulate one cycle of evolution on the island."""
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
        """Generate data for each year simulated.

        Generate data for heatmaps, population size and histograms.
        """
        # Generate data for heatmaps
        self.population_map_herbivore = self.island.get_property_map('v_size_herb_pop')
        self.population_map_carnivore = self.island.get_property_map('v_size_carn_pop')

        # Generate data for population size
        self.population_size_herbivore.append(self.population_map_herbivore.sum())
        self.population_size_carnivore.append(self.population_map_carnivore.sum())

        # Generate data for histograms
        herbivore_object_map = self.island.get_property_map_objects('v_herb_properties_objects')
        carnivore_object_map = self.island.get_property_map_objects('v_carn_properties_objects')

        object_maps = [herbivore_object_map, carnivore_object_map]
        for species in object_maps:
            acc_list = []
            with np.nditer(species, flags=['multi_index', 'refs_ok']) as it:
                for element in it:
                    list_on_location = element.item()
                    if list_on_location:
                        acc_list += list_on_location

            if species is herbivore_object_map:
                self.herbivore_age_weight_fitness = np.asarray(acc_list)
            if species is carnivore_object_map:
                self.carnivore_age_weight_fitness = np.asarray(acc_list)

    def _do_annual_graphics(self, current_year):
        """Decide how the current year's graphics shall be provided,
        and send data to :py:class:`.Graphics`.

        Parameters
        ----------
        current_year: `int`
            Current year being simulated
        """
        pause = 0.2
        show = False
        save = False

        if self._vis_years == 0:
            show = False
        elif self._vis_years is None:
            if (current_year + 1) == self._num_years:
                pause = 3
                show = True
        elif self._vis_years >= 1:
            if (current_year + 1) % self._vis_years == 0:
                pause = 1 / self._vis_years
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
