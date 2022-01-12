"""Tests for animal class, concerning both herbivores and carnivores."""
import pytest
import random
from biosim.animals import Herbivore, Carnivore
from biosim.lowland import Landscape

#  Overall parameters for probabilistic tests
SEED = 12345678  # random seed for tests


@pytest.fixture(autouse=True) #Combine with parameterization?
def reset_params_default():
    """Reset parameters to default after test has run."""
    yield
    Herbivore.set_params(Herbivore.default_params)
    Carnivore.set_params(Carnivore.default_params)

# @pytest.fixture(autouse=True)
# def create_animals(self):
#     """Create herb and carn."""
#     herb = Herbivore(10, 12.5)
#     carn = Carnivore(9, 10.5)


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_set_params(species):
    """Test optional change of default parameters."""
    species.set_params({'beta': 1.2, 'omega': 0.2})
    assert all([species.params['beta'] == 1.2, species.params['omega'] == 0.2])


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_parameter_control(species):
    """Test that only legal parameters and values are allowed."""
    with pytest.raises(ValueError):
        all([species.set_params({'beta': -0.2}), species.set_params({'eta': 1.2}), species.set_params({'alpha': 0.5})])


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
@pytest.mark.parametrize('age', [0, 10, 10.0])
def test_animal_create_age(species, age):
    """Test input age of animal."""
    assert species(12.5, age).age == age


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_animal_default_age(species):
    """Test default age value for newborns."""
    assert species(weight=12.5).age == 0


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
@pytest.mark.parametrize('wrong_age', [-1, 5.6, 'age'])
def test_animal_create_age_wrong(species, wrong_age):
    """Test control of age input if made wrong."""
    with pytest.raises(ValueError):
        species(12.5, wrong_age)


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_animal_create_weight(species):
    """Test initial weight of animal."""
    animal = species(weight=12.5, age=10)
    assert animal.weight == 12.5


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_animal_create_weight_wrong(species):
    """Test control of weight input if made wrong."""
    with pytest.raises(ValueError):
        all([species(weight=-12.5, age=10), species(weight='weight', age=10)])


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_animal_create_F_tilde(species): #TODO: Change name when F-tilde changes name
    """Validate initial value of F-tilde and its' possibility to change."""
    animal = species(12.5, 10)
    eat_amount = 5
    assert all([animal.F_tilde == 0, animal.F_tilde + eat_amount == eat_amount])


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_privacy_F_tilde(species):
    animal = species(12.5, 10)
    eat_amount = 5
    animal.F_tilde = eat_amount #TODO: We can change F_tilde anywhere... Should all getters and setters be _F_tilde?
    pass


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_animal_create_has_migrated(species):
    """Test that has_migrated attribute is set to False when animal is created."""
    assert not species(12.5, 10).has_migrated


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_zero_fitness(species):
    """Test fitness for animal with no weight."""
    assert species(0, 10).fitness == 0


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_fitness_attribute_change(species):
    """Test fitness-formula.

    If age and weight is equal to parameter values a_half and w_half respectively,
     expected fitness is 1/4 exactly."""
    age = species.params['a_half']
    weight = species.params['w_half']

    assert species(weight, age).fitness == 1/4


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_fitness_parameter_change(species):
    """Test fitness-formula.

    If phi_age and phi_weight is set to 0, expected fitness is 1/4 exactly
    (independently of age and weight)."""
    species.set_params({'phi_age': 0, 'phi_weight': 0})
    age = random.randint(0, 100)
    weight = random.uniform(0, 100)
    assert species(weight, age).fitness == 1/4


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_eat_unlimited(species):
    """Test correct weight gain when the amount of food available exceeds that of the animal's hunger."""
    animal_1 = species(12.5, 10)
    animal_2 = species(12.5, 10)
    initial_weight = animal_1.weight

    satisfying_amount_1 = species.params['F']
    satisfying_amount_2 = species.params['F']*2

    animal_1.eat(satisfying_amount_1) and animal_2.eat(satisfying_amount_2)
    weight_gain = species.params['F'] * species.params['beta']

    assert all((animal_1.weight == initial_weight + weight_gain, animal_1.weight == animal_2.weight))


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_eat_limited(species):
    """Test correct weight gain when the amount of food available subceeds that of the animal's hunger."""
    animal = species(12.5, 10)
    initial_weight = animal.weight

    limited_food = species.params['F'] - species.params['F']*0.5  # Make sure we have a positive value
    animal.eat(limited_food)
    weight_gain = limited_food * species.params['beta']
    assert animal.weight == initial_weight + weight_gain


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_eat_F_tilde_grow(species):
    """Test correct growth of attribute F_tilde."""
    pass #assume now "eaten" is correct


@pytest.mark.skip('Not finished')
def test_decrease_weight_when_aging():
    pass

@pytest.mark.skip('Not finished')
def test_aging():
    a = Herbivore()
    num_years = 10
    for n in range(num_years):
        a.age_and_weightloss()
    assert a.age == num_years + 1


@pytest.mark.skip('Not finished')
def test_probability_to_give_birth():
    pass

@pytest.mark.skip('Not finished')
def test_giving_birth():
    pass

@pytest.mark.skip('Not finished')
def test_death():
    pass


