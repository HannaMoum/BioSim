""" Lanscape class with subclasses
"""
# cannot import...?
from .animals import Carnivore
from itertools import chain

# TODO: When finished check that all method names are correct when overriding
class Landscape:
    params = {
        'f_max': None
    }

    def __init__(self):
        """
        Initial_pop looks like [Herbivore_class, Herbivore_class, ...]
        """
        self._fodder = self.params['f_max']  # Initial amount of fodder
        self._herb_pop = []
        self._carn_pop = []

    @property
    def fodder(self):
        return self._fodder

    @fodder.setter
    def fodder(self, value):
        if value > self.params['f_max']:
            raise ValueError('Value must be below f_max')  # Er dette et reelt tilfelle som kan oppstå?
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
            eaten = herbivore.eat(self.fodder)  # Her returneres måltid, dvs. det de har spist
            self.fodder -= eaten

            if self.fodder <= 0:
                break

    def hunting(self):
        """ Add later"""
        pass

    def give_birth(self):
        """
        Every herbivore tries to give birth.
        Expanding self.herb_pop with the new population after all animals have given birth.

        (We might want to adjust the names, and the probability_to_give_birth/giving_birth in Herbivores class,
        for a better code)

        """

        herb_babies = [newborn for individual in self.herb_pop if
                       (newborn := individual.giving_birth(len(self.herb_pop)))]

        carn_babies = [newborn for individual in self.carn_pop if
                       (newborn := individual.giving_birth(len(self.carn_pop)))]

        if len(herb_babies) > 0:  # TODO: Make absolutely sure this is necessary (again)
            self.herb_pop += herb_babies
        if len(carn_babies) > 0:
            self.carn_pop += carn_babies

    def migration(self):
        """ Create later"""
        pass

    def aging(self):
        """
        All animals turn one year older and looses weight.
        """

        for animal in chain(self.herb_pop, self.carn_pop):
            animal.age_and_weightloss()

    def death(self):
        """
        Kill herbivores and adjust self.herb_pop to only contain the living
        """
        def alive(species):
            return [individual for individual in species if not individual.probability_of_death()]

        self.herb_pop = alive(self.herb_pop)
        self.carn_pop = alive(self.herb_pop)

        #alive_herbs = [animal for animal in self.herb_pop if not animal.probability_of_death()]
        #alive_carns = [animal for animal in self.carn_pop if not animal.probability_of_death()]
        #self.herb_pop = alive_herbs
        #self.carn_pop = alive_carns

    def regrowth(self):
        """
        Method to reset the amount of fodder by the end of the year
        """
        self.fodder = self.params['f_max'] #TODO: Include parameters

    def add_animal(self, herb_pop, carn_pop):
        """ Function adding animals to landscape-object.
            Adding animals will be done initially and optionally mid-sim during break."""
        # Should not be necessary to check len > 0
        self.herb_pop += herb_pop
        self.carn_pop += carn_pop

class Lowland(Landscape):
    """ Adopts:
    * __init__ (+getters and setters)
    * grassing()
    * hunting()
    * give_birth()
    * migration()
    * aging
    * death
    * regrowth
    * add_animal()
    """
    pass


class Highland(Landscape):
    """ Adopts:
    * __init__ (+getters and setters)
    * grassing()
    * hunting()
    * give_birt()
    * migration()
    * aging
    * death
    * regrowth
    * add_animal()
    """
    pass


class Desert(Landscape):
    """ Adopts:
    __init__ (+getters and setters)
    * hunting()
    * give_birt()
    * migration()
    * aging
    * death
    * add_animal()
    """

    def grassing(self):
        """ No fodder available in the desert.
         Should be faster than feeding herbivores with 0 fodder (or at all open the function)"""
        pass

    def regrowth(self):
        """ No need to reset f_max to 0"""
        pass


class Water(Landscape):
    """ None of the above functions apply to Water.
    1. Is it enough to set attributes to None or
    2. Do we have to pass every method from Parent-class

    Thoughts: If we dont pass, grassing() vil try to sort None -> Error

    1. Do we call all functions for water classes during year cycle, or do we only cycle for the other classes?
    2. If we only cycle for the other landscapes, we still need to make sure a user cannot explicitly run
        f.ex. aging for water
    """

    def __init__(self):
        super().__init__()  # What difference does this make?... Seems to do the same with and without (in our case)
        # self.fodder = None Må evt. justere fodder.setter i parent class
        self.herb_pop = None
        self.carn_pop = None

    def grassing(self):
        pass

    def hunting(self):
        pass

    def give_birth(self):
        pass

    def migration(self):
        pass

    def aging(self):
        pass

    def death(self):
        pass

    def regrowth(self):
        pass

    def add_animal(self, herb_pop, carn_pop):
        raise AttributeError('Cannot place animals in Water landscape')
        # TODO: Figure out what correct error will be
###############################
a = Water()
a.grassing()

print(a._fodder)
