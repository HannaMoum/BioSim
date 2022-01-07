from .animals import Herbivore
from .animals import Carnivore
import random

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


class Lowland:
    """
    Doc-strings
    """

    # Vi må ha en tom liste med antall herbivores i ruta når vi starter. Denne oppdateres når dyr føder, og dør. (Samt migrerer).
    # Dyrene som lages av klassen herbivore må legges til i denne lista.
    params = {
        'f_max': 800.0
    }

    @classmethod
    def set_params(cls, new_params):
        """
        Function to edit paramteres
        new_params: Dict
        """
        #Should this be run for every simulation? If so, params should be default...
        for key, value in new_params.items():
            if key not in cls.params:
                raise KeyError('Invalid parameter name: ' + key)
            if value < 0:
                raise ValueError('Invalid value for parameter: ' + key)
            cls.params[key] = new_params[key]

    def __init__(self, initial_herb_pop, initial_carn_pop):
        """
        Initial_pop looks like [Herbivore_class, Herbivore_class, ...]
        """
        self._fodder = self.params['f_max']  # Initial amount of fodder
        self._herb_pop = initial_herb_pop
        self._carn_pop = initial_carn_pop

    @property
    def fodder(self):
        return self._fodder
    @fodder.setter
    def fodder(self, value):
        if value > self.params['f_max']:
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
            eaten = herbivore.eat(self.fodder)
            self.fodder -= eaten

            if self.fodder <= 0:
                break
# ---------------------------------------------------------------------------------------------
    @staticmethod
    def hunting_success(herb_fitness, carn_fitness, deltaphimax):
        r = random.uniform(0, 1)
        fitness_diff = (carn_fitness - herb_fitness)

        if carn_fitness <= herb_fitness:
            p = 0
        elif 0 < fitness_diff < deltaphimax:
            p = fitness_diff / deltaphimax
        else:
            p = 1

        return p > r

    def hunting(self):
        """ Carnivores hunting
        """
        # Randomize carn_population because they eat in random order
        hunting_order = random.sample(self.carn_pop, len(self.carn_pop))
        # Sorted list for herbivores based on fitness
        prey_order = sorted(self.herb_pop, key=lambda x: x.fitness)

        for hunter in hunting_order:
            hunter.F_tilde = 0
            for i, prey in enumerate(prey_order):
                if hunter.hungry:
                    if Lowland.hunting_success(prey.fitness,
                                               hunter.fitness,
                                               Params.DeltaPhiMax): # hunter.params['DeltaPhiMax']
                        hunter.eat(prey.weight)
                        del(prey_order[i])
                #else:
                    #break # Stopper hvis ikke hunter er sulten

        self.herb_pop = prey_order # Oppdaterer populasjonen til de som er igjen etter jakten

# ---------------------------------------------------------------------------------------------
    def give_birth(self):
        """
        Every herbivore tries to give birth.
        Expanding self.herb_pop with the new population after all animals have given birth.

        (We might want to adjust the names, and the probability_to_give_birth/giving_birth in Herbivores class,
        for a better code)

        1. Gå gjennom lista med dyrene
        2. Bruker probability_to_give_birt for å sjekke om det blir født et barn.
            2.1 Barnet fødes via metoden giving_birth. Her oppdateres også vekten til moren.
            2.2 Barnet må legges til i lista over alle herbivores.
        """


        # pop_size = len(population)
        population = self.herb_pop
        herb_babies = [newborn for individual in population if
                          (newborn := individual.giving_birth(len(population)))]

        population = self.carn_pop
        carn_babies = [newborn for individual in population if
                       (newborn := individual.giving_birth(len(population)))]

        if len(herb_babies) > 0:
            self.herb_pop += herb_babies
        if len(carn_babies) > 0:
            self.carn_pop += carn_babies



        ## Replaced version
        # new_herbivores =[]
        # for herbivore in self.herb_pop:
        #     newborn = herbivore.giving_birth(number_of_herbivores)
        #
        #     if newborn:  # Checks that newborn is not None
        #         new_herbivores.append(newborn)




    def migration(self):
        """
        Herbivores migrating or staying put
        """
        pass

    def aging(self):
        """
        The herbivores turn one year older and looses weight.
        """
        for herbivore in self.herb_pop:
            herbivore.aging()

        for carnivore in self.carn_pop:
            carnivore.aging()


    def death(self):
        """
        Kill herbivores and adjust self.herb_pop to only contain the living
        """
        alive_herbs = [animal for animal in self.herb_pop if not animal.probability_of_death()]
        alive_carns = [animal for animal in self.carn_pop if not animal.probability_of_death()]
        self.herb_pop = alive_herbs
        self.carn_pop = alive_carns

        # alive = []
        # for animal in self.herb_pop:
        #     if not animal.probability_of_death():
        #         alive.append(animal)
        #
        # self.herb_pop = alive

    def regrowth(self):
        """
        Method to reset the amount of fodder by the end of the year
        """
        self.fodder = self.params['f_max']






