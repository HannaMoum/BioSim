import math

class Herbivore:
    """"
    Legg inn doc-string
    """

    def __init__(self, age = 0, weight = None):
        self.age = age
        self.weight = weight

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

    def fitness(self, phi_age, phi_weight, a_half, w_half):
        """
        calculate fitness-condition based on age and weight
        (Might use numpy.heaviside function)
        """
        pass
