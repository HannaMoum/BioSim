""" Implements Animal model used by subspecies."""

import math
import random
from abc import ABC, abstractmethod  # Remove unless in use


class Animal:
    """Animal with corresponding characteristics and traits for different species.

    Notes
    ------
    Implemented species are :py:class:`.Herbivore` and :py:class:`.Carnivore`. #Move to Sphinx doc(?)

    Parameters
    ----------
    age: `int`
        The animal's age.
    weight: `float`
        The animal's weight.
    """

    # dict: Parameter values for calculations
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
        new_params: dict, optional
            Legal keys: 'w_birth', 'sigma_birth', 'beta',
                        'eta', 'a_half', 'phi_age', 'w_half',
                        'phi_weight', 'mu', 'gamma', 'zeta',
                        'xi', 'omega', 'F',' 'DeltaPhiMax'

        Raises
        -------
        ValueError
            Parameter value is negative
        KeyError
            Parameter key is not a Legal key
        """

        if not all(value >= 0 for value in new_params.values()):
            raise ValueError('Invalid value for parameter: ' + key)

        for key in new_params:
            if key not in cls.params:
                raise KeyError('Invalid parameter name: ' + key)

            if key == 'eta' and not 0 <= new_params['eta'] <= 1:
                raise ValueError('eta must be in interval [0, 1].')

            cls.params[key] = new_params[key]

    def __init__(self, age, weight):
        self._age = age
        self._weight = weight
        self._F_tilde = 0 #TODO: Change name of F_tilde to eaten

    @staticmethod
    def check_positive(value):
        """Command a value to be positive or equal to zero."""
        if value < 0:
            raise ValueError('Value must be positive')

    @staticmethod
    def check_integer(value):
        """Command a value to be an integer type."""
        if not float(value).is_integer():  # Must convert to float to work for integers.
            raise ValueError('Value must be integer')
            # Does not raise correct error if value cannot be converted to float

    @property
    def age(self):
        """The animal's age (`int`).

        A whole, positive number."""
        return self._age

    @age.setter
    def age(self, value):
        self.check_integer(value)
        self.check_positive(value)
        self._age = value

    @property
    def weight(self):
        """The animal's weight (`int` or `float`)."""
        return self._weight

    @weight.setter
    def weight(self, value):
        self.check_positive(value)
        # Må vi kanskje sjekke at dette er float/int eller blir det smør på flesk...
        self._weight = value

    @property
    def F_tilde(self):
        """Food currently eaten this year (`int` or `float`)."""
        return self._F_tilde

    @F_tilde.setter
    def F_tilde(self, value):
        self._F_tilde = value

    @property
    def fitness(self):
        """The animal's fitness (`float`, read-only).

        Notes
        ------
        The fitness is calculated using formula:

        .. math::
            \Phi = \\begin{cases}
                0  & w {\\leq} 0
                \\\ q^+(a, a_{\\frac{1}{2}}, \phi_{age}) * \
                    q^-(w, w_{\\frac{1}{2}},\phi_{weight}) & else
            \\end{cases}

        where a and w is the animal's age and weight respectively, and

        .. math::
            q^{\\pm}(x, x_{\\frac{1}{2}}, \phi) = \
            {\\frac{1}{1+e^{\\pm\phi(x-x_{\\frac{1}{2}})}}}

        For more information see :py:obj:`.params`. #TODO: Change when parameters are updated.
        """

        def q(sgn, x, x_half, phi):
            return 1 / (1 + math.exp(sgn * phi * (x - x_half)))

        if self.weight <= 0:
            return 0
        else:
            q_plus = q(+1, self.age, self.params['a_half'], self.params['phi_age'])
            q_minus = q(-1, self.weight, self.params['w_half'], self.params['phi_weight'])

            return q_plus * q_minus

    def eat(self, food_available):
        """
        Animal gains weight from eating.

        Animal will always eat until satisfied (parameter `F`) or eat **food_available**.
        Weight increase by `Food eaten` :math:`* \\beta`.

        Parameters
        ----------
        food_available: `int` or `float`
            Fodder in current terrain or weight of killed herbivore.
        Returns
        -------
        `int` or `float`
            Food eaten
        """
        wanted_food = self.params['F'] - self.F_tilde
        # Only necessary for Carnivores

        if food_available >= wanted_food:
            eaten = wanted_food
        else:
            eaten = food_available

        self.weight += eaten * self.params['beta']
        self.F_tilde += eaten  # TODO: Is it possible to make this only an attribute for carnivores (F_tilde)

        return eaten  # Only necessary for Herbivores

    def age_and_weightloss(self):
        """Age animal by 1 year and loose weight

        Weight reduces by factor :math:`\\eta`.
        """
        self.age += 1
        self.weight -= self.weight * self.params['eta']

    def migration(self, geography):
        """
        Migrating-function
        """
        pass

    def probability_to_give_birth(self, number_of_animals):
        """
        Decide an animals probability to give birth.

        Parameters
        ----------
        number_of_animals: Int
            Number of animals of chosen species in one cell before breeding season starts.

        Returns
        -------
        bool
            True if animal gives birth
        """

        probability = min(1, self.params['gamma'] * self.fitness * (number_of_animals - 1))
        r = random.uniform(0, 1)

        fertilization = r < probability

        weight_check = self.weight > self.params['zeta'] * \
                 (self.params['w_birth'] + self.params['sigma_birth'])

        birth_weight = random.gauss(self.params['w_birth'], self.params['sigma_birth'])

        maternal_health = self.weight > birth_weight * self.params['xi']

        if all((fertilization, weight_check, maternal_health)):
            return True, birth_weight

        return False, False  # TODO: Find prettier code

    def giving_birth(self, number_of_animals):
        """
        Animals give birth if necessary requirements are met.

        Parameters
        ----------
        number_of_animals: Int
            Number of animals of chosen species in one cell before breeding season starts.

        Returns
        -------
        object
            newborn animal if mother gives birth.
        """

        probability, birth_weight = self.probability_to_give_birth(number_of_animals)

        if probability:
            newborn = Herbivore(0, birth_weight)  # TODO: Should 0 be default?
            # TODO: Fix this so it creates either a herbivore or a Carnivore
            self._weight -= birth_weight * self.params['xi']

            return newborn

        return None

    def probability_of_death(self):
        """
        Decide whether animal dies.
        Returns
        -------
        bool
            True if animal dies.
        """
        starvation = self.weight <= 0

        probability = self.params['omega'] * (1 - self.fitness)
        r = random.uniform(0, 1)
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

        Returns
        -------
        bool
            True of carnivore is hungry
        """
        return self.F_tilde < self.params['F']

    def probability_to_kill(self, herb_fitness):
        """ Deciding whether or not a carnivore will kill the current Herbivore it is hunting"""

        r = random.uniform(0, 1)
        fitness_diff = self.fitness - herb_fitness

        if self.fitness <= herb_fitness:
            return False  # More efficient?
            # probability = 0
        elif 0 < fitness_diff < self.params['DeltaPhiMax']:
            probability = fitness_diff / self.params['DeltaPhiMax']
            # TODO: Make parameters work again
        else:
            probability = 1

        return probability > r

    def killing(self, herb_fitness, herb_weight):
        """
        Sentence
        Parameters
        ----------
        herb_fitness:
        herb_weight: float

        Returns
        -------

        """
        if self.hungry():
            if self.probability_to_kill(herb_fitness):
                self.eat(herb_weight)  # self.F_tilde grows
                return True
            else:
                return False
        else:
            return False
