import pytest
from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Landscape

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


def test_param_mistake():
    """Test for errormessage if wrongful value are given"""
    new_params = {'f_max': {'Highland': -200.0}}
    with pytest.raises(ValueError):
        Landscape.set_params(new_params)


@pytest.mark.parametrize('terrain', ['L', 'H', 'D', 'W'])
def test_init_landscape_type(terrain):
    """Test correct save of input value to Landscape class."""
    assert Landscape(terrain).landscape_type == terrain


# @pytest.mark.parametrize('terrain', ['L', 'H', 'D'])
# def test_init_is_migratable(terrain):
#     """Test that correct terrains are migratable."""
#     assert Landscape(terrain).is_migratable
#
#
# def test_init_is_not_migratable():
#     """Test that water is not migratable."""
#     assert not Landscape('W').is_migratable


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


@pytest.mark.parametrize('terrain', ['L', 'H'])
def test_legal_changes_of_fodder(terrain):
    """Test legal changes of fodder for lowland og highland with the correct update."""
    landscape_cell = Landscape(terrain)
    landscape_cell.fodder = 200
    assert landscape_cell.fodder == 200


@pytest.mark.parametrize('terrain', ['L', 'H', 'W', 'D'])
def test_illegal_changes_of_fodder(terrain):
    """Test ValueError is risen when illegal changes are made of fodder."""
    landscape_cell = Landscape(terrain)
    with pytest.raises(ValueError):
        landscape_cell.fodder = 900


@pytest.mark.parametrize('terrain', ['L', 'H', 'D', 'W'])
def test_initial_population_type(terrain):
    """Test that initial population type is a list."""
    assert all([type(Landscape(terrain).population) == list,
                type(Landscape(terrain).herbivores) == list,
                type(Landscape(terrain).carnivores) == list])


@pytest.mark.parametrize('terrain', ['L', 'H', 'D', 'W'])
def test_inital_population(terrain):
    """Test for no initial population. An emtpy list returns False"""
    assert not all([Landscape(terrain).population,
                    Landscape(terrain).herbivores,
                    Landscape(terrain).carnivores])


@pytest.mark.parametrize('terrain', ['L', 'H', 'D', 'W'])
def test_initial_pop_count(terrain):
    """Test that initial counter is set to 0."""
    assert all([Landscape(terrain).herbivores_number == 0, Landscape(terrain).carnivores_number == 0])


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])
def test_set_population(terrain):
    """Test correct update of ottribute population."""
    population = [Herbivore(12.5, 10), Carnivore(12.5, 10), Carnivore(9, 25), Herbivore(9, 25)]
    location_cell = Landscape(terrain)
    location_cell.population = population
    assert location_cell.population == population


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])
def test_extract_herbivores(terrain):
    """Test for correct herbivore population."""
    test_pop = [Herbivore(12.5, 10), Carnivore(12.5, 10), Carnivore(9, 25), Herbivore(9, 25)]
    location_cell = Landscape(terrain)
    location_cell.population += test_pop
    assert location_cell.herbivores == [test_pop[0], test_pop[3]]



@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])
def test_herbivores_reduction(terrain):
    """Test for correct herbivore population when population are reduced."""
    animal = Herbivore(12.5, 10)
    test_pop = [animal, Carnivore(12.5, 10), Carnivore(9, 25), Herbivore(9, 25)]

    location_cell = Landscape(terrain)
    location_cell.population += test_pop
    location_cell.population.remove(animal)

    assert location_cell.herbivores == [test_pop[3]]


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])
def test_extract_carnivores(terrain):
    """Test for correct herbivore population."""
    population = [Herbivore(12.5, 10), Carnivore(12.5, 10), Carnivore(9, 25), Herbivore(9, 25)]
    location_cell = Landscape(terrain)
    location_cell.population = population
    assert location_cell.carnivores == [population[1], population[2]]


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])
def test_carnivores_reduction(terrain):
    """Test for correct carnivore population when population are reduced."""
    animal = Carnivore(12.5, 10)
    population = [Herbivore(12.5, 10), animal, Carnivore(9, 25), Herbivore(9, 25)]

    location_cell = Landscape(terrain)
    location_cell.population += population
    location_cell.population.remove(animal)

    assert location_cell.carnivores == [population[2]]


