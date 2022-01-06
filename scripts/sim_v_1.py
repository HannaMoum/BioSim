""" Simulating only herbivores and lowland
"""
from biosim.animals import Herbivore
from biosim.landscapes import Lowland

#Herbivore.set_params({'omega': 0.2, 'gamma': 0.7})
sim = Lowland(20)

new_params = {'f_max': 800}
sim.set_params(new_params)

ini_herb_pop = [{'Species': 'Herbivore', 'age': 10, 'weight': 12.5},
                {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
                {'Species': 'Herbivore', 'age': 10, 'weight': 12.5},
                {'species': 'Herbivore', 'age': 9, 'weight': 10.3}]

def cycle(sim):
    sim.grassing()
    sim.give_birth()
    sim.aging()
    sim.death()
    sim.regrowth()

for year in range(10):
    cycle(sim)
    print(len(sim.herb_pop))
