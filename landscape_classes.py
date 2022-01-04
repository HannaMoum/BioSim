
class Lowland():
    """
    Doc-strings
    """
    def __init__(self, f_max=800.0):
        self.f_max = f_max ###
        self.fodder = f_max

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
