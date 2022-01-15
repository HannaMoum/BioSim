import textwrap
import pytest
from biosim.world import World
import numpy as np

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
    """Test correct creation of base_map."""
    base_map_wanted = [['W', 'W', 'W', 'W'],
                       ['W', 'L', 'H', 'W'],
                       ['W', 'W', 'W', 'W']]
    base_map = World(geogr_str).base_map
    for row_wanted, row in zip(base_map_wanted, base_map):
        for letter_wanted, letter in zip(row_wanted, row):
            assert letter_wanted == letter


@pytest.mark.skip
def test_migrate_map(geogr_str):
    """Test correct creation and attribute save of migrate_map."""
    migrate_map = [[False, False, False, False],
                   [False, True, True, False],
                   [False, False, False, False]]
    # assert all([World(geogr_str)._make_migrate_map() == migrate_map,
    #             World(geogr_str).migrate_map == migrate_map])
    assert np.testing.assert_allclose(World(geogr_str)._make_migrate_map(), migrate_map)


@pytest.mark.skip
def test_object_map_save(geogr_str):
    """Test correct attribute save from making an object map."""
    object_map_creation = World(geogr_str)._make_object_map()
    object_map_attribute = World(geogr_str).object_map
    assert object_map_creation == object_map_attribute  # Not sure this will work...


@pytest.mark.skip
def test_object_map_shape(geogr_str):
    """Test creation of correct size for object_map."""
    island = World(geogr_str)
    assert island.object_map.shape == (3, 4)


@pytest.mark.skip
def test_object_map_type(geogr_str):
    """Test correct creation of object references by checking their type."""
    island = World(geogr_str)
    for reference_row in island.object_map:
        for reference in reference_row:
            assert type(reference) == object  # Or something like this...


@pytest.mark.skip
def test_object_map_reference(geogr_str):
    """Test correct creation of object references by checking their attribute landscape_type."""
    island = World(geogr_str)
    geogr = geogr_str.split()
    for string, reference_row in zip(geogr, island.object_map):
        for letter, reference in zip(string, reference_row):
            assert reference.landscape_type == letter


@pytest.mark.skip
def test_object_map_coordinate(geogr_str):
    """Test that given coordinates picks out the correct object."""
    island = World(geogr_str)
    assert all([island.object_map[1, 1].landscape_type == 'L',
                island.object_map[1, 2].landscape_type == 'H'])


@pytest.mark.skip
@pytest.mark.parametrize('location', [(1, -1), (-1, 1), (0, 1), (9, 2), (2, 9)])
def test_add_animals_IndexError(geogr_str, location):
    """Test that IndexError arise if negative coordinates or non-existent coordinates are provided."""
    island = World(geogr_str)
    add_pop = [{'loc': location, 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 5}]}]
    with pytest.raises(IndexError):
        island.add_population(add_pop)


@pytest.mark.parametrize('location', [(2, 2), (2, 3)])
@pytest.mark.skip
def test_add_animals_success(geogr_str, location):
    """Test that animals are added in the correct locations."""
    island = World(geogr_str)
    add_pop = [{'loc': location, 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 5},
                                         {'species': 'Carnivore', 'age': 6, 'weight': 6.5}]}]
    island.add_population(add_pop)
    assert all([len(island.object_map[location].population) == 2,
                len(island.object_map[location].herbivores) == 1,
                len(island.object_map[location].carnivores) == 1])
