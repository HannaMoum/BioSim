from biosim.animals import Herbivore  # Should this be a relative import, and not absolute


class Lowland:
    """
    Doc-strings
    """

    params = {
        'f_max': 800.0,
        'F': 10.0
    }

    def __init__(self):
        self.f_max = self.params['f_max']  # Maximum available fodder
        self.fodder = self.params['f_max']  # Initial amount of fodder

    def grassing(self):
        """
        Function handling the animals eating in correct order

        Procedure-draft:
        for Herbivore in sorted list of Herbivores (after fitness-level):
            if self.fodder >= F:
                Herbivore.eat_fodder(F) (!F for Herbivores is 10.0) (gains weight at the same time)
                self.fodder -= F #Adjust available fodder
            elif:
                self.fodder > 0 and self.fodder < F:
                    Herbivore.eat_fodder(self.fodder)
                    self.fodder = 0
            else:
                nothing?
        """
        F_satisfied = self.params['F']
        for herbivore in Herbivore.herbivores_list().sort(key=lambda x: x.fitness, reverse=True):

            if self.fodder >= F_satisfied:
                herbivore.eat(F_satisfied)  # Gains weight
                self.fodder -= F_satisfied  # Adjust available fodder

            elif self.fodder > 0:  # More than zero, but less than F_satisfied
                herbivore.eat(self.fodder)
                self.fodder = 0

            else:
                None  #Is this correct?


    # vars(self.f_max) (https://www.programiz.com/python-programming/methods/built-in/vars)

    def regrowth(self):
        """
        Method to reset the amount of fodder by the end of the year
        """
        self.fodder = self.f_max # Check if this is a pointer or a copy



