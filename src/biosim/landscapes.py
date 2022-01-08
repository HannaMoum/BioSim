""" Lanscape class with subclasses
"""
# cannot import...?
from .animals import Carnivore

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
            raise ValueError('Value must be below f_max') # Er dette et reelt tilfelle som kan oppstå?
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


class Lowland(Landscape):
    """ Adopts:
    __init__ (+getters and setters)
    grassing()
    """
    pass

class Highland(Landscape):
    """ Adopts:
    __init__ (+getters and setters)
    grassing()
    """
    pass

class Desert(Landscape):
    """ Adopts:
    __init__ (+getters and setters)

    """
    def grassing(self):
        pass

    pass

class Water(Landscape):
    """ None of the above functions apply to Water.
    1. Is it enough to set attributes to None or
    2. Do we have to pass every method from Parent-class

    Thoughts: If we dont pass, grassing() vil try to sort None -> Error
    """
    def __init__(self):
        super().__init__() #What difference does this make?... Seems to do the same with and without (in our case)
        #self.fodder = None Må evt. justere fodder.setter i parent class
        self.herb_pop = None
        self.carn_pop = None

    def grassing(self):
        pass
###############################
a = Water()
a.grassing()

print(a._fodder)


