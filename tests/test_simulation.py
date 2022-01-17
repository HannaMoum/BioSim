import pytest
from biosim.simulation import BioSim
from biosim.world import World
from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Landscape


@pytest.fixture(autouse=True)
def reset_params_default():
    """Reset parameters to default after test has run."""
    yield
    Herbivore.set_params(Herbivore._default_params)
    Carnivore.set_params(Carnivore._default_params)
    Landscape.set_params(Landscape._default_params)


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

# todo: FIX
def test_set_img_years_default(map_str, hist_specs):
    """Test that img_years is set to default value when not else is requested."""
    sim = BioSim(map_str, hist_specs=hist_specs)
    assert sim._img_years == sim._vis_years

# TODO: FIX
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


# todo: FIX
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


def test_validate_im_params_oserror(mocker, map_str, hist_specs):
    """Test that OSError rises as expected."""
    mocker.patch('os.makedirs', side_effect=OSError())
    img_dir = 'not_a_path'
    img_base = 'not_a_name'
    with pytest.raises(OSError):
        BioSim(map_str,
               hist_specs=hist_specs,
               img_dir=img_dir,
               img_base=img_base)


def test_validate_im_params_valid(map_str, hist_specs):
    """Test expected return if (un)provided image parameters are valid."""
    sim = BioSim(map_str, hist_specs=hist_specs)
    assert sim._validate_im_params


def test_year_initial(map_str, hist_specs):
    """Test that parameter year is set to 0 before any simualtion."""
    sim = BioSim(map_str, hist_specs=hist_specs)
    assert sim.year == 0


def test_year_sim_once(map_str, hist_specs):
    """Test that attribute year is correctly updated after one simulation.
    (vis_years=0 enables graphics for more efficient testing.)."""
    sim = BioSim(map_str,
                 hist_specs=hist_specs,
                 vis_years=0)
    num_years = 10
    sim.simulate(num_years)
    assert sim.year == num_years


def test_year_sim_twice(map_str, hist_specs):
    """Test that attribute year is correctly updated after two simulations."""
    sim = BioSim(map_str,
                 hist_specs=hist_specs,
                 vis_years=0)
    first_sim = 5
    second_sim = 3
    sim.simulate(first_sim)
    sim.simulate(second_sim)
    assert sim.year == first_sim + second_sim


@pytest.mark.parametrize('ini_pop', [
    [{'loc': (2, 2), 'pop': []}],
    [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 5},
                             {'species': 'Carnivore', 'age': 5, 'weight': 5}]
      }]
])
def test_num_animals_initially(map_str, hist_specs, ini_pop):
    """Test that expected amount of animals are to be found on the island initially."""
    sim = BioSim(map_str,
                 ini_pop,
                 hist_specs=hist_specs)
    num_animals = len(ini_pop[0]['pop'])
    assert sim.num_animals == num_animals


def test_num_animals_added(map_str, hist_specs):
    """Test that expected amount of animals are to be found on the island after adding animals explicitly."""
    ini_pop = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 5},
                                       {'species': 'Carnivore', 'age': 5, 'weight': 5}]}]
    sim = BioSim(map_str, hist_specs=hist_specs)
    sim.add_population(ini_pop)
    assert sim.num_animals == 2


def test_num_animals_per_species_added(map_str, hist_specs):
    """Test that expected amount of animals of each species are to be found on the island."""
    ini_pop = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 5},
                                       {'species': 'Carnivore', 'age': 5, 'weight': 5}]}]
    sim = BioSim(map_str, hist_specs=hist_specs)
    sim.add_population(ini_pop)
    herbs = sim.num_animals_per_species['Herbivore']
    carns = sim.num_animals_per_species['Carnivore']
    assert all([herbs == 1, carns == 1])


def test_num_animals_after_sim(map_str, hist_specs, mocker):
    """Deterministic test: Test expected number of animals after simulation of one year,
    providing birth happens, and no death."""
    mocker.patch('biosim.animals.min', return_value=1)
    Herbivore.set_params({'xi': 0, 'zeta': 0, 'omega': 0})
    ini_pop = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 7, 'weight': 16},
                                       {'species': 'Herbivore', 'age': 7, 'weight': 16}]}]

    for _ in range(20):
        sim = BioSim(map_str,
                     ini_pop,
                     hist_specs=hist_specs,
                     vis_years=0)
        sim.simulate(1)
        assert all([sim.num_animals == 4,
                    sim.num_animals_per_species['Herbivore'] == 4,
                    sim.num_animals_per_species['Carnivore'] == 0])


@pytest.mark.parametrize('species, species_str', [(Herbivore, 'Herbivore'), (Carnivore, 'Carnivore')])
def test_set_animal_parameters(map_str, hist_specs, species, species_str):
    """Test that set_animal_parameters for all subspecies provide expected results."""
    sim = BioSim(map_str, hist_specs=hist_specs)
    sim.set_animal_parameters(species_str, {'omega': 0.6, 'beta': 1})
    assert all([species.params['omega'] == 0.6, species.params['beta'] == 1])


def test_set_animal_parameters_invalid(map_str, hist_specs):
    """Test that ValueError rises if wrongful species are provided."""
    sim = BioSim(map_str, hist_specs=hist_specs)
    with pytest.raises(ValueError):
        sim.set_animal_parameters('Penguin', {'omega': 0.6})


@pytest.mark.parametrize('landscape, landscape_type', [('Lowland', 'L'), ('Highland', 'H')])
def test_set_landscape_parameters_valid(map_str, hist_specs, landscape, landscape_type):
    """Test that set_landscape_parameters provide expected results for valid landscape types."""
    sim = BioSim(map_str, hist_specs=hist_specs)
    sim.set_landscape_parameters(landscape_type, {'f_max': 400})
    assert Landscape.params['f_max'][landscape] == 400


@pytest.mark.parametrize('landscape', ['D', 'W'])
def test_set_landscape_parameters_invalid(map_str, hist_specs, landscape):
    """Test that ValuError rises if invalid landscape type for parametersare given."""
    sim = BioSim(map_str, hist_specs=hist_specs)
    with pytest.raises(ValueError):
        sim.set_landscape_parameters(landscape, {'f_max': 400})


@pytest.mark.parametrize('ini_pop', [
    {'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'weight': 7}]},
    123,
    'abc'])
def test_add_population_invalid_type(map_str, hist_specs, ini_pop):
    """Test that ValueError rises if population added is not in a list."""
    with pytest.raises(TypeError):
        BioSim(map_str, ini_pop, hist_specs=hist_specs)


def test_add_population_none(map_str, hist_specs):
    """Test that None is returned when empty list is provided as initial population."""
    ini_pop = []
    sim = BioSim(map_str, hist_specs=hist_specs)
    assert sim.add_population(ini_pop) is None


def test_make_movie(map_str, hist_specs):
    """Test that no errror rises when trying to make a movie with correctly provided information."""
    img_dir = 'C:\\temp\BioSim'
    img_base = 'BioSim'
    ini_pop = [{'loc': (2,2), 'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]} for _ in range(20)]
    sim = BioSim(map_str, ini_pop, hist_specs=hist_specs, img_dir=img_dir, img_base=img_base)
    sim.simulate(15)
    assert sim.make_movie()


