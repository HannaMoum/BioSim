import pytest
from biosim.animals import Herbivore, Carnivore
from biosim.lowland import Landscape

#  Overall parameters for probabilistic tests
SEED = 12345678  # random seed for tests


@pytest.fixture(autouse=True)
def reset_params_defaul_land():
    """Reset parameters to default after test has run."""
    yield
    Landscape.set_params(Landscape._default_params)
    Herbivore.set_params(Herbivore._default_params)
    Carnivore.set_params(Carnivore._default_params)



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


@pytest.mark.parametrize('terrain', ['L', 'H', 'D', 'W'])
def test_initial_fodder(terrain):
    """Test that initial amount of fodder is equal to f_max."""
    location_cell = Landscape(terrain)
    assert location_cell.fodder == location_cell.f_max


@pytest.mark.parametrize('terrain', ['L', 'H', 'D', 'W'])
def test_initial_population_type(terrain):
    """Test that initial population type is a list."""
    assert all([type(Landscape(terrain).herb_pop) == list, type(Landscape(terrain).carn_pop) == list])


@pytest.mark.parametrize('terrain', ['L', 'H', 'D', 'W'])
def test_inital_population(terrain):
    """Test for no initial population. An emtpy list returns False"""
    assert not all([Landscape(terrain).herb_pop, Landscape(terrain).carn_pop])


### TODO: Is any of this valuable? HOW TO AVOID ADDING ANIMALS TO WATER
@pytest.mark.parametrize('terrain_letter, terrain', [('L', 'Lowland'), ('H', 'Highland')])  # TODO: Not water here!
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
    """Test correct eating order."""  # TODO: Denne referer ikke til koden. Hvordan gjøre dette?
    first_eater = Herbivore(12.5, 10)
    second_eater = Herbivore(Herbivore.params['w_half'], Herbivore.params['a_half'])
    third_eater = Herbivore(0, 3)

    herbivores = [second_eater, third_eater, first_eater]
    sorted_herbivores = [herbivore for herbivore in sorted(herbivores, key=lambda x: x.fitness, reverse=True)]

    assert sorted_herbivores == [first_eater, second_eater, third_eater]


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])  # ! No water
def test_hunting_no_carnivores(terrain):
    """Test for sorted updated herbivore population with the same amount of herbivores,
    when no carnivores are present."""
    first_prey = Herbivore(0, 3)
    second_prey = Herbivore(Herbivore.params['w_half'], Herbivore.params['a_half'])
    third_prey = Herbivore(12.5, 10)
    preys = [second_prey, third_prey, first_prey]

    location_cell = Landscape(terrain)
    location_cell.herb_pop += preys
    location_cell.hunting()

    assert location_cell.herb_pop == [first_prey, second_prey, third_prey]


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])  # ! No water
def test_hunting_no_killing(terrain):
    """Test for steady herbivore population, if no killing takes place.
    Parameter adjustments assures no killing (no hungry carnivores)."""
    Carnivore.set_params({'F': 0})

    preys = [Herbivore(Herbivore.params['w_half'], Herbivore.params['a_half']),
             Herbivore(12.5, 10), Herbivore(0, 3)]
    hunters = [Carnivore(Carnivore.params['w_half'], Carnivore.params['a_half']),
               Carnivore(12.5, 10), Carnivore(0, 3)]

    location_cell = Landscape(terrain)
    location_cell.herb_pop += preys
    location_cell.carn_pop += hunters
    location_cell.hunting()

    assert len(preys) == len(location_cell.herb_pop)


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])  # ! No water
def test_hunting_only_killing(terrain):
    """Test for no herbivore population if all are killed during hunt."""
    Carnivore.set_params({'DeltaPhiMax': 0})
    preys = [Herbivore(0.1, 50) for _ in range(3)]

    hunters = [Carnivore(Carnivore.params['w_half'], Carnivore.params['a_half'])]
    #Needo only one hunter for this...

    location_cell = Landscape(terrain)
    location_cell.herb_pop += preys
    location_cell.carn_pop += hunters
    location_cell.hunting()

    assert not location_cell.herb_pop


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])  # ! No water
def test_all_giving_birth(mocker, terrain):
    """Test correct update of population if all animals give birth."""
    mocker.patch('biosim.animals.uniform', return_value=0)

    Herbivore.set_params({'zeta': 0})
    Carnivore.set_params({'zeta': 0})
    herb_pop = [Herbivore(16, 10) for _ in range(200)]
    carn_pop = [Carnivore(16, 10) for _ in range(200)]

    location_cell = Landscape(terrain)

    location_cell.herb_pop += herb_pop
    location_cell.carn_pop += carn_pop

    location_cell.give_birth()

    assert all([len(location_cell.herb_pop) == len(herb_pop) * 2,
                len(location_cell.carn_pop) == len(carn_pop) * 2])


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])  # ! No water
def test_no_giving_birth(mocker, terrain):
    """Test no update of population if no animals give birth."""
    mocker.patch('biosim.animals.uniform', return_value=1)

    herb_pop = [Herbivore(16, 10) for _ in range(200)]
    carn_pop = [Carnivore(16, 10) for _ in range(200)]

    location_cell = Landscape(terrain)

    location_cell.herb_pop += herb_pop
    location_cell.carn_pop += carn_pop

    location_cell.give_birth()

    assert all([len(location_cell.herb_pop) == len(herb_pop),
                len(location_cell.carn_pop) == len(carn_pop)])


