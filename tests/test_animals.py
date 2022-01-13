"""Tests for animal class, concerning both herbivores and carnivores."""
import pytest
from random import uniform, randint, gauss
from statsmodels.stats.weightstats import ztest
from biosim.animals import Herbivore, Carnivore
from biosim.lowland import Landscape

#  Overall parameters for probabilistic tests
SEED = 12345678  # random seed for tests

@pytest.fixture(autouse=True) #Combine with parameterization?
def reset_params_default():
    """Reset parameters to default after test has run."""
    yield
    Herbivore.set_params(Herbivore.default_params)
    Carnivore.set_params(Carnivore.default_params)


# @pytest.fixture(autouse=True)
# def create_animals(self):
#     """Create herb and carn."""
#     herb = Herbivore(10, 12.5)
#     carn = Carnivore(9, 10.5)


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_set_params(species):
    """Test optional change of default parameters."""
    species.set_params({'beta': 1.2, 'omega': 0.2})
    assert all([species.params['beta'] == 1.2, species.params['omega'] == 0.2])


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_parameter_control(species):
    """Test that only legal parameters and values are allowed."""
    with pytest.raises(ValueError):
        all([species.set_params({'beta': -0.2}), species.set_params({'eta': 1.2}), species.set_params({'alpha': 0.5})])


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
@pytest.mark.parametrize('age', [0, 10, 10.0])
def test_animal_create_age(species, age):
    """Test input age of animal."""
    assert species(12.5, age).age == age


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_animal_default_age(species):
    """Test default age value for newborns."""
    assert species(weight=12.5).age == 0


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
@pytest.mark.parametrize('wrong_age', [-1, 5.6, 'age'])
def test_animal_create_age_wrong(species, wrong_age):
    """Test control of age input if made wrong."""
    with pytest.raises(ValueError):
        species(12.5, wrong_age)


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_animal_create_weight(species):
    """Test initial weight of animal."""
    animal = species(weight=12.5, age=10)
    assert animal.weight == 12.5


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_animal_create_weight_wrong(species):
    """Test control of weight input if made wrong."""
    with pytest.raises(ValueError):
        all([species(weight=-12.5, age=10), species(weight='weight', age=10)])


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_animal_create_F_tilde(species): #TODO: Change name when F-tilde changes name
    """Validate initial value of F-tilde and its' possibility to change."""
    animal = species(12.5, 10)
    eat_amount = 5
    assert all([animal.F_tilde == 0, animal.F_tilde + eat_amount == eat_amount])


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_privacy_F_tilde(species):
    animal = species(12.5, 10)
    eat_amount = 5
    animal.F_tilde = eat_amount #TODO: We can change F_tilde anywhere... Should all getters and setters be _F_tilde?
    pass


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_animal_create_has_migrated(species):
    """Test that has_migrated attribute is set to False when animal is created."""
    assert not species(12.5, 10).has_migrated


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_zero_fitness(species):
    """Test fitness for animal with no weight."""
    assert species(0, 10).fitness == 0


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_fitness_attribute_change(species):
    """Test fitness-formula.

    If age and weight is equal to parameter values a_half and w_half respectively,
     expected fitness is 1/4 exactly."""
    age = species.params['a_half']
    weight = species.params['w_half']

    assert species(weight, age).fitness == 1/4


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_fitness_parameter_change(species):
    """Test fitness-formula.

    If phi_age and phi_weight is set to 0, expected fitness is 1/4 exactly
    (independently of age and weight)."""
    species.set_params({'phi_age': 0, 'phi_weight': 0})
    assert species(12.5, 10).fitness == 1/4


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_eat_unlimited(species):
    """Test correct weight gain when the amount of food available exceeds that of the animal's hunger."""
    animal_1 = species(12.5, 10)
    animal_2 = species(12.5, 10)
    initial_weight = animal_1.weight

    satisfying_amount_1 = species.params['F']
    satisfying_amount_2 = species.params['F']*2

    animal_1.eat(satisfying_amount_1) and animal_2.eat(satisfying_amount_2)
    weight_gain = species.params['F'] * species.params['beta']

    assert all((animal_1.weight == initial_weight + weight_gain, animal_1.weight == animal_2.weight))


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_eat_limited(species):
    """Test correct weight gain when the amount of food available subceeds that of the animal's hunger."""
    animal = species(12.5, 10)
    initial_weight = animal.weight

    limited_food = species.params['F'] - species.params['F']*0.5  # Make sure we have a positive value
    animal.eat(limited_food)
    weight_gain = limited_food * species.params['beta']
    assert animal.weight == initial_weight + weight_gain


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_eat_F_tilde_grow(species): #TODO: Edit name when F_tilde changes
    """Test correct growth of attribute F_tilde when animals eat."""
    animal = species(12.5, 10)
    available_food = 100
    eaten = animal.eat(available_food)
    assert animal.F_tilde == eaten

