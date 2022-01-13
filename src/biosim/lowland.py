from random import random, choice, sample
from itertools import chain
from copy import deepcopy

from .animals import Animal
from .animals import Herbivore
from .animals import Carnivore

from dataclasses import dataclass

# Under arbeid
# @dataclass
# class Params:
#     w_birth: float = 6.0
#     sigma_birth: float = 1.0
#     beta: float = 0.75
#     eta: float = 0.0125
#     a_half: float = 40.0
#     phi_age: float = 0.3
#     w_half: float = 4.0
#     phi_weight: float = 0.4
#     mu: float = 0.4
#     gamma: float = 0.8
#     zeta: float = 3.5
#     xi: float = 1.1
#     omega: float = 0.8
#     F: float = 50.0
#     DeltaPhiMax: float = 10.0


class Landscape:
    """A landscape with corresponding characteristics and traits for different terrains.

    Notes
    ------
    Implemented terrains are: :py:class:`.Lowland`, :py:class:`.Highland`,
    :py:class:`.Desert` and :py:class:`.Water`. #Move to Sphinx doc(?)

    Attributes
    ----------
    fodder: `int` or `float`
        Fodder available
    herb_pop: `list` of :py:class:`.animals.Herbivore`.
        Herbivore population
    carn_pop: `list` of :py:class:`.animals.Carnivore`
        Carnivore population
    #TODO: Add new attributes
    """

    # dict: Parameter values for calculations
    _default_params = {'f_max': {'Highland': 300.0, 'Lowland': 800.0}}
    params = deepcopy(_default_params)

    def __init__(self, landscape_type):
        self._landscape_type = landscape_type

        if landscape_type == 'W':
            self._is_migratable = False
        else:
            self._is_migratable = True

        self._f_max = None

        self.fodder = self.f_max  # Initial amount of fodder
        self._herb_pop = []
        self._carn_pop = []

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
        if 'f_max' in new_params:
            param_dict = new_params['f_max']
            if 'Highland' in param_dict:
                cls.params['f_max']['Highland'] = param_dict['Highland']
            if 'Lowland' in param_dict:
                cls.params['f_max']['Lowland'] = param_dict['Lowland']

    @property
    def landscape_type(self):
        """TODO: Doc, read-only"""
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
    def is_migratable(self):
        """TODO: Doc, read-only"""
        return self._is_migratable

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
    def herb_pop(self):
        """Population of herbivores in current landscape (`list` of :py:class:`.animals.Herbivore`)."""
        return self._herb_pop

    @herb_pop.setter
    def herb_pop(self, value):
        self._herb_pop = value

    @property
    def carn_pop(self):
        """Population of carnivores in current landscape (`list` of :py:class:`.animals.Carnivore`)."""
        return self._carn_pop

    @carn_pop.setter
    def carn_pop(self, value):
        self._carn_pop = value

    def grassing(self):
        """Feed all herbivores and adjust available fodder.

        Notes
        -----
        Herbivores eat in order of fitness until everyone is satisfied
        or no more fodder is available.
        """
        for herbivore in sorted(self.herb_pop, key=lambda x: x.fitness, reverse=True):
            herbivore.F_tilde = 0
            eaten = herbivore.eat(self.fodder)
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
        hunting_order = sample(self.carn_pop, len(self.carn_pop))
        prey_order = sorted(self.herb_pop, key=lambda x: x.fitness)

        for hunter in hunting_order:
            hunter.F_tilde = 0

            survivors = [prey for prey in prey_order if not hunter.killing(prey.fitness, prey.weight)]
            prey_order = survivors

        self.herb_pop = prey_order

    def give_birth(self):
        """For each animal giving birth, update population.

        See Also
        --------
        :py:meth:`.giving_birth`, :py:meth:`.probability_to_give_birth`
        """
        herb_pop = self.herb_pop
        herb_babies = [newborn for individual in herb_pop if
                       (newborn := individual.giving_birth('Herbivore', len(herb_pop)))]

        carn_pop = self.carn_pop
        carn_babies = [newborn for individual in carn_pop if
                       (newborn := individual.giving_birth('Carnivore', len(carn_pop)))]

        # TODO: Make absolutely sure this is necessary (again)
        if len(herb_babies) > 0:
            self.herb_pop += herb_babies
        if len(carn_babies) > 0:
            self.carn_pop += carn_babies

    def migration_prep(self):
        """Prepare animal for migration."""
        for animal in self.herb_pop + self.carn_pop:
            animal.has_migrated = False

    # def migration_direction(self):
    #     """Finner hvilken retning migreringen skal skje, eller om den skal stå stille"""
    #     #r = uniform(0, 1)
    #     #p = self.fitness * self.params['mu']
    #     if self.herb_pop:
    #     #if p > r: # True betyr at den vil flytte seg
    #         return choice([(-1, 0), (1, 0), (0, 1), (0, -1)]) # Ned (sør), opp (nord), høyre (øst), venstre (vest)
    #     else:
    #         return (0, 0) # Stå stille #TODO: Update to False, if implementerbart...

    def migrate(self):
        """."""
        def make_migration_dict(species):
            migrating_animals = {animal: None for animal in species if animal.probability_to_migrate()}
            for animal in migrating_animals.keys():
                direction = choice([(-1, 0), (1, 0), (0, 1), (0, -1)])
                migrating_animals[animal] = direction
                animal.has_migrated = True
            return migrating_animals

        migrating_herbs = make_migration_dict(self.herb_pop)
        migrating_carns = make_migration_dict(self.carn_pop)

        return migrating_herbs, migrating_carns



    def aging(self):
        """Age all animals by one year.

        See Also
        --------
        :py:meth:`.age_and_weightloss`: Relationship
        """
        for animal in chain(self.herb_pop, self.carn_pop):
            animal.age_and_weightloss()

    def death(self):
        """Remove dying animals.

        See Also
        --------
        :py:meth:`probability_of_death`
        """
        def alive(species):
            return [individual for individual in species if not individual.probability_of_death()]

        self.herb_pop = alive(self.herb_pop)
        self.carn_pop = alive(self.carn_pop)

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
        #TODO: DO not add animals for water landscape
        for animal in added_pop:
            age = animal['age']
            weight = animal['weight']

            if animal['species'] == 'Herbivore':
                self.herb_pop += [Herbivore(weight, age)]
            elif animal['species'] == 'Carnivore':
                self.carn_pop += [Carnivore(weight, age)]
            else:
                raise TypeError(f'{animal} is not a defined animal.\n'
                                f'Defined animals are: {[cls.__name__ for cls in Animal.__subclasses__()]}')
