""" Simulating only herbivores and lowland
"""
from biosim.animals import Herbivore
from biosim.landscapes import Lowland

#Herbivore.set_params({'omega': 0.2, 'gamma': 0.7})
sim = Lowland(20)

new_params = {'f_max': 800}
sim.set_params(new_params)

#new_params = {'omega': 0.2} Does not work because this parameter is for Herbivore and not Lowland
#sim.set_params(new_params)
#print(sim.params)

def cycle(sim):
    sim.grassing()
    sim.give_birth()
    sim.aging()
    sim.death()
    sim.regrowth()

for year in range(10):
    cycle(sim)
    print(len(sim.herb_pop))
