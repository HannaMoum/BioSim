import numpy as np
from random import choice

from biosim.landscape import Landscape



class Island:
    """An island with unique geography and evolution.

    Attributes
    ----------
    base_map: `ndarray` of `str`
        Island map consisting of singular landscape letters.
    migrate_map: `ndarray` of `bool`
        Island map presenting migratable locations.
    object_map: `ndarray` of `obj`
        Island map consisting of :py:class:`.Landscape` object references.

    Parameters
    -----------
    island_map: `str`
        String of {'W', 'D', 'L', 'H'} mapping the entire island's geography.
    """

    def __init__(self, island_map):
        self._base_map = self._make_base_map(island_map)
        self._migrate_map = self._make_migrate_map()
        self._object_map = self._make_object_map()

    @property
    def base_map(self):
        """Map of island consisting of landscape letters (`ndarray` of `str`)."""
        return self._base_map

    @property
    def migrate_map(self):
        """Map of the island's migratable and non-migratable cells (`ndarray` of `bool`)."""
        return self._migrate_map

    @property
    def object_map(self):
        """Map of island consisting of landscape-object references (`ndarray` of `obj`)."""
        return self._object_map

    def _validate_island_map(self, island_map):
        """Validate correct setup of island map string.

        Parameters
        ----------
        island_map: `list` of `str`
            Draft of the island's geography.

            Each element of the list represents a row consisting of landscapeletters.

        Raises
        ------
        ValueError
            * Provided input consists of one or more illegal landscape letter, or
            * outer edges of the island are not uniquely made up landscape Water.

        Returns
        -------
        `bool`
            Return True if ValueError is not risen.
        """
        length = len(island_map[0])
        for line in island_map:
            for letter in line:
                if letter not in 'WHLD':
                    raise ValueError(
                        f'{letter} is not a defined landscape.\n'
                        f'Defined landscapes are: ["Lowland", "Highland", "Desert", "Water"]\n'
                        'respectively given by their belonging capital letter.')

            if not all([line.startswith('W'), line.endswith('W')]):
                raise ValueError('All the islands` outer edges must be of landscape Water.')

        if not island_map[0] == 'W'*length or not island_map[-1] == 'W'*length:
            raise ValueError('All the islands` outer edges must be of landscape Water.')

        return True

    def _make_base_map(self, input_map):
        """Mapping island with respect to each landscape letter.

        Parameters
        ----------
        input_map: `str`
            Geography of island.

            Made up by the letters 'W', 'D', 'L' and 'H' each representing a landscape.

        Returns
        -------
        _build_map: `ndarray` of `str`
            Array containing landscape letters in their respective positions.
        """
        map_list = input_map.split()
        self._validate_island_map(map_list)
        row, col = len(map_list), len(map_list[0])

        build_map = np.empty(shape=(row, col), dtype='str')
        for row_index, row_string in enumerate(map_list):
            for col_index, landscape_letter in enumerate(row_string):
                build_map[row_index, col_index] = landscape_letter

        return build_map

    def _make_migrate_map(self):
        """Create a map mapping all migratable cells (`ndarray` of `bool`)."""
        return self._base_map != 'W'

    def _make_object_map(self):
        """Create map of the island's landscape objects references.

        Returns
        -------
        _island_map_objects: `ndarray` of `obj`
            Array containing landscape objects in their respective positions.
        """
        object_map = np.empty(self._base_map.shape, dtype='object')
        vLandscape = np.vectorize(Landscape)
        object_map[:, :] = vLandscape(self._base_map)

        return object_map

    def add_population_in_location(self, population):
        """Add population in given locations.

        Parameters
        ----------
        population: `list` of `dict`
            Population of animals to be placed in specified locations on the island.

        Raises
        ------
        IndexError
            Provided location does not exist.

        See Also
        ---------
        :py:meth:`.add_animals`
        """
        for dictionary in population:

            row, col = dictionary['loc']
            row -= 1
            col -= 1
            max_r, max_col = self.base_map.shape

            if row < 0 or col < 0:
                raise IndexError('Given locations for adding population must be greater than zero.')

            if row >= max_r or col >= max_col:
                raise IndexError('Given locations for adding population does not exist on the created island.')

            landscape_object = self.object_map[row, col]

            population = dictionary['pop']
            landscape_object.add_animals(population)


    def do_migration(self):
        """Migrate all animals in all terrains."""
        global_migrated_animals = []
        with np.nditer(self.object_map, flags=['multi_index', 'refs_ok']) as it:
            for grid_cell in it:
                current_location = grid_cell.item()

                if current_location.population:
                    local_migrated_animals = []

                    for animal in current_location.population:
                        if animal not in global_migrated_animals:

                            if migrate_to_location := self._get_migration_location(animal, it.multi_index):
                                migrate_to_location.population.append(animal)
                                local_migrated_animals.append(animal)

                    for animal in local_migrated_animals:
                        current_location.population.remove(animal)

                    global_migrated_animals += local_migrated_animals

    def _get_migration_location(self, animal, location_coordinates):
        """Find final destination for a migrating animal.

        Parameters
        ----------
        animal: `obj`
            migrating animal
        location_coordinates: `tuple`
            Row and column of current position

        Returns
        -------
        `obj` or `bool`
            Return landscape cell reference if requirements are met, or return False.
        """
        r, c = location_coordinates
        view = self.migrate_map[r-1:r+2, c-1:c+2]

        if animal.probability_to_migrate():
            direction = choice('NSEW')
            mask = np.array([[False, direction == 'N', False],
                             [direction == 'W', False, direction == 'E'],
                             [False, direction == 'S', False]])
            destination = self.object_map[r - 1:r + 2, c - 1:c + 2][view & mask]
            if destination.size > 0:
                return destination.item()
            else:
                return False
        else:
            return False

    def get_property_map(self, fx_map_type):
        """User interface that provides mapped values from specified methods of the class.

        Notes
        -----
        Function takes method :py:meth:`.v_size_herb_pop` or :py:meth:`.v_size_carn_pop` as input
        and provides a map of the respective populations sizes for every cell on the island.

        Parameters
        ----------
        fx_map_type: {'v_size_herb_pop', 'v_size_carn_pop'}
            Class method
        Returns
        -------
        `ndarray`
            Array mapping chosen property
        """
        return self._make_property_map(getattr(self, fx_map_type))

    def _make_property_map(self, fx: callable(object)):
        """
        Create map of chosen property for :py:meth:`.get_property_map`.

        Parameters
        ----------
        fx: class method
            Method to be vectorized.

        Returns
        -------
        `ndarray`
            Array mapping chosen property.
        """
        property_map = np.empty(self.base_map.shape, dtype=float)
        vget_property = np.vectorize(fx)
        property_map[:, :] = vget_property(self.object_map)
        return property_map

    def v_size_herb_pop(self, location):
        """Find the herbivore population size at given location.

        See Also
        --------
        :py:meth:`.get_property_map`
            Relationship

        Parameters
        ----------
        location: `obj`
            Location on island.

        Returns
        -------
        `int`
            Number of herbivores.
        """
        return location.herbivores_number

    def v_size_carn_pop(self, location):
        """Find the carnivore population size at given location.

        See Also
        --------
        :py:meth:`.get_property_map`
            Relationship

        Parameters
        ----------
        location: `obj`
            Location on island.

        Returns
        -------
        `int`
            Number of carnivores.
        """
        return location.carnivores_number

    def get_property_map_objects(self, fx_map_type):
        """User interface that provides mapped values from specified methods of the class.

        Notes
        -----
        Function takes method :py:meth:`.v_herb_properties_objects` or :py:meth:`.v_carn_properties_objects`
        as input and provides full exposure of the respective animals' attributes age, weight and fitness
        for every cell on the island.

        Parameters
        ----------
        fx_map_type: {'v_herb_properties_objects', 'v_carn_properties_objects'}
            Class method

        Returns
        -------
        `ndarray`
            Array mapping attributes of chosen species.
        """
        return self._make_property_map_objects(getattr(self, fx_map_type))

    def _make_property_map_objects(self, fx: callable(object)):
        """Create mapping of a chosen species' attribuets for :py:meth:`.get_property_map_objects`.

        Parameters
        ----------
        fx: class method
            Method to be vectorized.

        Returns
        -------
        `ndarray`
            Array mapping chosen property.
        """
        property_map = np.empty(self.base_map.shape, dtype=object)
        vget_property = np.vectorize(fx)
        property_map[:, :] = vget_property(self.object_map)
        return property_map

    def v_herb_properties_objects(self, location):
        """Find the herbivores' attributes at given location.

        See Also
        --------
        :py:meth:`.get_property_map_objects`
            Relationship

        Parameters
        ----------
        location: `obj`
            Location on island.

        Returns
        -------
        `list`
            List of attributes for herbivores.
        """
        if location.herbivores:
            characteristics = []
            for animal in location.herbivores:
                characteristics.append((animal.age, animal.weight, animal.fitness))
            return characteristics

    def v_carn_properties_objects(self, location):
        """Find the carnivores' attributes at given location.

        See Also
        --------
        :py:meth:`.get_property_map_objects`
            Relationship

        Parameters
        ----------
        location: `obj`
            Location on island.

        Returns
        -------
        `list`
            List of attributes for carnivores.
        """
        if location.carnivores:
            characteristics = []
            for animal in location.carnivores:
                characteristics.append((animal.age, animal.weight, animal.fitness))
            return characteristics













