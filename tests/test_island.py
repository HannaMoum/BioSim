import textwrap
import pytest
from biosim.world import World
import numpy as np
from biosim.landscape import Landscape
from biosim.animals import Herbivore, Carnivore

SEED = 12345678  # random seed for tests


@pytest.fixture()
def geogr_str():
    """Create initial island string to be used in other tests."""
    geogr = """\
                    WWWW
                    WLHW
                    WWWW
                """
    geogr = textwrap.dedent(geogr)
    return geogr


# Initial tests, made to run when changes in world has been made


@pytest.mark.parametrize('geogr', ["""\
                                        WWW
                                        WLH 
                                        WWW
                                    """,
                                   """\
                                        WWW
                                        DLW
                                        WWW
                                    """,
                                   """\
                                        WWW
                                        WKW
                                        WWW
                                    """,
                                   """\
                                        WDW
                                        WLW
                                        WWW
                                    """,
                                   """\
                                        WWW
                                        WLW
                                        WHW
                                    """,
                                   """\
                                        WWW
                                        WH
                                        WWW
                                    """
                                   ])
def test_invalid_map_str(geogr):
    """Test ValueError if any map requirements are not met."""
    geogr_wrapped = textwrap.dedent(geogr)
    with pytest.raises(ValueError):
        World(geogr_wrapped)


def test_valid_map_str(geogr_str):
    """Test no ValueErrors are risen when valid map string are given."""
    assert np.all(World(geogr_str))


def test_base_map(geogr_str):
    """Test correct creation and attribute save of base_map."""
    base_map_wanted = [['W', 'W', 'W', 'W'],
                       ['W', 'L', 'H', 'W'],
                       ['W', 'W', 'W', 'W']]
    base_map = World(geogr_str).base_map
    for row_wanted, row in zip(base_map_wanted, base_map):
        for letter_wanted, letter in zip(row_wanted, row):
            assert letter_wanted == letter


def test_migrate_map(geogr_str):
    """Test correct creation and attribute save of migrate_map."""
    migrate_map_wanted = [[False, False, False, False],
                          [False, True, True, False],
                          [False, False, False, False]]
    migrate_map = World(geogr_str).migrate_map
    for row_wanted, row in zip(migrate_map_wanted, migrate_map):
        for wanted_bool, boolean in zip(row_wanted, row):
            assert wanted_bool == boolean


def test_object_map_shape(geogr_str):
    """Test creation of correct size for object_map."""
    island = World(geogr_str)
    assert island.object_map.shape == (3, 4)


def test_object_map_type(geogr_str):
    """Test correct creation of object references by checking their type."""
    island = World(geogr_str)
    for reference_row in island.object_map:
        for reference in reference_row:
            assert type(reference) == Landscape


def test_object_map_reference(geogr_str):
    """Test correct creation of object references by checking their attribute landscape_type."""
    island = World(geogr_str)
    geogr = geogr_str.split()
    for string, reference_row in zip(geogr, island.object_map):
        for letter, reference in zip(string, reference_row):
            assert reference.landscape_type == letter


def test_object_map_coordinate(geogr_str):
    """Test that given coordinates picks out the correct object."""
    island = World(geogr_str)
    assert all([island.object_map[1, 1].landscape_type == 'L',
                island.object_map[1, 2].landscape_type == 'H'])


@pytest.mark.parametrize('location', [(1, -1), (-1, 1), (0, 1), (9, 2), (2, 9)])
def test_add_animals_IndexError(geogr_str, location):
    """Test that IndexError arise if negative coordinates or non-existent coordinates are provided."""
    island = World(geogr_str)
    add_pop = [{'loc': location, 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 5}]}]
    with pytest.raises(IndexError):
        island.add_population(add_pop)


@pytest.mark.parametrize('location', [(2, 2), (2, 3)])
def test_add_animals_success(geogr_str, location):
    """Test that animals are added in the correct locations."""
    island = World(geogr_str)
    add_pop = [{'loc': location, 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 5},
                                         {'species': 'Carnivore', 'age': 6, 'weight': 6.5}]}]
    island.add_population(add_pop)
    row, col = location
    adjust_row = row - 1
    adjust_col = col - 1
    assert all([len(island.object_map[adjust_row, adjust_col].population) == 2,
                len(island.object_map[adjust_row, adjust_col].herbivores) == 1,
                len(island.object_map[adjust_row, adjust_col].carnivores) == 1])