### TODO: HOW TO AVOID ADDING ANIMALS TO WATER
@pytest.mark.parametrize('terrain_letter, terrain', [('L', 'Lowland'), ('H', 'Highland')])  # TODO: Not water here!
def test_grassing_fodder_adjustment(terrain_letter, terrain):
    """Test fodder adjustment when grassing in Lowland and Highland while there are still fodder available."""
    herbivores = [Herbivore(12.5, 10), Herbivore(0, 3),
                  Herbivore(Herbivore.params['w_half'], Herbivore.params['a_half'])]

    location_cell = Landscape(terrain_letter)
    location_cell.population += herbivores
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
    location_cell = Landscape('L')
    location_cell.population += herbivores

    sorted_herbivores = [herbivore for herbivore in sorted(location_cell.population, key=lambda x: x.fitness, reverse=True)]

    assert sorted_herbivores == [first_eater, second_eater, third_eater]


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])  # ! No water
def test_hunting_no_carnivores(terrain):
    """Test for correctly sorted updated herbivore population with the same amount of herbivores,
    when no carnivores are present."""
    first_prey = Herbivore(0, 3)
    second_prey = Herbivore(Herbivore.params['w_half'], Herbivore.params['a_half'])
    third_prey = Herbivore(12.5, 10)
    preys = [second_prey, third_prey, first_prey]

    location_cell = Landscape(terrain)
    location_cell.population += preys
    location_cell.hunting()

    assert location_cell.herbivores == [first_prey, second_prey, third_prey]


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
    location_cell.population += preys + hunters
    location_cell.hunting()

    assert len(preys) == len(location_cell.herbivores)


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])  # ! No water
def test_hunting_only_killing(terrain):
    """Test for no herbivore population if all are killed during hunt."""
    Carnivore.set_params({'DeltaPhiMax': 0})
    preys = [Herbivore(0.1, 50) for _ in range(3)]

    hunters = [Carnivore(Carnivore.params['w_half'], Carnivore.params['a_half'])]

    location_cell = Landscape(terrain)
    location_cell.population += preys + hunters
    location_cell.hunting()

    assert not location_cell.herbivores


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])  # ! No water
def test_all_giving_birth(mocker, terrain):
    """Test correct update of population if all animals give birth."""
    mocker.patch('biosim.animals.uniform', return_value=0)

    Herbivore.set_params({'zeta': 0})
    Carnivore.set_params({'zeta': 0})
    herb_pop = [Herbivore(16, 10) for _ in range(20)]
    carn_pop = [Carnivore(16, 10) for _ in range(20)]

    location_cell = Landscape(terrain)
    location_cell.population += herb_pop + carn_pop
    location_cell.give_birth()

    assert all([len(location_cell.herbivores) == len(herb_pop) * 2,
                len(location_cell.carnivores) == len(carn_pop) * 2,
                len(location_cell.population) == 2 * (len(herb_pop) + len(carn_pop))])


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])  # ! No water
def test_no_giving_birth(mocker, terrain):
    """Test no update of population if no animals give birth."""
    mocker.patch('biosim.animals.uniform', return_value=1)

    herb_pop = [Herbivore(16, 10) for _ in range(20)]
    carn_pop = [Carnivore(16, 10) for _ in range(20)]

    location_cell = Landscape(terrain)
    location_cell.population += herb_pop + carn_pop
    location_cell.give_birth()

    assert all([len(location_cell.herbivores) == len(herb_pop),
                len(location_cell.carnivores) == len(carn_pop),
                len(location_cell.population) == len(herb_pop) + len(carn_pop)])


