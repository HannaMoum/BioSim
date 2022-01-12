"""Tests for animal class, concerning both herbivores and carnivores."""
import pytest
from biosim.animals import Herbivore, Carnivore
from biosim.lowland import Landscape

#  Overall parameters for probabilistic tests
SEED = 12345678  # random seed for tests

#@pytest.fixture(autouse=True)
def create_animals():
    """Create herb and carn."""
    hebr = Herbivore(10, 12.5)
    carn = Carnivore(9, 10.5)
    pass

def test_set_params():
    """Test optional change of default parameters."""
    #Herbivore.set_params({'beta': 1.2, 'omega': 0.2})
    print(Herbivore.params)
    Herbivore.set_params(Herbivore.params)
    print(Herbivore.params)
    assert Herbivore.params


@pytest.fixture
def reset_params_default():
    #nothing. Hebr or Carn, not Animal
    yield
    Herbivore.set_params(Herbivore.params)
    Carnivore.set_params(Carnivore.params)
    pass

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


