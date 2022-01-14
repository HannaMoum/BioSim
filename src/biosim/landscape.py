from random import random, choice, sample
from copy import deepcopy

from biosim.animals import Animal
from biosim.animals import Herbivore
from biosim.animals import Carnivore


class Landscape:
    """A landscape with corresponding characteristics and traits for different terrains.

    Notes
    ------
    Implemented terrains are 'Lowland', 'Highland', 'Desert', 'Water'.

    Attributes
    ----------
    fodder: `int` or `float`
        Fodder available
    herb_pop: `list` of :py:class:`.animals.Herbivore`.
        Herbivore population
    carn_pop: `list` of :py:class:`.animals.Carnivore`
        Carnivore population
    #TODO: Add new attributes

    Parameters
    ----------
    landscape_type: {'L', 'H', 'D', 'W'}
        Terrain describing the landscape cell
    """

    # dict: Parameter values for calculations
    _default_params = {'f_max': {'Highland': 300.0, 'Lowland': 800.0}}
    params = deepcopy(_default_params)

    def __init__(self, landscape_type: str):
        self._landscape_type = landscape_type
        self._f_max = None
        self._fodder = self.f_max
        self._population = []
        self._herbivores = []
        self._carnivores = []
        self._herbivores_number = 0
        self._carnivores_number = 0

    @classmethod
    def set_params(cls, new_params):
        """Set class parameters.

        Parameters
        ----------
        new_params: `dict`, optional
            Legal keys: 'f_max'
        #TODO: Edit
        params = {'f_max': {'Highland': 300.0,'Lowland': 800.0}}
        Input vil se slik ut fra word: new_params = {'f_max': {'Highland': 200.0}}
        Landscape.set_params({'f_max': {'Highland': params['f_max']}})
        """
        if 'f_max' in new_params:  # Trengs kanskje ikke å sjekkes, sjekk input...
            param_dict = new_params['f_max']
            if not all([value >= 0 for value in param_dict.values()]):
                raise ValueError('f_max must be equal to or greater than zero')
            if 'Highland' in param_dict:
                cls.params['f_max']['Highland'] = param_dict['Highland']
            if 'Lowland' in param_dict:
                cls.params['f_max']['Lowland'] = param_dict['Lowland']

    @property
    def landscape_type(self):
        """The object's landscape type ({'L', 'H', 'D', 'W'}, read-only)."""
        return self._landscape_type

    @property
    def f_max(self):
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
        # TODO: make sure documentation states that f_max is not available for desert and water somewhere
        self._fodder = value

    @property
    def population(self) -> list:
        return self._population

    @population.setter
    def population(self, value):
        population_set = set(value)
        contains_duplicates = len(value) != len(population_set)
        if not contains_duplicates:
            self._population = value
            self._herbivores = [animal for animal in value if animal.species == 'Herbivore']  # Flytt til herbivores
            self._carnivores = [animal for animal in value if animal.species == 'Carnivore']
            self._herbivores_number = len(self._herbivores)
            self._carnivores_number = len(self._carnivores)
        else:
            raise ValueError('Population list can not contain duplicates')  # Når skjer det?

    # @property
    # def herb_pop(self):
    #     """Population of herbivores in current landscape (`list` of :py:class:`.animals.Herbivore`)."""
    #     return self._herb_pop
    #
    # @herb_pop.setter
    # def herb_pop(self, value):
    #     self._herb_pop = value
    #
    # @property
    # def carn_pop(self):
    #     """Population of carnivores in current landscape (`list` of :py:class:`.animals.Carnivore`)."""
    #     return self._carn_pop
    #
    # @carn_pop.setter
    # def carn_pop(self, value):
    #     self._carn_pop = value

    @property
    def herbivores(self) -> list:  # Hvorfor oppdaterer vi ikke de her istedenfor i population?
        """Returns a list of all animals of species Herbivore"""
        return self._herbivores

    @property
    def carnivores(self) -> list:
        """Returns a list of all animals of species Carnivores"""
        return self._carnivores

    @property
    def herbivores_number(self) -> int:
        """Returns a list of all animals of species Herbivores"""
        return self._herbivores_number

    @property
    def carnivores_number(self) -> int:
        """Returns a list of all animals of species Carnivores"""
        return self._carnivores_number

    def grassing(self):
        """Feed all herbivores and adjust available fodder.

        Notes
        -----
        Herbivores eat in order of fitness until everyone is satisfied
        or no more fodder is available.
        """
        for animal in sorted(self.population, key=lambda x: x.fitness, reverse=True):  # TODO: self.herbivores
            if animal.species == 'Herbivore':
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
        carnivores = self.carnivores  # TODO: Skriv self.carnivores rett inn i sorted()
        hunting_order = sample(carnivores, len(carnivores))

        herbivores = self.herbivores  # TODO: Skriv self.herbivores rett inn i sorted()
        prey_order = sorted(herbivores, key=lambda x: x.fitness)

        survivors = []
        for hunter in hunting_order:
            hunter.F_tilde = 0

            survivors = [prey for prey in prey_order if not hunter.killing(prey.fitness, prey.weight)]

        self.population = survivors + hunting_order

    def give_birth(self):
        """For each animal giving birth, update population.

        See Also
        --------
        :py:meth:`.giving_birth`, :py:meth:`.probability_to_give_birth`
        """
        # TODO: Linjene under burde kunne slås sammen til en funksjon
        herbivores = self.herbivores
        herb_babies = [newborn for individual in herbivores if
                       (newborn := individual.giving_birth('Herbivore', self.herbivores_number))]
        carnivores = self.carnivores
        carn_babies = [newborn for individual in carnivores if
                       (newborn := individual.giving_birth('Carnivore', self.carnivores_number))]

        if herb_babies:
            self.population += herb_babies
        if carn_babies:
            self.population += carn_babies

    # def migration_prep(self):
    #     """Prepare animal for migration."""
    #     for animal in self.population:
    #         animal.has_migrated = False

    # def migration_direction(self):
    #     """Finner hvilken retning migreringen skal skje, eller om den skal stå stille"""
    #     #r = uniform(0, 1)
    #     #p = self.fitness * self.params['mu']
    #     if self.herb_pop:
    #     #if p > r: # True betyr at den vil flytte seg
    #         return choice([(-1, 0), (1, 0), (0, 1), (0, -1)]) # Ned (sør), opp (nord), høyre (øst), venstre (vest)
    #     else:
    #         return (0, 0) # Stå stille #TODO: Update to False, if implementerbart...

    # def migrate(self):
    #     """Decide in what direction migrating animals shall move.
    #
    #     Direction is chosen at random between the bordering horizontal and vertical landscape cells."""
    #     def make_migration_dict(species):
    #         migrating_animals = {animal: None for animal in species if animal.probability_to_migrate()}
    #         for animal in migrating_animals.keys():
    #             direction = choice([(-1, 0), (1, 0), (0, 1), (0, -1)])
    #             migrating_animals[animal] = direction
    #             animal.has_migrated = True
    #         return migrating_animals
    #
    #     migrating_herbs = make_migration_dict(self.herbivores)
    #     migrating_carns = make_migration_dict(self.carnivores)
    #
    #     return migrating_herbs, migrating_carns

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
        # TODO: Trenger vel ikke funksjonen når vi bare har en populasjon å forholde oss til. Bør kunne bli en list-comp.
        # def alive(population):
        #     return [animal
        #             for animal in population
        #             if not animal.probability_of_death()]
        #
        # self.population = alive(self.population)
        population = self.population
        survivors = [animal for animal in population if not animal.dies()]
        #die = [animal for animal in population if animal.dies()]

        # print(len(die), len(survivors), len(population))
        # for animal in die:
        #     print(animal.species, animal.id, animal.fitness)

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
        # TODO: DO not add animals for water landscape. Check in island
        for animal in added_pop:
            age = animal['age']
            weight = animal['weight']

            if animal['species'] == 'Herbivore':
                self.population += [Herbivore(weight, age)]
            elif animal['species'] == 'Carnivore':
                self.population += [Carnivore(weight, age)]
            else:
                raise TypeError(f'{animal} is not a defined animal.\n'
                                f'Defined animals are: {[cls.__name__ for cls in Animal.__subclasses__()]}')
