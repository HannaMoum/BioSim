import math

class Herbivore:
    """"
    Legg inn doc-string
    """

    def __init__(self, age = 0, weight = None, loc = None):
        self.age = age
        self.weight = weight
        self.loc = loc

    def determine_birthweight(self, w_birth, sigma_birth):
        """
        Funksjon som avgjør fødselsvekten basert på mean og standard deviation. Gaussian dist.
        """
        pass

    def increase_weight_when_eating(self, F_tilde, beta):
        """
        Funksjon som regner ut vektøkningen etter at dyret har spist
        beta*F_tilde
        """
        pass

    def decrease_weight_when_aging(self, eta):
        """
        Funksjon som regner ut hvor mye vekten minker per år
        eta*weight
        """
        pass

    @Property
    def fitness(self, phi_age, phi_weight, a_half, w_half):
        """
        calculate fitness-condition based on age and weight
        (Might use numpy.heaviside function)
        Return "self.fitness"
        """
        pass

    def migration(self):
        """
        Migrating-function
        """
        pass

    def probability_to_give_birth(self, gamma, number_of_herbivores):
        """
        Function giving the probability for giving birth
        """
        pass

