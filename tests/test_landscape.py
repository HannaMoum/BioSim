import pytest
from biosim.landscapes import Lowland

#  Overall parameters for probabilistic tests
SEED = 12345678  # random seed for tests

def test_set_params():
    """ Testing change of parameter default value (f_max)"""
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