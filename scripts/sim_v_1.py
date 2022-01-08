""" Simulating only herbivores and lowland
"""
from biosim.animals import Herbivore
from biosim.animals import Carnivore
from biosim.lowland import Lowland

# Creating initial population as list/dicts

ini_herb_pop = [{'Species': 'Herbivore', 'age': 5, 'weight': 6} for _ in range(10)]
ini_carn_pop = [{'Species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(50)]


                # {'Species': 'Herbivore', 'age': 11, 'weight': 10.3},
                # {'Species': 'Herbivore', 'age': 12, 'weight': 12.5},
                # {'Species': 'Herbivore', 'age': 13, 'weight': 10.3},
                # {'Species': 'Herbivore', 'age': 14, 'weight': 12.5},
                # {'Species': 'Herbivore', 'age': 15, 'weight': 10.3},
                # {'Species': 'Herbivore', 'age': 16, 'weight': 12.5},
                # {'Species': 'Herbivore', 'age': 17, 'weight': 10.3}]


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

    # def create_carn_list(self):
    #     # Turning initial list of information into list of Herbivores
    #     # NOW: Assuming we only have herbivores
    #     carn_list = []
    #     for animal in self.initial_population:
    #         if animal['Species'] == 'Herbivore':
    #             herb_list.append(Herbivore(animal['age'], animal['weight']))
    #     return herb_list

    def cycle(self, location):
        location.regrowth()
        location.grassing()
        location.hunting()
        location.give_birth()
        location.age_and_weightloss()
        location.death()


    def run(self, years):
        herbs = self.create_herb_list()
        carns = [Carnivore(5, 8.1),
                Carnivore(3, 7.3),
                Carnivore(5, 8.1),
                Carnivore(4, 6.7),
                Carnivore(3, 12.0),
                Carnivore(8, 8.1),
                Carnivore(1, 4.0),
                Carnivore(5, 8.1)]
        location = Lowland(herbs, carns)
        for year in range(years):
            self.cycle(location)
            print(f'Number of animals after year {year}: h: {len(location.herb_pop)}  c: {len(location.carn_pop)}')


my_sim = Simulation(ini_herb_pop)
my_sim.run(100)