#No testing for wanted_food = param F - F_tilde...


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_aging(species):
    """Deterministic test: Age must increase by one each year.""" #OBS! Dette er det samme som Plesser har...
    animal = species(12.5)
    num_years = 10
    for n in range(num_years):
        animal.age_and_weightloss()
        assert animal.age == n + 1


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_decrease_weight_when_aging(species):
    """Deterministic test: Weight must decrease by a factor of eta every year."""
    animal = species(12.5)
    num_years = 10
    for n in range(num_years):
        new_weight = animal.weight - animal.weight*species.params['eta']
        animal.age_and_weightloss()
        assert animal.weight == new_weight


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_migration_probability(mocker, species):
    """Test that all animals will migrate if the probability is always bigger than a random drawn number"""
    mocker.patch('biosim.animals.uniform', return_value=0)
    for _ in range(20):
        assert species(12.5, 10).probability_to_migrate()


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_probability_to_give_birth(species):
    """Test animal giving birth if all requirements are fulfilled

    xi = 0: assures maternal health
    zeta = 0: assures puberty
    num_animals = any positive number >= 8, gamma = 0.5 and fitness = 1/4: Assures match_probability
    sigma_birth = 0.2 (small enough to assure no miscarriages)
    """
    species.set_params({'xi': 0, 'zeta': 0, 'gamma': 0.5, 'sigma_birth': 0.2})
    age = species.params['a_half']
    weight = species.params['w_half']
    num_animals = 10

    for _ in range(100):
        assert species(weight, age).probability_to_give_birth(num_animals)

@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_birth_ztest(species):
    """Test that the mean of all birth weights drawn from probability_to_give_birth is within
    a gaussian distribution with a given mean and variance.
    Ztest returns a p_value which gives the probability to observe a value a distance or further
    away from the mean, if that value follows the assumed distribution.
    We compare the p_value to a predefined acceptance limit alpha, and pass the test if p > a.

    Test edits parameters to assure all babies are born."""
    species.set_params({'xi': 0, 'zeta': 0, 'gamma': 0.5, 'sigma_birth': 0.2})
    age = species.params['a_half']
    weight = species.params['w_half']
    num_animals = 10
    animal = species(weight, age)

    alpha = 0.001
    newborn_weights = [animal.probability_to_give_birth(num_animals) for _ in range(200)]
    test_stat, p_value = ztest(newborn_weights, value=species.params['w_birth'])

    assert p_value > alpha


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_birth_prob_matchmaking(mocker, species):
    """Deterministic test: No birth takes place if all requirements but matchmaking are fulfilled.

    xi = 0: assures maternal health
    zeta = 0: assures puberty
    num_animals = any positive number < 8, gamma = 0.5, fitness = 1 / 4 and mocker ('random.uniform) return 1:
     assures no match_probability
    sigma_birth = 0.2 (small enough to assure no miscarriages)
    """
    mocker.patch('biosim.animals.uniform', return_value=1)
    species.set_params({'xi': 0, 'zeta': 0, 'gamma': 0.5, 'sigma_birth': 0.2})
    age = species.params['a_half']
    weight = species.params['w_half']
    num_animals = 7

    for _ in range(100):
        assert not species(weight, age).probability_to_give_birth(num_animals)


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_birth_prob_fertilization(species):
    """Deterministic test: No birth can take place if only one animal is present."""
    animal = species(12.5, 10)
    num_animals = 1
    for _ in range(50):
        assert not animal.probability_to_give_birth(num_animals)


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_birth_prob_puberty(mocker, species):
    """Deterministic test: no birth takes place if all requirements but reached_puberty are fulfilled.

    xi = 0: assures maternal health
    zeta = weight/sigma_birth,  when 0 < sigma_birth < 1 and w_birth = anything (but negative)
    num_animals = any positive number < 8, gamma = 0.5, fitness = 1 / 4 and mocker ('random.uniform) return 1:
     assures no match_probability
    sigma_birth = 0.2 (small enough to assure no miscarriages)
    """
    mocker.patch('biosim.animals.uniform', return_value=0)
    age = species.params['a_half']
    weight = species.params['w_half']
    species.set_params({'xi': 0, 'gamma': 0.5, 'sigma_birth': 0.2})
    species.set_params({'zeta': weight/species.params['sigma_birth']})
    num_animals = 10

    for _ in range(100):
        assert not species(weight, age).probability_to_give_birth(num_animals)


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_birth_prob_maternal_health(species):
    """Deterministic test: no birth takes place if all requirements but maternal health are fulfilled.

    xi = 300: big number assuring maternal health fails
    zeta = 0: assures puberty
    num_animals = any positive number >= 8, gamma = 0.5 and fitness = 1/4: Assures match_probability
    sigma_birth = 0.2 (small enough to assure no miscarriages)
    """
    species.set_params({'xi': 300, 'zeta': 0, 'gamma': 0.5, 'sigma_birth': 0.2})
    age = species.params['a_half']
    weight = species.params['w_half']
    num_animals = 10

    for _ in range(100):
        assert not species(weight, age).probability_to_give_birth(num_animals)


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_birth_prob_miscarriage(species):
    """Statistical test: testing that miscarriage is directly connected to birth_weight
    trough the gaussian distribution.

    w_birth = 0 and sigma_birth as any positive value assures 50% of births are miscarriages.
    We pass the test if this statement holds by ± 10% due to:
        1. We can only calculate with whole numbers
        2. If by chance a baby is born at exact weight 0, it will count as a positive birth.
    """
    species.set_params({'sigma_birth': 0.2, 'w_birth': 0})

    newborns = [gauss(species.params['w_birth'], species.params['sigma_birth']) for _ in range(500)]
    negative_newborns = [newborn for newborn in newborns if newborn < 0]
    lower_limit = 1.90
    upper_limit = 2.10

    assert lower_limit < len(newborns)/len(negative_newborns) < upper_limit


