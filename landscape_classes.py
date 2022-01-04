import .herbivore_class

class Lowland():
    """
    Doc-strings
    """

    params = {
        'f_max': 800.0,
        'F' : 10.0
    }

    def __init__(self):
        self.f_max = params['f_max'] #Maximum available fodder
        self.fodder = params['f_max'] #Initial amount of fodder

    def grassing(self, some_list_of_Herbivores_in_area, F):
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

        pass

    # Need to reset the amount of fodder by the end of the year. vars(self.f_max) (https://www.programiz.com/python-programming/methods/built-in/vars)

    def regrowth(self):
        self.fodder = self.f_max
