import pytest
from biosim.landscape import Lowland
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
    Test they are eating in correct order (test sorting-funtion) #How?...
    Test for weightgain after eating? #SHOULD BE TESTED IN test_eat, transferred
    Test for the correctly updated value of fodder #test here
    Test that a loop break happens under correct circumstances #test here
    """

    # Test fodder reduction
    herbivores = [Herbivore(10, 12.5), Herbivore(9, 10.3), Herbivore(3, 6.8)]
    loc = Lowland(herbivores)
    loc.grassing()
    # Assumption: Enough food available. Need some adjustments
    assert Lowland.params['f_max'] - len(herbivores)*Herbivore.params['F'] == loc.fodder

    # Transferred this code to test_eat in test_animals instead.
    # Delete everything, should it be tested here...?

    # herbivores_i = [Herbivore(10, 12.5), Herbivore(9, 10.3), Herbivore(3, 6.8)]  # before eating
    # herbivores_f = [Herbivore(10, 12.5), Herbivore(9, 10.3), Herbivore(3, 6.8)]  # after eating
    #
    # #Weightgain
    # gain = Herbivore.params['F'] * Herbivore.params['beta']
    #
    # initial = Lowland(herbivores_i).herb_pop
    #
    # final_loc = Lowland(herbivores_f)
    # final_loc.grassing()
    # final = final_loc.herb_pop
    #
    # for herbivore_i, herbivore_f in zip(initial, final):
    #
    #     assert herbivore_i._weight + gain == herbivore_f._weight
    #pass

