import pytest
from biosim.biosim_klasse import BioSim, BioSimParam
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


def test_map_validation(map_str, hist_specs):
    """Test creation of World object if map input is valid."""
    sim = BioSim(map_str, hist_specs=hist_specs)
    assert type(sim.island) == World


@pytest.mark.parametrize('map', ["WWW\nWLW\nWW", 1234])
def test_invalid_map(hist_specs, map):
    """Test that ValueError rises when invalid map format is given."""
    with pytest.raises(ValueError):
        BioSim(map, hist_specs=hist_specs)


@pytest.mark.parametrize('hist_spec_invalid', [{'fitness': {'max': 1.0, 'delta': 0.05},
                                                'wrong_age': {'max': 60.0, 'delta': 2},
                                                'weight': {'max': 60, 'delta': 2}},
                                               {'fitness': {'max': 1.0, 'delta': 0.05},
                                                'age': {'max': 60.0, 'delta': 2},
                                                'weight': {'max': 60, 'omega': 2}}])
def test_hist_spec_invalid(map_str, hist_spec_invalid):
    """Test that KeyError rises if provided hist_spec is invalid."""
    with pytest.raises(KeyError):
        BioSim(map_str, hist_specs=hist_spec_invalid)


def test_hist_spec_valid(map_str, hist_specs):
    """Test expected return if provided hist_specs are valid."""
    sim = BioSim(map_str, hist_specs=hist_specs)
    boolean = sim._validate_hist_specs(hist_specs)
    assert boolean


def test_set_img_years_default(map_str, hist_specs):
    """Test that img_years is set to default value when not else is requested."""
    sim = BioSim(map_str, hist_specs=hist_specs)
    assert sim._img_years == sim._vis_years


def test_set_img_years(map_str, hist_specs):
    """Test that private setter method provides correct img_years value when defined."""
    sim = BioSim(map_str, hist_specs=hist_specs, img_years=5)
    assert sim._img_years == 5


def test_set_vis_years(map_str, hist_specs):
    """Test that private setter method provides correct vis_years value."""
    sim = BioSim(map_str, hist_specs=hist_specs, vis_years=5)
    assert sim._vis_years == 5


@pytest.mark.parametrize('cmax', [None, {'Herbivore': 40, 'Carnivore': 10}])
def test_cmax_animals_validation_true(map_str, hist_specs, cmax):
    """Test that validation of cmax goes trough when provided with valid options."""
    sim = BioSim(map_str, hist_specs=hist_specs)
    assert sim._validate_cmax_animals(cmax)


def test_cmax_animals_validation_error(map_str, hist_specs):
    """Test that KeyError rises if invalid cmax_animals dictionary is provided."""
    with pytest.raises(KeyError):
        BioSim(map_str,
               hist_specs=hist_specs,
               cmax_animals={'Herbivore': 40, 'Dog': 10})


@pytest.mark.parametrize('img_dir, img_base', [(None, 'BioSimInconsistent'),
                                               ('C:/temp/BioSimInconsistent', None)])
def test_validate_im_params_inconsistent(map_str, hist_specs, img_dir, img_base):
    """Test that ValueError rises if inconsistent image parameters are provided as input"""
    with pytest.raises(ValueError):
        BioSim(map_str,
               hist_specs=hist_specs,
               img_dir=img_dir,
               img_base=img_base)


def test_validate_im_params_unsupported_format(map_str, hist_specs):
    """Test that ValueError rises of unsupported image format is provided."""
    img_fmt = 'txt'
    with pytest.raises(ValueError):
        BioSim(map_str,
               hist_specs=hist_specs,
               img_fmt=img_fmt)


def test_validate_im_params_default_values(map_str, hist_specs):
    """Test that default values are provided if image parameters are unspecified from user."""
    sim = BioSim(map_str, hist_specs=hist_specs)
    assert all([sim._img_dir == sim.default_img_dir,
                sim._img_base == sim.default_img_base,
                sim._img_fmt == sim.default_img_fmt])


def test_validate_im_params_specified_values(map_str, hist_specs):
    """Test that correct values are saved in the image parameters when specified."""
    img_dir = 'C:/temp/BioSimTester'
    img_base = 'BioSimTester'
    img_fmt = 'jpg'
    sim = BioSim(map_str,
                 hist_specs=hist_specs,
                 img_dir=img_dir,
                 img_base=img_base,
                 img_fmt=img_fmt)
    assert all([sim._img_dir == img_dir,
                sim._img_base == img_base,
                sim._img_fmt == img_fmt])

