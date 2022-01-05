""" Simulating only herbivores and lowland
"""
from biosim.animals import Herbivore
from biosim.landscapes import Lowland

sim = Lowland(5)

def cycle(sim):
    sim.grassing()
    sim.give_birth()
    sim.aging()
    sim.death()
    sim.regrowth()


for year in range(100):
    cycle(sim)
    print(len(sim.herb_pop))
