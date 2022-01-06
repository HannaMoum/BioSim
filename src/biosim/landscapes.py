from .animals import Herbivore


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

    def __init__(self, initial_pop):
        """
        Initial_pop looks like [Herbivore_class, Herbivore_class, ...]
        """
        self.f_max = self.params['f_max']  # Maximum available fodder
        self.fodder = self.params['f_max']  # Initial amount of fodder
        self.herb_pop = initial_pop

    def number_of_current_living_animals(self):
        return len(self.herb_pop)

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

        1. Gå gjennom lista med dyrene
        2. Bruker probability_to_give_birt for å sjekke om det blir født et barn.
            2.1 Barnet fødes via metoden giving_birth. Her oppdateres også vekten til moren.
            2.2 Barnet må legges til i lista over alle herbivores.
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
        # self.fodder = self.params['f_max']






