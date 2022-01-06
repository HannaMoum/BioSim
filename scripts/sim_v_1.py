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

# Turning initial list of information into list of Herbivores
initial_pop = []
for animal in ini_herb_pop:
    if animal['Species'] == 'Herbivore':
        initial_pop.append(Herbivore(animal['age'], animal['weight']))
for an in initial_pop:
    print(an.params)


sim = Lowland(initial_pop)


def cycle(simulation):
    simulation.grassing()
    simulation.give_birth()
    simulation.aging()
    simulation.death()
    simulation.regrowth()


for year in range(100):
    cycle(sim)
    print(len(sim.herb_pop))
