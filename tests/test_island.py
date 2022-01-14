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
                    WLDW
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
    assert World(geogr_str)

@pytest.mark.skip


@pytest.mark.skip
def test_create_base_map():
    island = World(geogr)
    #World.base_map ==

