import pytest
from biosim.animals import Herbivore

#  Overall parameters for probabilistic tests
SEED = 12345678  # random seed for tests

@pytest.mark.skip('Not finished')
def test_set_params():
    pass
    # old
    # new
    # Sammenlign etter å ha kjørt prossedyren

#@pytest.mark.skip('Not finished')
def test_count_new_herbi():
    x = Herbivore.instance_count # Sjekker status i klassen
    Herbivore.count_new_herbi() # kaller prossedyren
    assert Herbivore.instance_count == x + 1 # Sjekker om tellevariabel har økt
    # Tilbakestilling
    Herbivore.instance_count = x


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

@pytest.mark.skip('Not finished')
def test_eat():
    pass

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
        a.aging()
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


