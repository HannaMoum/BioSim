from .animals import Herbivore


class Lowland:
    """
    Doc-strings
    """

    params = {
        'f_max': 800.0
    }

    @classmethod
    def set_params(cls, new_params):
        for key in new_params:
            if key not in cls.params:
                raise KeyError('Invalid parameter name: ' + key)
            if key < 0:
                raise ValueError('Invalid value for parameter: ' + key)
            cls.params[key] = new_params[key]

    def __init__(self, num_herb):
        self.f_max = self.params['f_max']  # Maximum available fodder
        self.fodder = self.params['f_max']  # Initial amount of fodder

        self.herb_pop = [Herbivore() for _ in range(num_herb)]  # List containing all alive herbivores in one location

    def grassing(self):
        """
        Function handling the animals eating in correct order
        """
        # Sort list, highest fitness first:
        for herbivore in sorted(self.herb_pop, key=lambda x: x.fitness, reverse=True):

            eaten = herbivore.eat(self.fodder)
            self.fodder -= eaten

            if self.fodder == 0:
                break

    def give_birth(self):
        """
        Every herbivore tries to give birth.
        Expanding self.herb_pop with the new population after all animals have given birth.

        (We might want to adjust the names, and the probability_to_give_birth/giving_birth in Herbivores class,
        for a better code)
        """
        newborns = []
        for herbivore in self.herb_pop:
            possible_baby = herbivore.giving_birth()
            if possible_baby is not None:
                newborns.append(possible_baby)
        self.herb_pop += newborns

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

    def death(self):
        """
        Kill herbivores and adjust self.herb_pop to only contain the living
        """
        #alive = [animal for animal in self.herb_pop if not animal.probability_of_death()]
        #self.herb_pop = alive
        def survivors(pop):
            """
            Return list of animals that do not die.
            """
            return [animal for animal in pop if not animal.probability_of_death()]

        self.herb_pop = survivors(self.herb_pop)

    def regrowth(self):
        """
        Method to reset the amount of fodder by the end of the year
        """
        self.fodder = self.f_max