@pytest.mark.parametrize('species_obj, species_str', [(Herbivore, 'Herbivore'), (Carnivore, 'Carnivore')])
def test_giving_birth_true(species_obj, species_str):
    """"Test correct return value if animal gives birth.

    Test use the same parameter values as in test probability_to_give_birth to assure birth takes place."""
    species_obj.set_params({'xi': 0, 'zeta': 0, 'gamma': 0.5, 'sigma_birth': 0.2})
    age = species_obj.params['a_half']
    weight = species_obj.params['w_half']
    num_animals = 10
    animal = species_obj(weight, age)

    for _ in range(20):
        newborn = animal.giving_birth(species_str, num_animals)
        assert all((newborn, type(newborn) == species_obj))


@pytest.mark.parametrize('species_obj, species_str', [(Herbivore, 'Herbivore'), (Carnivore, 'Carnivore')])
def test_giving_birth_weight(species_obj, species_str):
    """Test weight loss if animal gives birth.
    Adjust parameters to assure birth."""
    species_obj.set_params({'xi': 0.0001, 'zeta': 0, 'gamma': 0.5, 'sigma_birth': 0.2})
    age = species_obj.params['a_half']
    weight = species_obj.params['w_half']
    num_animals = 10
    animal = species_obj(weight, age)

    for _ in range(20):
        initial_weight = animal.weight
        animal.giving_birth(species_str, num_animals)
        assert animal.weight < initial_weight


@pytest.mark.parametrize('species_obj, species_str', [(Herbivore, 'Herbivore'), (Carnivore, 'Carnivore')])
def test_giving_birth_false(species_obj, species_str):
    """"Test correct return value if animal does not gives birth.
    Let animal be alone in landscape to assure no birth takes place."""
    animal = species_obj(12.5, 10)
    newborn = animal.giving_birth(species_str, 1)
    assert not newborn


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_death_probability_starved(mocker, species):
    """Test that animal always dies if starved."""
    mocker.patch('biosim.animals.uniform', return_value=1)
    starved_animal = species(0, 10)
    for _ in range(20): #Necessary with for loop?
        assert starved_animal.probability_of_death()


@pytest.mark.parametrize('species', [Herbivore, Carnivore])
def test_death_probability_sick(mocker, species):
    mocker.patch('biosim.animals.uniform', return_value=0)
    sick_animal = species(12.5, 10)
    for _ in range(20):
        assert sick_animal.probability_of_death()