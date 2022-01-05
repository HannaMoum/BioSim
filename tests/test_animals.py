import pytest
from biosim.animals import Herbivore

#  Overall parameters for probabilistic tests
SEED = 12345678  # random seed for tests

@pytest.mark.skip('Not finished')
def test_set_params():
    pass

@pytest.mark.skip('Not finished')
def test_count_new_herbi():
    pass

@pytest.mark.skip('Not finished')
def test_num_herbis():
    pass

@pytest.mark.skip('Not finished')
def test_init():
    pass

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

#@pytest.mark.skip('Not finished')
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


