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
def test_init_f_max_grass(terrain_letter, terrain):
    """Test that f_max for lowland and highland are correct parameter values."""
    assert Landscape(terrain_letter).f_max == Landscape.params['f_max'][terrain]


@pytest.mark.parametrize('terrain', ['D', 'W'])
def test_init_f_max_zero(terrain):
    """Test that f_max for desert and water are equal to zero only."""
    assert Landscape(terrain).f_max == 0


@pytest.mark.parametrize('terrain', ['L', 'W', 'D', 'W'])
def test_initial_fodder(terrain):
    """Test that initial amount of fodder is equal to f_max."""
    location_cell = Landscape(terrain)
    assert location_cell.fodder == location_cell.f_max


@pytest.mark.parametrize('terrain', ['L', 'W', 'D', 'W'])
def test_initial_population_type(terrain):
    """Test that initial population type is a list."""
    assert all([type(Landscape(terrain).herb_pop) == list, type(Landscape(terrain).carn_pop) == list])


@pytest.mark.parametrize('terrain', ['L', 'W', 'D', 'W'])
def test_inital_population(terrain):
    """Test for no initial population. An emtpy list returns False"""
    assert not all([Landscape(terrain).herb_pop, Landscape(terrain).carn_pop])


### TODO: Is any of this valuable?
@pytest.mark.parametrize('terrain_letter, terrain', [('L', 'Lowland'), ('H', 'Highland')]) #TODO: Not water here!
def test_grassing_fodder_adjustment(terrain_letter, terrain):
    """Test fodder adjustment when grassing in Lowland and Highland while there are still fodder available.
    #Fitness rangering: H(12.5, 10), H(half), H(0)"""
    herbivores = [Herbivore(12.5, 10), Herbivore(0, 3),
                  Herbivore(Herbivore.params['w_half'], Herbivore.params['a_half'])]

    location_cell = Landscape(terrain_letter)
    location_cell.herb_pop += herbivores
    location_cell.grassing()

    assert location_cell.fodder < Landscape.params['f_max'][terrain]


@pytest.mark.parametrize('terrain_letter, terrain', [('L', 'Lowland'), ('H', 'Highland'), ('D', 'Desert')])
def test_grassing_break_statement(terrain_letter, terrain):
    # TODO: How?
    pass

def test_correct_eating_order():
    """Test correct eating order.""" #TODO: Denne referer ikke til koden. Hvordan gjøre dette?
    first_eater = Herbivore(12.5, 10)
    second_eater = Herbivore(Herbivore.params['w_half'], Herbivore.params['a_half'])
    third_eater = Herbivore(0, 3)

    herbivores = [second_eater, third_eater, first_eater]
    sorted_herbivores = [herbivore for herbivore in sorted(herbivores, key=lambda x: x.fitness, reverse=True)]

    assert sorted_herbivores == [first_eater, second_eater, third_eater]


@pytest.mark.skip
def test_grassing_no():
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
    pass

