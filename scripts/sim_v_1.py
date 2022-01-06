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


class Simulation:

    def __init__(self, initial_population):
        self.initial_population = initial_population

    def create_herb_list(self):
        # Turning initial list of information into list of Herbivores
        # NOW: Assuming we only have herbivores
        herb_list = []
        for animal in self.initial_population:
            if animal['Species'] == 'Herbivore':
                herb_list.append(Herbivore(animal['age'], animal['weight']))
        return herb_list

    def cycle(self, loc_with_herbs):
        loc_with_herbs.grassing()
        loc_with_herbs.give_birth()
        loc_with_herbs.aging()
        loc_with_herbs.death()
        loc_with_herbs.regrowth()

    def run(self, years):
        herbs = self.create_herb_list()
        location = Lowland(herbs)
        for year in range(years):
            self.cycle(location)
            print(f'Number of herbivores after year {year}: {len(location.herb_pop)}')


my_sim = Simulation(ini_herb_pop)
my_sim.run(100)


