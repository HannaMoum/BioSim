import pytest
from biosim.animals import Herbivore
from biosim.lowland import Landscape

#  Overall parameters for probabilistic tests
SEED = 12345678  # random seed for tests


@pytest.fixture(autouse=True)
def reset_params_default():
    """Reset parameters to default after test has run."""
    yield
    Landscape.set_params(Landscape._default_params)

@pytest.mark.parametrize('terrain, value', [('Highland', 200.0), ('Lowland', 400.0)])
def test_set_single_params(terrain, value):
    """Test optional change of default parameters, singles."""
    Landscape.set_params({'f_max': {terrain: value}})
    assert Landscape.params['f_max'][terrain] == value


def test_set_all_params():
    """Test optional change of default parameters, multiple."""
    new_params = {'f_max': {'Highland': 200.0, 'Lowland': 400.0}}
    Landscape.set_params(new_params)
    assert Landscape.params == new_params


@pytest.mark.parametrize('terrain', ['L', 'H', 'D', 'W'])
def test_init_landscape_type(terrain):
    """Test correct save of input value to Landscape class."""
    assert Landscape(terrain).landscape_type == terrain


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])
def test_init_is_migratable(terrain):
    """Test that correct terrains are migratable."""
    assert Landscape(terrain).is_migratable


def test_init_is_not_migratable():
    """Test that water is not migratable."""
    assert not Landscape('W').is_migratable

@pytest.mark.parametrize('terrain_letter, terrain', [('L', 'Lowland'), ('H', 'Highland')])
def test_init_f_max(terrain_letter, terrain):
    """Test that f_max for lowland and highland are correct parameter values."""
    Landscape.set_params({})
    assert Landscape(terrain_letter).f_max == Landscape.params['f_max'][terrain]


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

