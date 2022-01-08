""" Lanscape class with subclasses
"""
from .animals import Animal

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

class Lowland(Landscape):
    pass

class Highland(Landscape):
    pass

class Desert(Landscape):
    pass

class Water(Landscape):

    def __init__(self):
        super().__init__() #What difference does this make?... Seems to do the same with and without (in our case)
        #self.fodder = None Må evt. justere fodder.setter i parent class
        self.herb_pop = None
        self.carn_pop = None

a = Water()

print(a._fodder)


