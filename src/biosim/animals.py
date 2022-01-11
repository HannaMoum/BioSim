import math
from random import random, seed, choice, gauss, sample, uniform
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict

@dataclass
class Animal_params:
    w_birth:        float
    sigma_birth:    float
    beta:           float
    eta:            float
    a_half:         float
    phi_age:        float
    w_half:         float
    phi_weight:     float
    mu:             float
    gamma:          float
    zeta:           float
    xi:             float
    omega:          float
    F:              float


@dataclass
class Herbivore_params:
    w_birth:        float = 8.0
    sigma_birth:    float = 1.5
    beta:           float = 0.9
    eta:            float = 0.05
    a_half:         float = 40.0
    phi_age:        float = 0.6
    w_half:         float = 10.0
    phi_weight:     float = 0.1
    mu:             float = 0.25
    gamma:          float = 0.2
    zeta:           float = 3.5
    xi:             float = 1.2
    omega:          float = 0.4
    F:              float = 10.0

@dataclass
class Carnivore_params:
    mu: float = 0.4


class Animal(ABC):
    params = {
        'w_birth': None,
        'sigma_birth': None,
        'beta': None,
        'eta': None,
        'a_half': None,
        'phi_age': None,
        'w_half': None,
        'phi_weight': None,
        'mu': None,
        'gamma': None,
        'zeta': None,
        'xi': None,
        'omega': None,
        'F': None,
        'DeltaPhiMax': None
    }
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

        #  Checks if key in new_params exists in params
        for key in new_params:
            if key not in cls.params:
                raise KeyError('Invalid parameter name: ' + key)
            if not all(value >= 0 for value in new_params.values()):
                raise ValueError('Invalid value for parameter: ' + key)
            if key == 'eta':
                if not 0 <= new_params['eta'] <= 1:
                    raise ValueError('eta must be in [0, 1].')
            # Update params
            cls.params[key] = new_params[key]


    def __init__(self, age, weight):
        """Legg til doc-string."""

        self._age = age
        self._weight = weight

        # Property for mengde som dyret har spist
        self._F_tilde = 0

        self._has_migrated = False

    @property
    def has_migrated(self):
        return self._has_migrated
    @has_migrated.setter
    def has_migrated(self, bool):
        self._has_migrated = bool

    @staticmethod
    def check_positive(value):
        if value < 0:
            raise ValueError('Value must be positive')

    @staticmethod
    def check_integer(value):
        if not type(value) == int:
            raise ValueError('Value must be integer')

    @property
    def age(self):
        return self._age
    @age.setter
    def age(self, value):
        self.check_integer(value)
        self.check_positive(value)

        self._age = value

    @property
    def weight(self):
        return self._weight
    @weight.setter
    def weight(self, value):
        self.check_positive(value)
        self._weight = value

    @property
    def F_tilde(self):
        """Eaten amount"""
        return self._F_tilde
    @F_tilde.setter
    def F_tilde(self, value):
        self._F_tilde = value

    @property
    def fitness(self):
        """
        calculate fitness-condition based on age and weight
        Return "self.fitness"
        """
        # Maby q as function inside fitness function.

        if self.weight <= 0:
            return 0
        else:
            q_plus = Animal._q(+1, self.age, self.params['a_half'], self.params['phi_age'])
            q_minus = Animal._q(-1, self.weight, self.params['w_half'], self.params['phi_weight'])

            return q_plus * q_minus

    @staticmethod
    def _q(sgn, x, x_half, phi):
        """
        Legg inn doc-string
        sgn = fortegnet i regnestykket (+1 eller -1)
        """
        return 1 / (1 + math.exp(sgn * phi * (x - x_half)))

    def eat(self, food_available):
        """
        Function that makes the animal eat. First step is to check if any fodder/food is available.
        beta*F_tilde
        F_tilde = det som blir spist
        """
        max_måltid = self.params['F'] - self.F_tilde  # Hvor mye plass det er i magen
        if max_måltid < food_available:
            måltid = max_måltid
        else:
            måltid = food_available

        self.weight += måltid * self.params['beta']
        self.F_tilde += måltid

        return måltid

    def age_and_weightloss(self):
        """
        After 1 year passed, each herbivore becomes 1 year older
        """
        self.age += 1
        self.weight -= self.weight * self.params['eta']

    def migration_direction(self):
        """Finner hvilken retning migreringen skal skje, eller om den skal stå stille"""
        r = uniform(0, 1)
        p = self.fitness * self.params['mu']
        if p > r: # True betyr at den vil flytte seg
            return choice([(-1, 0), (1, 0), (0, 1), (0, -1)]) # Ned (sør), opp (nord), høyre (øst), venstre (vest)
        else:
            return (0, 0) # Stå stille



    def migration(self, geography):
        """
        Migrating-function
        """
        pass

    def probability_to_give_birth(self, number_of_animals):
        """
        Function giving the probability for giving birth
        (number_of_herbivores is the number of herbivores before the breeding season starts)
        N = number of herbivores. Dette må komme fra lowland klassen, som har oversikt over hvor mange dyr det er i cellen.
        """

        # probability = min(1, self.params['gamma'] * self.fitness * (self.instance_count - 1))
        # number_of_animals = Lowland.number_of_current_living_animals()
        probability = min(1, self.params['gamma'] * self.fitness * (number_of_animals - 1))

        r = uniform(0, 1)

        befruktning = r < probability  # Sannsynligheten for at det skjer en befruktning

        fertil = self.weight > self.params['zeta'] * (self.params['w_birth'] + self.params[
            'sigma_birth'])  # Denne sannsynligheten ser på om populasjonen tenderer til å ha store barn.

        # Må regne ut birth_weight for å vite om det blir en fødsel. Birth_weight blir tatt videre til __init__ når en ny herbivore opprettes.

        birth_weight = gauss(self.params['w_birth'], self.params['sigma_birth'])  # regner ut fødselsvekt.

        maternal_health = self.weight > birth_weight * self.params[
            'xi']  # Sjekker om moren sin vekt er mer enn det hun vil miste når hun føder.

        if all((befruktning, fertil, maternal_health)):  # Om alle disse kriteriene stemmer vil det skje en fødsel.
            # Returnerer true for å angi at fødsel skjer, og birth_weight fordi denne brukes når en ny herbivore opprettes.
            return birth_weight

        return None  # Se kommentar under giving_birth. Forbedringspotensiale

    def giving_birth(self, species, number_of_animals):
        """
        Animal gives birth and loses weight.

        Animal gives birth if requirements from :py:meth:`.probability_to_give_birth` are met.
        Weight decreases by newborn's weight :math:`*\\xi`

        Parameters
        ----------
        species: `str`
            Species giving birth.
        number_of_animals: `int`
            Number of same species in current terrain before breeding season.

        Returns
        -------
        newborn: `obj` or None
            Class instance for the newborn animal if parent gives birth, otherwise None.
        """
        birth_weight = self.probability_to_give_birth(number_of_animals)  # Kan ikke unpacke uten noen verdien

        if birth_weight:
            if species == 'Herbivore':
                newborn = Herbivore(0, birth_weight)  # TODO: Should 0 be default?
            if species == 'Carnivore':
                newborn = Carnivore(0, birth_weight)

            # lose weight
            self._weight -= birth_weight * self.params['xi']

            return newborn
        return None

    def probability_of_death(self):
        """ Decides whether or not the animal dies """
        starvation = self.weight <= 0
        # Random death
        probability = self.params['omega'] * (1 - self.fitness)
        r = uniform(0, 1)
        sickness = r < probability

        return any((starvation, sickness))


