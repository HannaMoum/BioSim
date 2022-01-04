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


    def find_birthweight(self):
        """
        Funksjon som avgjør fødselsvekten basert på mean og standard deviation. Gaussian distribution.
        """
        birthweight = random.gauss(self.params['w_birth'], self.params['sigma_birth'])
        return birthweight


    def eat(self, F_tilde):
        """
        Funksjon som regner ut vektøkningen etter at dyret har spist
        beta*F_tilde
        """
        # Sjekk om det er tilgjengelig mat i cellen.
        # Om det ikke er det spiser dyret 0.
        # Om matenmengden er mindre enn ønskelig mengde spiser den all maten i cellen.
        # Om matmengden er mer enn ønskelig spiser dyret det den ønsker.
        self.weight += F_tilde * self.params['beta']
        return self.weight


    @staticmethod
    def _q(sgn, x, x_half, phi):
        """
        Legg inn doc-string
        sgn = fortegnet i regnestykket (+1 eller -1)
        """
        return 1/(1 + math.exp(sgn * phi * (x - x_half)))


    @property
    def fitness(self):
        """
        calculate fitness-condition based on age and weight
        (Might use numpy.heaviside function)
        Return "self.fitness"
        """

        q_plus = self._q(+1, self.age, self.params['a_half'], self.params['phi_age'])
        q_minus = self._q(-1, self.weight, self.params['w_half'], self.params['phi_weight'])

        if self.weight <= 0:
            return 0
        else:
            return q_plus * q_minus



    def decrease_weight_when_aging(self):
        """
        Funksjon som regner ut hvor mye vekten minker per år
        eta*weight
        self.weight -= self.weight*eta
        """
        self.weight -= self.weight * self.params['eta']
        return self.weight

    def aging(self):
        """
        After 1 year passed, each herbivore becomes 1 year older
        """
        self.age += 1
        self.weight = self.decrease_weight_when_aging() # Kan man hete ut vekten fra den forrige metoden på denne måten?
        #Har testet -> Ja, ser ut til å fungere

    def migration(self, geography):
        """
        Migrating-function
        """
        pass

    def probability_to_give_birth(self, num_of_species_in_cell):
        """
        Function giving the probability for giving birth
        (number_of_herbivores is the number of herbivores before the breeding season starts)
        N = number of herbivores. Dette må komme fra lowland klassen, som har oversikt over hvor mange dyr det er i cellen.
        """
        probability = min(1, self.params['gamma'] * self.fitness * (num_of_species_in_cell - 1))
        r = random.uniform(0, 1)

        if r < probability:
            return True
        if self.weight < self.params['zeta'] * (self.params['w_birth'] + self.params['sigma_birth']):
            return False
        else:
            return False #TODO: Hvorfor er denne her - er dette riktig?

    def giving_birth(self):
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
        if self.probability_to_give_birth():
            newborn = Herbivore()
            w = newborn.weight
            # check if the baby is too heavy
            if w > self.weight: #TODO: Burde være *xi her vel?
                # del newborn
                return None
                # TODO: Make sure this removes w from the list of Herbivores.
                # If it doesn't - kill it right away
            else:
                # lose weight
                self.weight -= self.weight * self.params['xi']
                return newborn
        return None #TODO: Make sure this is correct... Necessary at all?


    def probability_of_death(self):
        probability = self.params['omega'] * (1 - self.fitness) # Blir dette riktig måte å hente ut fitness-verdien på?
        r = random.uniform(0, 1)

        if self.weight <= 0:
            return True  # Dyret dør
            # Evt. delete animal
        if r < probability:
            return True
        else:
            return False

    def death(self):
        """
        Function deciding if the Herbivore should die.
        """
        if self.probability_of_death():
            # Should we delete this animal?
            pass



