import pytest
from biosim.biosim_klasse import BioSim
from biosim.world import World


@pytest.fixture()
def hist_specs():
    hist_specs = {'fitness': {'max': 1.0, 'delta': 0.05},
                  'age': {'max': 60.0, 'delta': 2},
                  'weight': {'max': 60, 'delta': 2}}
    return hist_specs

@pytest.fixture()
def map_str():
    return "WWW\nWLW\nWWW"


def test_map_validation(hist_specs, map_str):
    """Test creation of World object if map input is valid."""
    sim = BioSim(map_str, hist_specs=hist_specs)
    assert type(sim.island) == World


@pytest.mark.parametrize('map', ["WWW\nWLW\nWW", 1234])
def test_invalid_map(hist_specs, map):
    """Test that ValueErrors are risen when invalid map format is given."""
    with pytest.raises(ValueError):
        BioSim(map, hist_specs=hist_specs)





def test_set_vis_years(hist_specs, map_str):
    """Test that private setter function provides correct vis_years value."""
    sim = BioSim(map_str, hist_specs=hist_specs, vis_years=5)
    assert sim._vis_years == 5

