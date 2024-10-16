import os
import shutil
import pytest

from biosim.simulation import BioSim
from biosim.island import Island
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
def map_str():
    return "WWW\nWLW\nWWW"


@pytest.fixture()
def img_dir_base():
    img_dir = 'C:\\temp\BioSimTest'
    yield img_dir
    shutil.rmtree(img_dir)


def test_map_validation(map_str):
    """Test creation of Island object if map input is valid."""
    sim = BioSim(map_str)
    assert type(sim.island) == Island


@pytest.mark.parametrize('map', ["WWW\nWLW\nWW", 1234])
def test_invalid_map(map):
    """Test that ValueError rises when invalid map format is given."""
    with pytest.raises(ValueError):
        BioSim(map)


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


def test_hist_spec_valid(map_str):
    """Test expected return if provided hist_specs are valid."""
    hist_specs = {'fitness': {'max': 1.0, 'delta': 0.05},
                  'age': {'max': 60.0, 'delta': 2},
                  'weight': {'max': 60, 'delta': 2}}
    sim = BioSim(map_str, hist_specs=hist_specs)
    boolean = sim._validate_hist_specs(hist_specs)
    assert boolean


def test_set_img_years_default_zero(map_str):
    """Test that img_years is set to default value 0 when not required,
    and no image directory is provided."""
    sim = BioSim(map_str)
    assert sim._img_years == 0


def test_set_img_years_default_vis(map_str, img_dir_base):
    """Test that img_years is set to default value vis_years, when required,
    and image directory is provided"""
    sim = BioSim(map_str,
                 img_dir=img_dir_base,
                 img_base='Biosim')
    assert sim._img_years == sim._vis_years


def test_set_img_years(map_str, img_dir_base):
    """Test that private setter method provides correct img_years value when defined correctly."""
    sim = BioSim(map_str,
                 img_years=5,
                 img_dir=img_dir_base,
                 img_base='Biosim')
    assert sim._img_years == 5


def test_set_img_years_error(map_str):
    """Test that private setter method provides errormessage when invalid input is given."""
    with pytest.raises(ValueError):
        BioSim(map_str, img_years=-5)


def test_set_vis_years(map_str):
    """Test that private setter method provides correct vis_years value."""
    sim = BioSim(map_str, vis_years=5)
    assert sim._vis_years == 5


@pytest.mark.parametrize('invalid_vis', [-5, 5.7, 'string'])
def test_set_vis_years_invalid(map_str, invalid_vis):
    """Test that ValueError rises if invalid values for vis_years are provided as input."""
    with pytest.raises(ValueError):
        BioSim(map_str, vis_years=invalid_vis)


@pytest.mark.parametrize('cmax', [None, {'Herbivore': 40, 'Carnivore': 10}])
def test_cmax_animals_validation_true(map_str, cmax):
    """Test that validation of cmax goes trough when provided with valid options."""
    sim = BioSim(map_str)
    assert sim._validate_cmax_animals(cmax)


def test_cmax_animals_validation_error(map_str):
    """Test that KeyError rises if invalid cmax_animals dictionary is provided."""
    with pytest.raises(KeyError):
        BioSim(map_str,
               cmax_animals={'Herbivore': 40, 'Dog': 10})


@pytest.mark.parametrize('img_dir, img_base', [(None, 'BioSimInconsistent'),
                                               ('C:/temp/BioSimInconsistent', None)])
def test_validate_im_params_inconsistent(map_str, img_dir, img_base):
    """Test that ValueError rises if inconsistent image parameters are provided as input"""
    with pytest.raises(ValueError):
        BioSim(map_str,
               img_dir=img_dir,
               img_base=img_base)


def test_validate_im_params_default_img_fmt(map_str):
    """Test that img_fmt is set to default value when not provided by user."""
    sim = BioSim(map_str)
    assert sim._img_fmt == 'png'


def test_validate_im_params_unsupported_format(map_str):
    """Test that ValueError rises of unsupported image format is provided."""
    img_fmt = 'txt'
    with pytest.raises(ValueError):
        BioSim(map_str, img_fmt=img_fmt)


def test_validate_im_params_specified_values(map_str, img_dir_base):
    """Test that correct values are saved in the image parameters when specified."""
    img_base = 'BioSim'
    img_fmt = 'jpg'
    sim = BioSim(map_str,
                 img_dir=img_dir_base,
                 img_base=img_base,
                 img_fmt=img_fmt)
    assert all([sim._img_dir == img_dir_base,
                sim._img_base == img_base,
                sim._img_fmt == img_fmt])


def test_validate_im_params_oserror(mocker, map_str):
    """Test that OSError rises as expected."""
    mocker.patch('os.makedirs', side_effect=OSError())
    img_dir = 'not_a_path'
    img_base = 'not_a_name'
    with pytest.raises(OSError):
        BioSim(map_str,
               img_dir=img_dir,
               img_base=img_base)


def test_validate_im_params_valid(map_str):
    """Test expected return if (un)provided image parameters are valid."""
    sim = BioSim(map_str)
    assert sim._validate_im_params


def test_figure_saved_name(map_str, img_dir_base):
    """Test that figures are saved during simulation"""
    file_name = 'BioSim'
    sim = BioSim(map_str,
                 ini_pop=[],
                 seed=1,
                 img_dir=img_dir_base,
                 img_base=file_name,
                 img_fmt='png')

    sim.simulate(2)
    assert all([os.path.isfile('C:\\temp\BioSimTest\Biosim_00000.png'),
                os.path.isfile('C:\\temp\BioSimTest\Biosim_00001.png')])


def test_year_initial(map_str):
    """Test that parameter year is set to 0 before any simulation."""
    sim = BioSim(map_str)
    assert sim.year == 0


