""" Simulating only herbivores and lowland
"""
from biosim.animals import Herbivore
from biosim.landscapes import Lowland

# Creating initial population as list/dicts
ini_herb_pop = [{'Species': 'Herbivore', 'age': 10, 'weight': 12.5},
                {'Species': 'Herbivore', 'age': 9, 'weight': 10.3},
                {'Species': 'Herbivore', 'age': 10, 'weight': 12.5},
                {'Species': 'Herbivore', 'age': 9, 'weight': 10.3}]

# Adjusting parameters
# new_params_herbivore = {'omega': 0.7, 'gamma': 0.3}
# Herbivore.set_params(new_params_herbivore)
# new_params_landscape = {'f_max': 600}
# Lowland.set_params(new_params_landscape)


# Be aware; Currently awful variable names
class Simulation:

    def __init__(self, initial_population):
        self.initial_population = initial_population

    def create_herb_list(self):
        # Turning initial list of information into list of Herbivores
        # NOW: Assuming we only have herbivores
        pop_reorganised = []
        for animal in self.initial_population:
            if animal['Species'] == 'Herbivore':
                pop_reorganised.append(Herbivore(animal['age'], animal['weight']))
        return pop_reorganised

    def cycle(self, herbs_in_one_field):
        herbs_in_one_field.grassing()
        herbs_in_one_field.give_birth()
        herbs_in_one_field.aging()
        herbs_in_one_field.death()
        herbs_in_one_field.regrowth()

    def run(self, years):
        herbs = self.create_herb_list()
        to_be_simulated = Lowland(herbs)
        for year in range(years):
            self.cycle(to_be_simulated)
            print(f'Number of herbivores after year {year}: {len(to_be_simulated.herb_pop)}')


my_sim = Simulation(ini_herb_pop)
my_sim.run(100)


