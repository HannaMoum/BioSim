import textwrap
import pytest
from biosim.world import World

SEED = 12345678  # random seed for tests

# @pytest.fixture()
# def geogr_str():
#     """Create initial island string to be used in other tests."""
#     geogr = """\
#                     WWWW
#                     WLHW
#                     WLDW
#                     WWWW
#                 """
#     geogr = textwrap.dedent(geogr)
#     geogr = geogr.split()
#     return geogr

#Initial tests, made to run when changes in world has been made

#@pytest.mark.skip
@pytest.mark.parametrize('geogr_str', ["""\
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
def test_validate_map_str(geogr_str):
    """Test ValueError is risen if outer edge"""
    geogr = textwrap.dedent(geogr_str)
    with pytest.raises(ValueError)
        World(geogr_str)

@pytest.mark.skip
def test_create_base_map():
    island = World(geogr)
    #World.base_map ==

