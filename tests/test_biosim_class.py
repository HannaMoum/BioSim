import pytest
from biosim.biosim_klasse import BioSim
from biosim.world import World


@pytest.fixture()
def hist_specs():
    hist_specs = {'fitness': {'max': 1.0, 'delta': 0.05},
                  'age': {'max': 60.0, 'delta': 2},
                  'weight': {'max': 60, 'delta': 2}}
    return hist_specs


def test_map_validation(hist_specs):
    """Test creation of World object if map input is valid."""
    map_str = "WWW\nWLW\nWWW"
    sim = BioSim(map_str, hist_specs=hist_specs)
    assert type(sim.island) == World


@pytest.mark.parametrize('map', ["WWW\nWLW\nWW", 1234])
def test_invalid_map(hist_specs, map):
    """Test that ValueErrors are risen when invalid map format is given."""
    with pytest.raises(ValueError):
        sim = BioSim(map, hist_specs=hist_specs)