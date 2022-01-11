from .animals import Herbivore
from .animals import Carnivore
import random
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
    """
    Doc-strings
    """
    params = {'f_max': {'Highland': 300.0,'Lowland': 800.0}}


    def __init__(self, landscape_type):
        """
        Initial_pop looks like [Herbivore_class, Herbivore_class, ...]
        """
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
        self._herb_pop = []
        self._carn_pop = []


    @classmethod
    def set_params(cls, new_params):
        """
        Function to edit paramteres
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
        return self._landscape_type

    @property
    def is_migratable(self):
        return self._is_migratable

    @property
    def fodder(self):
        return self._fodder
    @fodder.setter
    def fodder(self, value):
        if value > self.f_max:
            raise ValueError('Value must be below f_max')
        self._fodder = value

    @property
    def herb_pop(self):
        return self._herb_pop
    @herb_pop.setter
    def herb_pop(self, value):
        self._herb_pop = value

    @property
    def carn_pop(self):
        return self._carn_pop
    @carn_pop.setter
    def carn_pop(self, value):
        self._carn_pop = value

    def grassing(self):
        """
        Function handling the animals eating in correct order
        """
        # Sort list, highest fitness first:
        for herbivore in sorted(self.herb_pop, key=lambda x: x.fitness, reverse=True):
            herbivore.F_tilde = 0
            eaten = herbivore.eat(self.fodder) # Her returneres måltid, dvs. det de har spist
            self.fodder -= eaten

            if self.fodder <= 0:
                break

    @staticmethod
    def hunting_success(herb_fitness, carn_fitness, deltaphimax): # Egen skap ved verden/landskapet ikke ved hver carnivore
        """Probability to kill"""
        r = random.uniform(0, 1)
        fitness_diff = (carn_fitness - herb_fitness)

        if carn_fitness <= herb_fitness:
            p = 0
        elif 0 < fitness_diff < deltaphimax:
            p = fitness_diff / deltaphimax
        else:
            p = 1

        return p > r

    # TODO: Add hunting func from tidying here
    def hunting(self):
        """Carnivores hunt herbivores.

        Adjust population of herbivores.

        See Also
        --------
        :py:meth:`.killing`, :py:meth:`.probability_to_kill`
        """
        hunting_order = random.sample(self.carn_pop, len(self.carn_pop))
        prey_order = sorted(self.herb_pop, key=lambda x: x.fitness)

        for hunter in hunting_order:
            hunter.F_tilde = 0

            survivors = [prey for prey in prey_order if not hunter.killing(prey.fitness, prey.weight)]
            prey_order = survivors

            # Nested version:
            # survivors = []
            # for prey in prey_order:
            #     if not hunter.killing(prey.fitness, prey.weight):
            #         survivors.append(prey)

            # prey_order = survivors

        self.herb_pop = prey_order
    # def hunting(self):
    #     """ Carnivores hunting
    #     """
    #     # Randomize carn_population because they eat in random order
    #     hunting_order = random.sample(self.carn_pop, len(self.carn_pop))
    #     # Bruker sample slik at vi får en ny liste. Ønsker ikke å endre på selve populasjons propertyen, det skal kun gjøres av setteren.
    #     # Ønsker ikke å endre på selve lista.
    #
    #     # Sorted list for herbivores based on fitness
    #     prey_order = sorted(self.herb_pop, key=lambda x: x.fitness)
    #
    #     for hunter in hunting_order:
    #         hunter.F_tilde = 0
    #         for prey in prey_order:
    #             if prey.alive:
    #                 if hunter.hungry:
    #                     if Landscape.hunting_success(prey.fitness,
    #                                                         hunter.fitness,
    #                                                         Params.DeltaPhiMax): # hunter.params['DeltaPhiMax']
    #                                 hunter.eat(prey.weight)
    #                                 prey.alive = False
    #
    #     remaining_prey = []
    #     for herbivore in prey_order:
    #         if herbivore.alive:
    #             remaining_prey.append(herbivore)
    #     self.herb_pop = remaining_prey # Oppdaterer populasjonen til de som er igjen etter jakten

    def give_birth(self):
        """
        Every herbivore tries to give birth.
        Expanding self.herb_pop with the new population after all animals have given birth.

        (We might want to adjust the names, and the probability_to_give_birth/giving_birth in Herbivores class,
        for a better code)

        """
        population = self.herb_pop
        herb_babies = [newborn for individual in population if
                          (newborn := individual.giving_birth('Herbivore', len(population)))]

        population = self.carn_pop
        carn_babies = [newborn for individual in population if
                       (newborn := individual.giving_birth('Carnivore', len(population)))]

        if len(herb_babies) > 0:
            self.herb_pop += herb_babies
        if len(carn_babies) > 0:
            self.carn_pop += carn_babies


    def aging(self):
        """
        The herbivores turn one year older and looses weight.
        """

        for animal in chain(self.herb_pop, self.carn_pop):
            animal.age_and_weightloss()


    def death(self):
        """
        Kill herbivores and adjust self.herb_pop to only contain the living
        """
        alive_herbs = [animal for animal in self.herb_pop if not animal.probability_of_death()]
        alive_carns = [animal for animal in self.carn_pop if not animal.probability_of_death()]

        self.herb_pop = alive_herbs
        self.carn_pop = alive_carns


    def regrowth(self):
        """
        Method to reset the amount of fodder by the end of the year
        """
        self.fodder = self.f_max

    # def add_animal(self, added_pop): # TODO: Add population på verdens nivå må kalle må denne
    #     """ Function adding animals to landscape-object.
    #         Adding animals will be done initially and optionally mid-sim during break.
    #
    #         Input: List of dictionaries as in;
    #          [{'species': 'Herbivore',
    #             'age': 10, 'weight': 12.5},
    #         {'species': 'Herbivore',
    #             'age': 9, 'weight': 10.3}]
    #
    #         Source url for finding all subclass names (read 08.01):
    #         https://stackoverflow.com/questions/3862310/how-to-find-all-the-subclasses-of-a-class-given-its-name"""
    #
    #     for animal in added_pop:
    #         # animal = {'species': H, 'age': _ , 'weight': _ }
    #         age = animal['age']
    #         weight = animal['weight']
    #
    #         if animal['species'] == 'Herbivore':
    #             self.herb_pop += [Herbivore(age, weight)]
    #         elif animal['species'] == 'Carnivore':
    #             self.carn_pop += [Carnivore(age, weight)]
    #         else:
    #             raise TypeError(f'{animal} is not a defined animal.\n'
    #                             f'Defined animals are: {[cls.__name__ for cls in Animal.__subclasses__()]}')







