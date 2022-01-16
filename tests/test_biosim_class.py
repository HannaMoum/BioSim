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


@pytest.mark.parametrize('hist_spec_invalid', [{'fitness': {'max': 1.0, 'delta': 0.05},
                                                'wrong_age': {'max': 60.0, 'delta': 2},
                                                'weight': {'max': 60, 'delta': 2}},
                                               {'fitness': {'max': 1.0, 'delta': 0.05},
                                                'age': {'max': 60.0, 'delta': 2},
                                                'weight': {'max': 60, 'omega': 2}}])
def test_hist_spec_invalid(map_str, hist_spec_invalid):
    """Test that KeyError is risen if provided hist_spec is invalid."""
    with pytest.raises(KeyError):
        BioSim(map_str, hist_specs=hist_spec_invalid)


def test_hist_spec_valid(map_str, hist_specs):
    """Test expected return if provided hist_specs are valid."""
    sim = BioSim(map_str, hist_specs=hist_specs)
    boolean = sim._validate_hist_specs(hist_specs)
    assert boolean


def test_set_img_years_default(hist_specs, map_str):
    """Test that img_years is set to default value when not else is requested."""
    sim = BioSim(map_str, hist_specs=hist_specs)
    assert sim._img_years == sim._vis_years


def test_set_img_years(hist_specs, map_str):
    """Test that private setter method provides correct img_years value when defined."""
    sim = BioSim(map_str, hist_specs=hist_specs, img_years=5)
    assert sim._img_years == 5


def test_set_vis_years(hist_specs, map_str):
    """Test that private setter method provides correct vis_years value."""
    sim = BioSim(map_str, hist_specs=hist_specs, vis_years=5)
    assert sim._vis_years == 5



