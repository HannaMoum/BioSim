"""Implement Animal model used by subspecies."""

import math
from copy import deepcopy
from random import gauss, uniform


class Animal:
    """Animal with corresponding characteristics and traits for different species.

    Notes
    ------
    Implemented species are :py:class:`.Herbivore` and :py:class:`.Carnivore`.

    Parameters
    ----------
    age: `int` or `float`
        The animal's age.

        Must be a whole number.
    weight: `float`
        The animal's weight.
    """
    params = None

    @classmethod
    def set_params(cls, new_params):
        """Set class parameters.

        Parameters
        ----------
        new_params: `dict`, optional
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

        for key, value in new_params.items():
            if key not in cls.params:
                raise KeyError('Invalid parameter name: ' + key)

            if not value >= 0:
                raise ValueError('Invalid value for parameter: ' + key)

            if key == 'eta' and not 0 <= new_params['eta'] <= 1:
                raise ValueError('parameter eta must be within range [0, 1].')

            cls.params[key] = new_params[key]

    def __init__(self, weight, age=0):

        if not isinstance(weight, (int, float)) or weight < 0:
            raise ValueError('Weight must be a positive number')
        self._weight = weight

        if not float(age).is_integer() or not isinstance(age, (int, float)):
            raise ValueError('Age must be a whole number')
        elif age < 0:
            raise ValueError('Age must be a positive number')

        self._age = age

        self._F_tilde = 0
        self._fitness = self._calculate_fitness()

    @property
    def age(self):
        """The animal's age (`int` or `float`).

        A whole, positive number."""
        return self._age

    @age.setter
    def age(self, value):
        self._age = value
        self._fitness = self._calculate_fitness()

    @property
    def weight(self):
        """The animal's weight (`int` or `float`)."""
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value
        self._fitness = self._calculate_fitness()

    @property
    def F_tilde(self):
        """Food currently eaten this year by the animal (`int` or `float`)."""
        return self._F_tilde

    @F_tilde.setter
    def F_tilde(self, value):
        self._F_tilde = value

    @property
    def fitness(self):
        """The animal's fitness (`float`, read-only)

        See Also
        --------
        :py:meth:`._calculate_fitness`
        """
        return self._fitness

    def _calculate_fitness(self):
        """Calculate the animal's fitness.

        Notes
        ------
        The fitness is calculated using formula:

        .. math::
            \Phi = \\begin{cases}
                0  & w \; {\\leq}\; 0
                \\\ q^+(a, a_{\\frac{1}{2}}, \phi_{age}) * \
                    q^-(w, w_{\\frac{1}{2}},\phi_{weight}) & else
            \\end{cases}

        where a and w is the animal's age and weight respectively, and

        .. math::
            q^{\\pm}(x, x_{\\frac{1}{2}}, \phi) = \
            {\\frac{1}{1+e^{\\pm\phi(x-x_{\\frac{1}{2}})}}}

        For more information see table of parameters.

        Returns
        -------
        fitness: `float`
            The animal's fitness
        """

        def q(sgn, x, x_half, phi):
            return 1 / (1 + math.exp(sgn * phi * (x - x_half)))

        if self.weight <= 0:
            return 0
        else:
            q_plus = q(+1, self.age, self.params['a_half'], self.params['phi_age'])
            q_minus = q(-1, self.weight, self.params['w_half'], self.params['phi_weight'])

            fitness = q_plus * q_minus
            return fitness

    def eat(self, food_available):
        """Animal gains weight from eating.

        Animal will always eat until satisfied (`F`),
        otherwise it will eat :math:`\mathtt{food\_available}`.
        Weight increases by `Food eaten` :math:`* \\beta`.

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

        if food_available >= wanted_food:
            eaten = wanted_food
        else:
            eaten = food_available

        self.weight += eaten * self.params['beta']
        self.F_tilde += eaten

        return eaten

    def age_and_weightloss(self):
        """Age animal by one year and lose weight.

        Weight reduces by factor :math:`\eta`.
        """
        self.age += 1
        self.weight -= self.weight * self.params['eta']

    def probability_to_migrate(self):
        r = uniform(0, 1)
        p = self.fitness * self.params['mu']
        return p > r

    def probability_to_give_birth(self, number_of_animals):
        """Decide the animal's probability to give birth.

        Notes
        ------
        The probability to give birth is

        .. math::

            min(1, \gamma * \Phi * (N-1)).

        The probability is zero if:

        .. math::

             N &= 1

             &or

             w < \zeta(&w_{birth} + \sigma_{birth})

        where
        :math:`\Phi` is the animal's :py:attr:`.fitness`, :math:`w` the :py:attr:`.weight`,\
         and N is :math:`\mathtt{number\_of\_animals}`

        At birth, the mother loses :math:`\\xi` times the birthweight of the baby.
        If this is more than her own weight, no baby is born and mother's weight remain unchanged.

        The baby's birthweight is drawn from a gaussian distribution.
        If the weight drawn is less than zero, it is treated as miscarriage,
        with no baby born and mother's weight unchanged.

        Gender plays no role in mating.
        Each animal can give birth to at most one offspring every year.

        For more information see table of parameters.

        Parameters
        ----------
        number_of_animals: `int`
            Number of same species in current terrain before breeding season.

        Returns
        -------
        birth_weight: `float` or `bool`
            Birth weight of animal if birth takes place, otherwise False.
        """
        match_probability = min(1, self.params['gamma'] * self.fitness * (number_of_animals - 1))
        r = uniform(0, 1)

        fertilization = r < match_probability

        reached_puberty = self.weight > self.params['zeta'] * \
                          (self.params['w_birth'] + self.params['sigma_birth'])

        birth_weight = gauss(self.params['w_birth'], self.params['sigma_birth'])
        miscarriage = birth_weight < 0

        maternal_health = self.weight > birth_weight * self.params['xi']
        if all((fertilization, reached_puberty, maternal_health, not miscarriage)):
            return birth_weight

        return False

    def giving_birth(self, species, number_of_animals):
        """Animal gives birth and loses weight.

        Animal gives birth if requirements from :py:meth:`.probability_to_give_birth` are met.
        Weight decreases by newborn's weight :math:`*\\xi`
        
        Parameters
        ----------
        species: {'Herbivore', 'Carnivore'}
            Animal of chosen species giving birth.
        number_of_animals: `int`
            Number of same species in current terrain before breeding season.

        Returns
        -------
        newborn: `obj` or None
            Class instance for the newborn animal if parent gives birth, otherwise None.
        """
        birth_weight = self.probability_to_give_birth(number_of_animals)

        if birth_weight:
            if species == 'Herbivore':
                newborn = Herbivore(birth_weight)
            if species == 'Carnivore':
                newborn = Carnivore(birth_weight)

            self.weight -= birth_weight * self.params['xi']
            return newborn

        return None

    def dies(self):
        """Decide whether animal dies.

        Notes
        -----
        An animal dies:
            #. from starvation if its' weight is zero
            #. from sickness with probability :math:`\omega(1-\Phi)`

        Returns
        -------
        `bool`
            True if animal dies, otherwise False.
        """
        starvation = self.weight <= 0

        probability = self.params['omega'] * (1 - self.fitness)
        r = uniform(0, 1)
        sickness = r < probability

        return any((starvation, sickness))


class Herbivore(Animal):
    """Animal species adopting all methods from superclass Animal."""

    species = 'Herbivore'

    _default_params = {
        'w_birth': 8.0,
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

    # Changeable parameter values by option set to default values
    params = deepcopy(_default_params)


class Carnivore(Animal):
    """Animal species adopting all methods from superclass Animal,
    with its' own unique traits added."""

    species = 'Carnivore'

    _default_params = {
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

    # Changeable parameters values by option set to default values
    params = deepcopy(_default_params)

    def hungry(self):
        """Decide whether carnivore is hungry.

        Carnivore is satisfied when it has eaten amount `F`.

        Returns
        -------
        `bool`
            True if carnivore is hungry, False otherwise.
        """
        return self.F_tilde < self.params['F']

    def probability_to_kill(self, herb_fitness):
        """Decide the carnivore's probability to kill a herbivore.

        Notes
        ------

        A carnivore kills a herbivore with probability

        .. math::
            p = \\begin{cases}
                0  & if  \Phi_{carn} \; {\\leq} \; \Phi_{herb}
                \\\ \\frac{\Phi_{carn} - \Phi_{herb}}{\Delta\Phi_{max}} & if\;
                0 < \Phi_{carn}-\Phi_{herb} <\Delta\Phi_{max}
                \\\ 1 & otherwise
            \\end{cases}

        until it has eas eaten an amount `F` or tried to kill every herbivore in its' location.

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
