from .animals import Herbivore


class Lowland:
    """
    Doc-strings
    """

    params = {
        'f_max': 800.0,
        'F': 10.0
    }

    def __init__(self, num_herb):
        self.f_max = self.params['f_max']  # Maximum available fodder
        self.fodder = self.params['f_max']  # Initial amount of fodder

        self.herb_pop = [Herbivore() for _ in range(num_herb)]  # List containing all alive herbivores in one location

    def grassing(self):
        """
        Function handling the animals eating in correct order
        """
        F_satisfied = self.params['F']
        # Sort list, highest fitness first:
        for herbivore in sorted(self.herb_pop, key=lambda x: x.fitness, reverse=True):

            if self.fodder >= F_satisfied:
                herbivore.eat(F_satisfied)  # Gains weight
                self.fodder -= F_satisfied  # Adjust available fodder

            elif self.fodder > 0:  # More than zero, but less than F_satisfied
                herbivore.eat(self.fodder)
                self.fodder = 0

            else:
                break  # No reason to continue looping if there are no more fodder available.


    # vars(self.f_max) (https://www.programiz.com/python-programming/methods/built-in/vars)

    def give_birth:
        for herbivore in self.herb_pop():
            herbivore.giving_birth()

    def regrowth(self):
        """
        Method to reset the amount of fodder by the end of the year
        """
        self.fodder = self.f_max # Check if this is a pointer or a copy

    def death(self):
        def survivors(pop):
            return [animal for animal in pop if not animal.probability_of_death()]

        self.herb_pop = survivors(self.herb_pop)