@pytest.mark.parametrize('function_call', ['v_size_herb_pop', 'v_size_carn_pop'])
def test_get_property_map_population_size(geogr_str, function_call):
    """Test get_ and make_property_map for all species by checking expected population,
    in expected location.
    All other cells are expect to contain zero population."""
    island = World(geogr_str)
    add_pop = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 5},
                                       {'species': 'Carnivore', 'age': 6, 'weight': 6.5}]}]
    island.add_population(add_pop)
    species_map = island.get_property_map(function_call)
    zeros = sum(True for sub_array in species_map for number in sub_array if not number)
    row, col = species_map.shape
    expected_zeros = (row * col) - 1

    assert all([species_map[1, 1] == 1, zeros == expected_zeros])


@pytest.mark.parametrize('function_call, species', [('v_herb_properties_objects', Herbivore),
                                                    ('v_carn_properties_objects', Carnivore)])
def test_get_property_map_objects(geogr_str, function_call, species):
    """Test get_ and make_property_map_objects for all species by checking expected
    saved attributes in expected location.
    All other cells are expected to contain None"""
    island = World(geogr_str)
    add_pop = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 6, 'weight': 6.5},
                                       {'species': 'Carnivore', 'age': 6, 'weight': 6.5}]}]
    island.add_population(add_pop)
    attributes = island.get_property_map_objects(function_call)
    nones = sum(True for sub_array in attributes for value in sub_array if not value)
    row, col = attributes.shape
    expected_nones = (row * col) - 1

    assert all([attributes[1, 1] == [(6, 6.5, species(6.5, 6).fitness)], nones == expected_nones])


def test_migration(mocker, geogr_str):
    """Test correct migration of animal by assuring migration will happen in right direction
    and checking expected journey."""
    mocker.patch('biosim.animals.uniform', return_value=0)
    mocker.patch('biosim.world.choice', return_value='E')
    island = World(geogr_str)
    add_pop = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 6, 'weight': 6.5},
                                       {'species': 'Carnivore', 'age': 6, 'weight': 6.5}]}]
    island.add_population(add_pop)
    island.do_migration()

    assert all([island.object_map[1, 2].population,
                len(island.object_map[1, 2].herbivores) == 1,
                len(island.object_map[1, 2].carnivores) == 1])


@pytest.mark.parametrize('direction', ['N', 'S', 'W'])
def test_migration_water(mocker, geogr_str, direction):
    """Test that migration can not happen to water cells."""
    mocker.patch('biosim.animals.uniform', return_value=0)
    mocker.patch('biosim.world.choice', return_value=direction)
    island = World(geogr_str)
    add_pop = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 6, 'weight': 6.5}]}]
    island.add_population(add_pop)
    island.do_migration()

    assert not all([island.object_map[1, 2].population,
                    island.object_map[0, 1].population,
                    island.object_map[1, 0].population,
                    island.object_map[2, 1].population,
                    not island.object_map[1, 1].population])


def test_one_migration(mocker):
    """Test that an animal bound to migrate will only migrate once."""
    mocker.patch('biosim.animals.uniform', return_value=0)
    mocker.patch('biosim.world.choice', return_value='E')

    geogr = """\
                WWWWW
                WLHDW
                WWWWW"""
    geogr = textwrap.dedent(geogr)

    island = World(geogr)
    add_pop = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 6, 'weight': 6.5}]}]
    island.add_population(add_pop)
    island.do_migration()

    assert all([not island.object_map[1, 1].population,
                island.object_map[1, 2].population,
                not island.object_map[1, 3].population])


def test_no_migration(mocker, geogr_str):
    """Test for no migration if probability_to_migrate is absent."""
    mocker.patch('biosim.animals.uniform', return_value=1)
    mocker.patch('biosim.world.choice', return_value='E')

    island = World(geogr_str)
    add_pop = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 6, 'weight': 6.5}]}]
    island.add_population(add_pop)
    island.do_migration()

    assert all([island.object_map[1, 1].population,
                not island.object_map[1, 2].population])

