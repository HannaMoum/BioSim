""" Simulating only herbivores and lowland
"""
from biosim.animals import Herbivore
from biosim.landscapes import Lowland

# Creating initial population as list/dicts
ini_herb_pop = [{'Species': 'Herbivore', 'age': 10, 'weight': 12.5},
                {'Species': 'Herbivore', 'age': 11, 'weight': 10.3},
                {'Species': 'Herbivore', 'age': 12, 'weight': 12.5},
                {'Species': 'Herbivore', 'age': 13, 'weight': 10.3},
                {'Species': 'Herbivore', 'age': 14, 'weight': 12.5},
                {'Species': 'Herbivore', 'age': 15, 'weight': 10.3},
                {'Species': 'Herbivore', 'age': 16, 'weight': 12.5},
                {'Species': 'Herbivore', 'age': 17, 'weight': 10.3}]

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
    sim.regrowth()
    sim.grassing()
    sim.give_birth()
    sim.aging()
    sim.death()


for year in range(100):
    cycle(sim)
    print('-' * 30)
    print(f'Year: {year}   ', end='')
    print('Pop:', len(sim.herb_pop))

    #for i in sim.herb_pop:
        #print(i.age, i.weight, i.fitness)

