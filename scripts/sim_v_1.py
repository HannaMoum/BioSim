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
#Herbivore.set_params(new_params)
#Herbivore.set_params({'omega': 0.2, 'gamma': 0.7})

# Turning initial list of information into list of Herbivores
initial = []
for animal in ini_herb_pop:
    if animal['Species'] == 'Herbivore':
        initial.append(Herbivore(animal['age'], animal['weight']))

sim = Lowland(initial)

#new_params = {'f_max': 800}
#sim.set_params(new_params)

def cycle(sim):
    sim.grassing()
    sim.give_birth()
    sim.aging()
    sim.death()
    sim.regrowth()

for year in range(100):
    cycle(sim)
    print(len(sim.herb_pop))
