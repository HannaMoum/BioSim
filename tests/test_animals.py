"""Tests for animal class, concerning both herbivores and carnivores."""
import pytest
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
def test_animal_create_age(species):
    """Test initial age of animal."""
    newborn = species(5)
    animal_int = species(weight=12.5, age=10)
    animal_float = species(weight=12.5, age=10.0)
    assert all((newborn.age == 0, animal_int.age == 10, animal_float.age == 10.0))


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_animal_create_age_wrong(species):
    """Test control of input age."""
    negative_age = -1
    float_age = 5.6
    string_age = 'age'

    with pytest.raises(ValueError):
        all([species(12.5, negative_age), species(12.5, float_age), species(12.5, string_age)])


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_animal_create_weight(species):
    """Test initial weight of animal."""
    animal = species(weight=12.5, age=10)
    assert animal.weight == 12.5

# self._age = age
# self._weight = weight
# self._F_tilde = 0 #TODO: Change name of F_tilde to eaten
# self._has_migrated = False
#@pytest.mark.skip('Not finished')
def test_num_herbis():
    x = Herbivore.instance_count  # Sjekker status i klassen
    assert x == Herbivore.num_herbis()  # kaller funksjonen


#@pytest.mark.skip('Not finished')
def test_init_class_variables():
    x = Herbivore.instance_count
    a = Herbivore()
    assert Herbivore.instance_count == x + 1

#@pytest.mark.skip('Not finished')

    #assert a.__dict__ == {'_age': 0, '_weight': None, 'loc': None}

#@pytest.mark.skip('Not finished')
def test_animal_create():
    """
    Test that a new animal has age 0.
    """
    a = Herbivore(2, 10)
    assert a._age == 2
    assert a._weight == 10


@pytest.mark.skip('Not finished')
def test_find_birthweight():
    pass

#@pytest.mark.skip('Not finished')
def test_eat():
    """ Test weightgain when eating"""
    herbivore = Herbivore(10, 12.5)
    initial_weight = herbivore._weight

    food_available = Lowland.params['f_max']
    herbivore.eat(food_available)
    final_weight = herbivore._weight
    weight_gain = Herbivore.params['F'] * Herbivore.params['beta']

    assert initial_weight + weight_gain == final_weight


@pytest.mark.skip('Not finished')
def test__q():
    assert _q()

@pytest.mark.skip('Not finished')
def test_fitness():
    pass

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


