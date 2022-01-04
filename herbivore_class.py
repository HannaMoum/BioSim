import math
import random

class Animal:
    pass

# class Herbivore(Animal):
class Herbivore:

    params = {
        'w_birth':8,
        'sigma_birth': 1.5,
        'beta': 0.9,
        'eta': 0.05,
        'a_half': 40.0,
        'phi_age': 0.6,
        'w_half': 10.0,
        'phi_weight': 0.1,
        'mu': 0.25,
        'gamma': 0.2,
        'zeta': 3.5,
        'xi': 1.2,
        'omega': 0.4,
        'F': 10.0,
        'DeltaPhiMax': None # Sjekk om dette er riktig. Står ingen verdi i tabellen.
    }
    """"
    Legg inn doc-string
    """

    def __init__(self, age = 0, weight = None, loc = None):
        """Legg til doc-string."""
        self.age = age

        birth_weight = self.find_birthweight()

        if weight is None:
            self.weight = birth_weight
        else:
            self.weight = weight

        self.loc = loc

    # @property
    # def weight(self):
    #
    #     return self.weight



    def find_birthweight(self):
        """
        Funksjon som avgjør fødselsvekten basert på mean og standard deviation. Gaussian distribution.
        """
        birthweight = random.gauss(self.params['w_birth'], self.sigma_birth)
        return birthweight


    def eat(self, F_tilde, beta):
        """
        Funksjon som regner ut vektøkningen etter at dyret har spist
        beta*F_tilde
        """
        self.weight += F_tilde * beta
        return self.weight

    #def eat_fodder(self, F_tilde, beta):
    #    """
    #    Call on function "increase_weight_when_eating" and adjust weight
    #    """
    #    pass

    def decrease_weight_when_aging(self, eta):
        """
        Funksjon som regner ut hvor mye vekten minker per år
        eta*weight
        self.weight -= self.weight*eta
        """
        pass

    @property
    def fitness(self, phi_age, phi_weight, a_half, w_half):
        """
        calculate fitness-condition based on age and weight
        (Might use numpy.heaviside function)
        Return "self.fitness"
        """

        fitness = q_plus * q_minus
        if self.weight <= 0:
            return 0
        else:

        pass

    def aging(self):
        """
        After 1 year passed, each herbivore becomes 1 year older
        """
        self.age += 1
        # Sett inn minking av vekt

    def migration(self, geography):
        """
        Migrating-function
        """
        pass

    def probability_to_give_birth(self, gamma, number_of_herbivores):
        """
        Function giving the probability for giving birth
        (number_of_herbivores is the number of herbivores before the breeding season starts)
        """
        pass

    def giving_birth(self, xi):
        """
        function handling the birth of a new herbivore.
        Runs if probability_to_give_birth > random number

        Possible procedure:
        1. Find birthweight of new baby using Gaussian distribution
        birth_weight = random.gauss(
        2. Find mother's weight loss (birthweight * xi)
        3.1 If weight in point 2 is bigger than mother's weight - No new baby, stop giving_birth
        3.2 Else; Adjust mother's weight + create new Herbivore with birthweight found in point 2

        ! Create an attribute (or such) that keeps control of whether this Herbivore has given birth or not
        this year. (self.mother = False/True)!
        """
        # check if it can give birth
        if can_give_birth:
            newborn = Herbivore()
            w = newborn.weight
            # check if the baby is too heavy
            if too_heavy:
                del newborn
                return None
            else:
                # lose weight here
                return newborn
        return None
        pass

    def death(self):
        """
        Function deciding if the Herbivore should die.
        """
        pass



