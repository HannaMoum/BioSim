import math
import random


class Animal:
    pass


# class Herbivore(Animal):
class Herbivore:

    herbivores = []

    params = {
        'w_birth': 8,
        'sigma_birth': 1.5,
        'beta': 0.9,
        'eta': 0.05, # Mindre eller lik 1
        'a_half': 40.0,
        'phi_age': 0.6,
        'w_half': 10.0,
        'phi_weight': 0.1,
        'mu': 0.25,
        'gamma': 0.2,
        'zeta': 3.5,
        'xi': 1.2,
        'omega': 0.4,
        'F': 10.0
    }
    """"
    Legg inn doc-string
    """


    @classmethod
    def set_params(cls, new_params):
        """
        Set class parameters.

        Parameters
        ----------
        new_params : dict
            Legal keys: ''

        Raises
        ------
        ValueError, KeyError
        """
        # cls.params.update(new_params)

        #  Checks if key in new_params exists in params
        for key in new_params:
            if key not in params:
                raise KeyError('Invalid parameter name: ' + key)
            if not all(value >= 0 for value in new_params.values()):
                raise ValueError('Invalid value for parameter: ' + key)
            if key == 'eta':
                if not 0 <= new_params['eta'] <= 1:
                    raise ValueError('eta must be in [0, 1].')
                cls.eta = new_params['eta']

            cls.params[key] = new_params[key]




    @classmethod
    def all_alive_herbivores(cls, self):  # Liste av alle herbivores
        """
        :param self: Classobject
        Adds the current classobject to list herbivores
        """
        cls.herbivores.append(self)

    @classmethod
    def herbivores_list(cls):
        """ When called, this function returns a complete list of all herbivores
        (currently just one area)
        """
        return cls.herbivores

    def __init__(self, age=0, weight=None, loc=None):
        """Legg til doc-string."""
        self.age = age

        birth_weight = self.find_birthweight()

        if weight is None:
            self.weight = birth_weight
        else:
            self.weight = weight

        self.loc = loc
        self.count_herbivores()  # Adding this herbivore to the list og all herbivores

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
        # return self.weight

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

    def probability_to_give_birth(self):
        """
        Function giving the probability for giving birth
        (number_of_herbivores is the number of herbivores before the breeding season starts)
        N = number of herbivores. Dette må komme fra lowland klassen, som har oversikt over hvor mange dyr det er i cellen.
        """
        probability = min(1, self.params['gamma'] * self.fitness * (len(self.herbivores) - 1))
        r = random.uniform(0, 1)

        if r < probability:
            if self.weight < self.params['zeta'] * (self.params['w_birth'] + self.params['sigma_birth']):
                return False
            else:
                return True
        else:
            return False

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
            if w * self.params['xi'] > self.weight:
                # > or >= (in if statement)
                #   Hvis vektene er like, får mora 0 i vekt... Skal det være mulig å gi fødsel da?
                # del newborn
                return None
                # TODO: Make sure this removes w from the list of Herbivores.
                # If it doesn't - kill it right away
            else:
                # lose weight
                self.weight -= self.weight * self.params['xi']
                return newborn
        return None

    def probability_of_death(self):
        """ Decides wether animal dies """
        probability = self.params['omega'] * (1 - self.fitness)  # Blir dette riktig måte å hente ut fitness-verdien på?
        r = random.uniform(0, 1)

        if self.weight <= 0:
            return True  # Dyret dør
            # Evt. delete animal
        return r < probability

    @classmethod
    def death(cls):
        """
        Requires call: Herbivore.death()
        Kill all animals that must die according to probability_to_die at once
        :return:
        """
        dead_animals = {animal for animal in cls.herbivores if animal.probability_to_die()}
        cls.herbivores = list(set(cls.herbivores) - dead_animals)

    # Or...


    def kill_only_one_herbivore(self):
        """
        Todo: We should probably delete this one
        self: Current classobject
        Kills only one animal at a time

        - Transfer to script:

        For one: animal.kill_only_one_herbivore(animal)
        For several:
        dead_animals = {animal for animal in list_of_herbivores if animal.probability_to_die()}
        for animal in dead_animals:
            Herbivore.death(animal)

        NOTE! In this case must all dead animals be collected in a set before they are removed.
              We cannot remove elements from a list while iterating trough it
        """
        self.herbivores.remove(self)






