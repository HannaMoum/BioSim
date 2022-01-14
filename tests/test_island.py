import textwrap
import pytest
from biosim.world import World

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

#Initial tests, made to run when changes in world has been made

@pytest.mark.skip
@pytest.mark.parametrize('geogr', ["""\
                                        WWW
                                        WLH 
                                        WWW
                                    """,
                                   """\
                                        WWW
                                        WKW
                                        WWW
                                    """,
                                   """\
                                        WDW
                                        WWW
                                        WWW
                                    """,
                                   """\
                                        WWW
                                        WH
                                        WWW
                                    """])
def test_invalid_map_str(geogr):
    """Test ValueError if any map requirements are not met."""
    geogr_wrapped = textwrap.dedent(geogr)
    with pytest.raises(ValueError):
        World(geogr_wrapped)


@pytest.mark.skip
def test_valid_map_str(geogr_str):
    """Test no ValuErrors are risen when valid map string are given."""
    assert all ([World(geogr_str),
                 World(geogr_str)._make_base_map(geogr_str)])


@pytest.mark.skip
def test_base_map(geogr_str):
    """Test correct creation and attribute save of base_map."""
    base_map = [['W', 'W', 'W', 'W'],
                ['W', 'L', 'H', 'W'],
                ['W', 'W', 'W', 'W']]
    assert all([World(geogr_str)._make_base_map(geogr_str) == base_map,
                World(geogr_str).base_map == base_map,])


@pytest.mark.skip
def test_migrate_map(geogr_str):
    """Test correct creation and attribute save of migrate_map."""
    migrate_map = [[False, False, False, False],
                   [False, True, True, False],
                   [False, False, False, False]]
    assert all([World(geogr_str)._make_migrate_map() == migrate_map,
                World(geogr_str).migrate_map == migrate_map])


@pytest.mark.skip
def test_object_map_save(geogr_str):
    """Test correct attribute save from making an object map."""
    object_map_creation = World(geogr_str)._make_object_map()
    object_map_attribute = World(geogr_str).object_map
    assert object_map_creation == object_map_attribute #Not sure this will work...


@pytest.mark.skip
def test_object_map_type(geogr_str):
    island = World(geogr_str)
    #Må iterere riktig, ikke slik;
    for letter, reference in (geogr_str, island.object_map):
        assert reference.landscape_type == letter


