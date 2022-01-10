""" Landscape class with subclasses
"""
from .animals import Animal, Herbivore, Carnivore
from itertools import chain
import random

# TODO: Relative importing does not work. Fix it
# TODO: When finished check that all method names are correct when overriding


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
    """

    # dict: Parameter values for calculations
    params = {
        'f_max': None
    }

    def __init__(self):
        self._fodder = self.params['f_max']  # Initial amount of fodder
        self._herb_pop = []
        self._carn_pop = []

    @property
    def fodder(self):
        """Fodder available in current landscape (`int` or `float`)."""
        return self._fodder

    @fodder.setter
    def fodder(self, value):
        if value > self.params['f_max']:
            raise ValueError('Value must be below f_max')  # Er dette et reelt tilfelle som kan oppstå?
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

    def give_birth(self):
        """For each animal giving birth, update population.

        See Also
        --------
        :py:meth:`.giving_birth`, :py:meth:`.probability_to_give_birth`
        """
        herb_babies = [newborn for individual in self.herb_pop if
                       (newborn := individual.giving_birth('Herbivore', len(self.herb_pop)))]

        carn_babies = [newborn for individual in self.carn_pop if
                       (newborn := individual.giving_birth('Carnivore', len(self.carn_pop)))]

        # TODO: Make absolutely sure this is necessary (again)
        if herb_babies:
            self.herb_pop += herb_babie
        if carn_babies:
            self.carn_pop += carn_babies

    def migration(self):
        """ Create later"""
        pass

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
        self.carn_pop = alive(self.herb_pop)

    def regrowth(self):
        """Reset available fodder in terrain to maximum.

        Regrowth of fodder initially every year.
        """
        self.fodder = self.params['f_max'] #TODO: Include parameters

    def add_animal(self, added_pop):
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
        for animal in added_pop:
            age = animal['age']
            weight = animal['weight']

            if animal['species'] == 'Herbivore':
                self.herb_pop += [Herbivore(age, weight)]
            elif animal['species'] == 'Carnivore':
                self.carn_pop += [Carnivore(age, weight)]
            else:
                raise TypeError(f'{animal} is not a defined animal.\n'
                                f'Defined animals are: {[cls.__name__ for cls in Animal.__subclasses__()]}')


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

    def add_animal(self, added_pop):
        raise AttributeError('Cannot place animals in Water landscape')
        # TODO: Figure out what correct error will be


