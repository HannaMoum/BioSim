from animals import Animal
from animals import Herbivore
from animals import Carnivore
from random import random, choice, sample
from itertools import chain

from dataclasses import dataclass

# Under arbeid
@dataclass
class Params:
    w_birth: float = 6.0
    sigma_birth: float = 1.0
    beta: float = 0.75
    eta: float = 0.0125
    a_half: float = 40.0
    phi_age: float = 0.3
    w_half: float = 4.0
    phi_weight: float = 0.4
    mu: float = 0.4
    gamma: float = 0.8
    zeta: float = 3.5
    xi: float = 1.1
    omega: float = 0.8
    F: float = 50.0
    DeltaPhiMax: float = 10.0


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
    params = {'f_max': {'Highland': 300.0,'Lowland': 800.0}}

    def __init__(self, landscape_type:str):
        self._landscape_type = landscape_type

        if landscape_type == 'W':
            self._is_migratable = False
        else:
            self._is_migratable = True

        if self.landscape_type == 'H':
            self.f_max = self.params['f_max']['Highland']
        elif self.landscape_type == 'L':
            self.f_max = self.params['f_max']['Lowland']
        else:
            self.f_max = 0

        self._fodder = self.f_max  # Initial amount of fodder
        self._population = []
        self._herbivores = []
        self._carnivores = []
        #self._herb_pop = []
        #self._carn_pop = []


    @classmethod
    def set_params(cls, new_params:dict):
        """Set class parameters.
        #TODO: Edit
        new_params: Dict
        params = {'f_max': {'Highland': 300.0,'Lowland': 800.0}}
        new_params = {'f_max': {'Highland': 200.0}}
        Landscape.set_params({'f_max': {'Highland': params['f_max']}})
        """
        if 'f_max' in new_params:
            value_dict = new_params['f_max']
            if 'Highland' in value_dict:
                cls.params = {'f_max': {'Highland': value_dict['Highland'], 'Lowland': cls.params['f_max']['Lowland']}}
            if 'Lowland' in value_dict:
                cls.params = {'f_max': {'Lowland': value_dict['Lowland'], 'Highland': cls.params['f_max']['Highland']}}

    @property
    def landscape_type(self):
        """TODO: Doc, read-only"""
        return self._landscape_type

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
    def population(self)-> list:
        return self._population
    @population.setter
    def population(self, value):
        population_set = set(value)
        contains_duplicates = len(value) != len(population_set)
        if not contains_duplicates:
            self._population = value
            self._herbivores = [animal for animal in value if animal.species == 'Herbivore']
            self._carnivores = [animal for animal in value if animal.species == 'Carnivore']
        else:
            raise ValueError('Population list cant contain duplicates')


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
    def herbivores(self)->list:
        """Returns a list of all animals of species Herbivore"""
        return self._herbivores

    @property
    def carnivores(self) -> list:
        """Returns a list of all animals of species Carnivores"""
        return self._carnivores

    def grassing(self):
        """Feed all herbivores and adjust available fodder.

        Notes
        -----
        Herbivores eat in order of fitness until everyone is satisfied
        or no more fodder is available.
        """
        for animal in sorted(self.population, key=lambda x: x.fitness, reverse=True):
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
        carnivores = self.carnivores
        hunting_order = sample(carnivores, len(carnivores))

        herbivores = self.herbivores
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
                       (newborn := individual.giving_birth('Herbivore', len(herbivores)))]
        carnivores = self.carnivores
        carn_babies = [newborn for individual in carnivores if
                        (newborn := individual.giving_birth('Carnivore', len(carnivores)))]

        # TODO: Make absolutely sure this is necessary (again). YES! Ha en beskyttelse mot tomme lister, lister inni lister, None etc. Konsekvensene av dette er så store.
        if len(herb_babies) > 0:
            self.population += herb_babies
        if len(carn_babies) > 0:
            self.population += carn_babies




    def migration_prep(self):
        """Prepare animal for migration."""
        for animal in self.population:
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

        migrating_herbs = make_migration_dict(self.herbivores)
        migrating_carns = make_migration_dict(self.carnivores)

        return migrating_herbs, migrating_carns


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
        die = [animal for animal in population if animal.dies()]

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
        #TODO: DO not add animals for water landscape
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
