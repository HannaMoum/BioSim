from random import sample
from copy import deepcopy

from biosim.animals import Animal, Herbivore, Carnivore


class Landscape:
    """A landscape with corresponding characteristics and traits for different terrains.

    Notes
    ------
    Implemented terrains are 'Lowland', 'Highland', 'Desert' and 'Water'.

    Attributes
    ----------
    fodder: `int` or `float`
        Fodder currently available.
    f_max: `int` or `float`
        Total amount of fodder available.
    population: `list`
        All animals in current landscape.

    Parameters
    ----------
    landscape_type: {'L', 'H', 'D', 'W'}
        Terrain describing the landscape cell.
    """

    _default_params = {'f_max': {'Highland': 300.0, 'Lowland': 800.0}}

    # Changeable parameters values by option set to default values
    params = deepcopy(_default_params)

    def __init__(self, landscape_type):
        self._landscape_type = landscape_type
        self._f_max = None
        self._fodder = self.f_max
        self._population = []

    @classmethod
    def set_params(cls, new_params):
        """Set class parameters.

        Parameters
        ----------
        new_params: `dict` of `str`, optional
            Legal keys: 'f_max' followed by `Highland` or `Lowland`, or both.
        """
        param_dict = new_params['f_max']
        if not all([value >= 0 for value in param_dict.values()]):
            raise ValueError('f_max must be equal to or greater than zero')
        if 'Highland' in param_dict:
            cls.params['f_max']['Highland'] = param_dict['Highland']
        if 'Lowland' in param_dict:
            cls.params['f_max']['Lowland'] = param_dict['Lowland']

    @property
    def landscape_type(self):
        """The object's landscape type ({'L', 'H', 'D', 'W'}, read-only).

        L: Lowland, H: Highland, D: Desert, W: Water."""
        return self._landscape_type

    @property
    def f_max(self):
        """Total amount of fodder available every year in one terrain (`int` or `float`).

        :math:`\mathtt{f\_max}` is changeable by option for landscapes Lowland and Highland,
        but set to zero for Desert and Water."""
        if self.landscape_type == 'H':
            self._f_max = self.params['f_max']['Highland']
        elif self.landscape_type == 'L':
            self._f_max = self.params['f_max']['Lowland']
        else:
            self._f_max = 0

        return self._f_max

    @property
    def fodder(self):
        """Fodder available in current landscape (`int` or `float`)."""
        return self._fodder

    @fodder.setter
    def fodder(self, value):
        if value > self.f_max:
            raise ValueError('Value must be below f_max')
        self._fodder = value

    @property
    def population(self):
        """All animals in current landscape (`list`)."""
        return self._population

    @population.setter
    def population(self, value):
        self._population = value

    @property
    def herbivores(self):
        """All animals of species Herbivore in current landscape (`list`, read-only)."""
        herbivores = [animal for animal in self.population if animal.species == 'Herbivore']
        return herbivores

    @property
    def carnivores(self):
        """All animals of species Carnivore in current landscape (`list`, read-only)."""
        carnivores = [animal for animal in self.population if animal.species == 'Carnivore']
        return carnivores

    @property
    def herbivores_number(self):
        """The number of herbivores in current landscape (`int`, read-only)."""
        herbivores_number = len(self.herbivores)
        return herbivores_number

    @property
    def carnivores_number(self):
        """The number of carnivores in current landscape (`int`, read-only)."""
        carnivores_number = len(self.carnivores)
        return carnivores_number

    def grassing(self):
        """Feed all herbivores and adjust available fodder.

        Notes
        -----
        Herbivores eat in order of fitness until everyone is satisfied
        or no more fodder is available.
        """
        for animal in sorted(self.herbivores, key=lambda x: x.fitness, reverse=True):
            animal.F_tilde = 0
            eaten = animal.eat(self.fodder)
            self.fodder -= eaten

            if self.fodder <= 0:
                break

    def hunting(self):
        """Carnivores hunt herbivores.

        Adjust population of herbivores.

        See Also
        --------
        :py:meth:`.killing`, :py:meth:`.probability_to_kill`
        """
        hunting_order = sample(self.carnivores, self.carnivores_number)

        prey_order = sorted(self.herbivores, key=lambda x: x.fitness)

        for hunter in hunting_order:
            hunter.F_tilde = 0

            survivors = [prey for prey in prey_order if not hunter.killing(prey.fitness, prey.weight)]
            prey_order = survivors

        self.population = prey_order + hunting_order

    def give_birth(self):
        """For each animal giving birth, update population.

        See Also
        --------
        :py:meth:`.giving_birth`, :py:meth:`.probability_to_give_birth`
        """
        def create_newborns(species, num_animals, species_list):
            newborns = [newborn for individual in species_list if
                        (newborn := individual.giving_birth(species, num_animals))]
            return newborns

        herbivore_babies = create_newborns('Herbivore', self.herbivores_number, self.herbivores)
        carnivore_babies = create_newborns('Carnivore', self.carnivores_number, self.carnivores)

        if herbivore_babies:
            self.population += herbivore_babies
        if carnivore_babies:
            self.population += carnivore_babies

    def aging(self):
        """Age all animals by one year.

        See Also
        --------
        :py:meth:`.age_and_weightloss`: Relationship
        """
        for animal in self.population:
            animal.age_and_weightloss()

    def do_death(self):
        """Remove dying animals.

        See Also
        --------
        :py:meth:`probability_of_death`
        """
        population = self.population
        survivors = [animal for animal in population if not animal.dies()]

        self.population = survivors

    def regrowth(self):
        """Reset available fodder in terrain to maximum.

        Regrowth of fodder initially every year.
        """
        self.fodder = self.f_max

    def add_animals(self, added_pop):
        """Add animals to current location.

        Parameters
        ----------
        added_pop: `list` of `dict`
            Added population of chosen species in current location.

        Raises
        -------
        TypeError
            Added animal does not exist.

        References
        ----------
        [1]_ https://stackoverflow.com/questions/3862310/how-to-find-all-the-subclasses-of-a-class-given-its-name
        (read 08.01)
        """
        if self.landscape_type == 'W':
            raise ValueError('Can not add animals into a water landscape.')
        for animal in added_pop:
            age = animal['age']
            weight = animal['weight']

            if animal['species'] == 'Herbivore':
                self.population += [Herbivore(weight, age)]
            elif animal['species'] == 'Carnivore':
                self.population += [Carnivore(weight, age)]
            else:
                raise ValueError(f'{animal} is not a defined animal.\n'
                                 f'Defined animals are: {[cls.__name__ for cls in Animal.__subclasses__()]}')
