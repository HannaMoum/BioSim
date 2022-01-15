##BioSim A15 Cassandra Hanna
#BioSim Island Simulation

BioSim provides a compound simulation of an island's evolution.

##Background and motivation
This project is made on behalf of Pylandia's Environmental Protection Agency (PEPA), 
and a direct result of the course INF200 running at the Norwegian University of Life Sciences
(NMBU) in 2022. Its' goal is to investigate the stability of the ecosystem on Rossumøya and
provide data on possible preservation of Rossumøya as a nature park.

##Project descritption
The BioSim simulation runs with the following implemented aspects:
* Two species of animals are allowed to evolve on the island. 
The species are herbivores and carnivores, with both similar and independent traits.
* Four different landscapes provides different migration and 
eating opportunities. The landscapes are lowland, highland, desert and water.
* All aspects and actions stays within the created island.

BioSim provides a simualtion of animals' evolution over time on an island.
The evolution is affected both by randomness and changeable traits for each species 
and landcapes (presented as parameters).
Provided graphics visualize populationevolution, heat-maps for evolution in populationdensity,
and histograms for the evolution of the animals' age, weigth and fitness.

##Dependencies
Python > 3.8

##Contents
* src: The source code biosim Package
* reference_examples: Examples for using the package
* tests: A testsuite

##Further Development
For further development the authors recommend:
* optimizing the hierarchy structure
* provide the Landscape class with one attribute for each animal's species
population, rather than one for both. This should save some runningtime for the simulation.
* Investigate optimization possibilities in current code 
to provide better efficiency.

##Credits
Projectcode developed and tested in a collaboration between Cassandra Hjortdahl and Hanna Lye Moum.
Lectures and guidance given by Hans Ekkehard Plesser.

##Licence
MIT




A README.md contains a description of the distribution package, 
and usually contain some information to the user about how to install
it and where to look for examples/documentation. The file type is flexible,
but Markdown is common