# @pytest.mark.parametrize('terrain', ['L', 'H', 'D'])  # ! No water
# def test_migration_preparation(terrain):
#     """Test that migration_preparation resets all has_migrated attributes to False."""
#     herb_pop = [Herbivore(16, 10) for _ in range(20)]
#     carn_pop = [Carnivore(16, 10) for _ in range(20)]
#
#     landscape_cell = Landscape(terrain)
#
#     for animal in herb_pop + carn_pop:
#         animal.has_migrated = True
#
#     landscape_cell.herb_pop += herb_pop
#     landscape_cell.carn_pop += carn_pop
#     landscape_cell.migration_prep()
#
#     for animal in landscape_cell.herb_pop + landscape_cell.carn_pop:
#         assert not animal.has_migrated


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])  # ! No water
def test_aging(terrain):
    """Test that all animals in the landscape have lost weight and become older."""
    herb_pop = [Herbivore(12.5, 10) for _ in range(20)]
    carn_pop = [Carnivore(12.5, 10) for _ in range(20)]

    landscape_cell = Landscape(terrain)
    landscape_cell.population += herb_pop + carn_pop
    landscape_cell.aging()

    for animal in landscape_cell.population:
        assert all([animal.age > 10, animal.weight < 12.5])


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])  # ! No water
def test_death_all(terrain):
    """Test no population left in landscape cell if all animals dies due to lack of weight."""
    herb_pop = [Herbivore(0, 10) for _ in range(20)]
    carn_pop = [Carnivore(0, 10) for _ in range(20)]

    landscape_cell = Landscape(terrain)
    landscape_cell.population += herb_pop + carn_pop
    landscape_cell.do_death()

    assert not all([landscape_cell.herbivores, landscape_cell.carnivores, landscape_cell.population])


@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])  # ! No water
def test_no_death(terrain, mocker):
    """Test no change of population in landscape cell if all animals survive."""
    mocker.patch('biosim.animals.uniform', return_value=1)
    herb_pop = [Herbivore(12.5, 10) for _ in range(20)]
    carn_pop = [Carnivore(12.5, 10) for _ in range(20)]

    landscape_cell = Landscape(terrain)
    landscape_cell.population += herb_pop + carn_pop

    landscape_cell.do_death()

    assert all([landscape_cell.herbivores == herb_pop,
                landscape_cell.carnivores == carn_pop,
                landscape_cell.population == herb_pop + carn_pop])


@pytest.mark.parametrize('terrain_letter, terrain', [('L', 'Lowland'), ('H', 'Highland')])
def test_regrowth(terrain_letter, terrain):
    """Test that fodder is reset to f_max when running regrowth method."""
    landscape_cell = Landscape(terrain_letter)
    landscape_cell.fodder = 50
    landscape_cell.regrowth()

    assert landscape_cell.fodder == Landscape.params['f_max'][terrain]


# @pytest.mark.skip
@pytest.mark.parametrize('terrain', ['L', 'H', 'D'])  # ! No water
def test_add_valid_animals(terrain):
    added_pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                 {'species': 'Carnivore', 'age': 10, 'weight': 12.5},
                 {'species': 'Herbivore', 'age': 20, 'weight': 11}]

    landscape_cell = Landscape(terrain)
    landscape_cell.add_animals(added_pop)
    assert landscape_cell.herb_pop[0].age == 10, landscape_cell.her
    # assert all([landscape_cell.herb_pop == [Herbivore(12.5, 10), Herbivore(11, 20)],
    #            landscape_cell.carn_pop == [Carnivore(12.5, 10)]]) #Wrong identities.TODO: In progress

# @pytest.mark.skip
# @pytest.mark.parametrize('terrain', ['L', 'H', 'D'])  # ! No water
# def test_add_invalid_animals(terrain):
#     pass


# def add_animals(self, added_pop):

#     #TODO: DO not add animals for water landscape. Check in island
#     for animal in added_pop:
#         age = animal['age']
#         weight = animal['weight']
#
#         if animal['species'] == 'Herbivore':
#             self.herb_pop += [Herbivore(weight, age)]
#         elif animal['species'] == 'Carnivore':
#             self.carn_pop += [Carnivore(weight, age)]
#         else:
#             raise TypeError(f'{animal} is not a defined animal.\n'
#                             f'Defined animals are: {[cls.__name__ for cls in Animal.__subclasses__()]}')
