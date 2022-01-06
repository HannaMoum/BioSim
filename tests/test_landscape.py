import pytest
from biosim.landscapes import Lowland
from biosim.animals import Herbivore

#  Overall parameters for probabilistic tests
SEED = 12345678  # random seed for tests

def test_set_params():
    """ Testing change of parameter default value (f_max)
        Testing raise of error if wrongful params have been given"""
    #Split in severeal? Keep as one?...
    wanted_param = {'f_max': 600}
    wrongful_param = {'f_min': 600}
    wrongful_value = {'f_max': -600}

    Lowland.set_params(wanted_param)
    new_param = Lowland.params['f_max']
    assert wanted_param['f_max'] == new_param

    with pytest.raises(KeyError):
        Lowland.set_params(wrongful_param)

    with pytest.raises(ValueError):
        Lowland.set_params(wrongful_value)

def test_init_fodder():
    pass

def test_init_herb_pop():
    pass

def test_grassing():
    """
    Test they are eating in correct order (test sorting-funtion)
    Test for weightgain after eating?
    Test for the correctly updated value of fodder
    Test that a loop break happens under correct circumstances
    """
    #herbivores = [Herb]
    grass = Lowland()