def test_year_sim_once(map_str):
    """Test that attribute year is correctly updated after one simulation.
    (vis_years=0 enables graphics for more efficient testing)."""
    sim = BioSim(map_str, vis_years=0)
    num_years = 10
    sim.simulate(num_years)
    assert sim.year == num_years


def test_year_sim_twice(map_str):
    """Test that attribute year is correctly updated after two simulations."""
    sim = BioSim(map_str, vis_years=0)
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
def test_num_animals_initially(map_str, ini_pop):
    """Test that expected amount of animals are to be found on the island initially."""
    sim = BioSim(map_str, ini_pop)
    num_animals = len(ini_pop[0]['pop'])
    assert sim.num_animals == num_animals


def test_num_animals_added(map_str):
    """Test that expected amount of animals are to be found on the island
    after adding animals explicitly."""
    ini_pop = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 5},
                                       {'species': 'Carnivore', 'age': 5, 'weight': 5}]}]
    sim = BioSim(map_str)
    sim.add_population(ini_pop)
    assert sim.num_animals == 2


def test_num_animals_per_species_added(map_str):
    """Test that expected amount of animals of each species are to be found on the island."""
    ini_pop = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 5},
                                       {'species': 'Carnivore', 'age': 5, 'weight': 5}]}]
    sim = BioSim(map_str)
    sim.add_population(ini_pop)
    herbs = sim.num_animals_per_species['Herbivore']
    carns = sim.num_animals_per_species['Carnivore']
    assert all([herbs == 1, carns == 1])


def test_num_animals_after_sim(map_str, mocker):
    """Deterministic test: Test expected number of animals after simulation of one year,
    providing birth happens, and no death."""
    mocker.patch('biosim.animals.min', return_value=1)
    Herbivore.set_params({'xi': 0, 'zeta': 0, 'omega': 0})
    ini_pop = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 7, 'weight': 16},
                                       {'species': 'Herbivore', 'age': 7, 'weight': 16}]}]

    for _ in range(20):
        sim = BioSim(map_str,
                     ini_pop,
                     vis_years=0)
        sim.simulate(1)
        assert all([sim.num_animals == 4,
                    sim.num_animals_per_species['Herbivore'] == 4,
                    sim.num_animals_per_species['Carnivore'] == 0])


@pytest.mark.parametrize('species, species_str',
                         [(Herbivore, 'Herbivore'),
                          (Carnivore, 'Carnivore')])
def test_set_animal_parameters(map_str, species, species_str):
    """Test that set_animal_parameters for all subspecies provide expected results."""
    sim = BioSim(map_str)
    sim.set_animal_parameters(species_str, {'omega': 0.6, 'beta': 1})
    assert all([species.params['omega'] == 0.6, species.params['beta'] == 1])


def test_set_animal_parameters_invalid(map_str):
    """Test that ValueError rises if wrongful species are provided."""
    sim = BioSim(map_str)
    with pytest.raises(ValueError):
        sim.set_animal_parameters('Penguin', {'omega': 0.6})


@pytest.mark.parametrize('landscape, landscape_type', [('Lowland', 'L'), ('Highland', 'H')])
def test_set_landscape_parameters_valid(map_str, landscape, landscape_type):
    """Test that set_landscape_parameters provide expected results for valid landscape types."""
    sim = BioSim(map_str)
    sim.set_landscape_parameters(landscape_type, {'f_max': 400})
    assert Landscape.params['f_max'][landscape] == 400


@pytest.mark.parametrize('landscape', ['D', 'W'])
def test_set_landscape_parameters_invalid(map_str, landscape):
    """Test that ValueError rises if invalid landscape type for parameters are given."""
    sim = BioSim(map_str)
    with pytest.raises(ValueError):
        sim.set_landscape_parameters(landscape, {'f_max': 400})


@pytest.mark.parametrize('ini_pop', [
    {'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'weight': 7}]},
    123,
    'abc'])
def test_add_population_invalid_type(map_str, ini_pop):
    """Test that ValueError rises if population added is not in a list."""
    with pytest.raises(TypeError):
        BioSim(map_str, ini_pop)


def test_add_population_none(map_str):
    """Test that None is returned when empty list is provided as initial population."""
    ini_pop = []
    sim = BioSim(map_str)
    assert sim.add_population(ini_pop) is None


def test_make_movie(map_str, img_dir_base):
    """Test that movie is saved correctly."""
    img_base = 'BioSim'
    ini_pop = [{'loc': (2, 2),
                'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]}
               for _ in range(20)]
    sim = BioSim(map_str,
                 ini_pop,
                 img_dir=img_dir_base,
                 img_base=img_base,
                 vis_years=10,
                 img_years=1)
    sim.simulate(10)
    sim.make_movie()
    assert os.path.isfile('C:\\temp\BioSimTest\BioSim_video.mp4')


def test_make_movie_error(map_str, img_dir_base):
    """Test that error rises if directory is empty."""
    img_base = 'BioSim'
    ini_pop = [{'loc': (2, 2),
                'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]}
               for _ in range(20)]
    sim = BioSim(map_str, ini_pop, img_dir=img_dir_base, img_base=img_base)
    with pytest.raises(FileNotFoundError):
        sim.make_movie()


def test_simulation_modulus_error_first_sim(map_str):
    """Test that ValueError rises if the modulus between vis_years and number
    of years simulating is different from zero."""
    sim = BioSim(map_str, vis_years=8)
    with pytest.raises(ValueError):
        sim.simulate(10)


def test_simulation_modulus_error_second_sim(map_str):
    """Test that ValueError rises if modulus is incorrect during second simulation."""
    sim = BioSim(map_str, vis_years=8)
    sim.simulate(8)
    with pytest.raises(ValueError):
        sim.simulate(10)