class Herbivore(Animal):

    params = {
        'w_birth': 8,
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
        'F': 10.0
    }
    """"
    Legg inn doc-string
    """



class Carnivore(Animal):
    params = {
        'w_birth': 6.0,
        'sigma_birth': 1.0,
        'beta': 0.75,
        'eta': 0.0125,
        'a_half': 40.0,
        'phi_age': 0.3,
        'w_half': 4.0,
        'phi_weight': 0.4,
        'mu': 0.4,
        'gamma': 0.8,
        'zeta': 3.5,
        'xi': 1.1,
        'omega': 0.8,
        'F': 50.0,
        'DeltaPhiMax': 10.0
    }

    def hungry(self):
        """
        Decide whether carnivore is hungry.

        Carnivore is satisfied when it has eaten amount `F` (parameter). #TODO: fix parameters

        Returns
        -------
        `bool`
            True if carnivore is hungry, False otherwise.
        """
        return self.F_tilde < self.params['F']

    def probability_to_kill(self, herb_fitness):
        """
        Decide the carnivore's probability to kill a herbivore.

        Notes
        ------
        #TODO: Equations

        Parameters
        ----------
        herb_fitness: `float`
            Fitness of the herbivore the carnivore is currently hunting.

        Returns
        -------
        `bool`
            True if the killing can take place, otherwise False.
        """
        r = uniform(0, 1)
        fitness_diff = self.fitness - herb_fitness

        if self.fitness <= herb_fitness:
            return False

        elif 0 < fitness_diff < self.params['DeltaPhiMax']:
            probability = fitness_diff / self.params['DeltaPhiMax']
            # TODO: Make parameters work again
        else:
            probability = 1

        return probability > r

    def killing(self, herb_fitness, herb_weight):
        """Carnivore kills herbivore and eats it.

        Carnivore kills if requirements from :py:meth:`.probability_to_kill` are met,
        and if carnivore is :py:meth:`.hungry`.

        See Also
        --------
        :py:meth:`.eat`
            for eating procedure. Takes :math:`\mathtt{herb\_weight}` as input.

        Parameters
        ----------
        herb_fitness: `float`
            Fitness of herbivore
        herb_weight: `float`
            Weight of herbivore

        Returns
        -------
        `bool`
            True if carnivore kills, otherwise False.
        """
        if self.hungry():
            if self.probability_to_kill(herb_fitness):
                self.eat(herb_weight)
                return True
            else:
                return False
        else:
            return False
