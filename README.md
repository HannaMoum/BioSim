##BioSim A15 Cassandra Hanna
#BioSim Island Simulation

BioSim provides a compound simulation of an island's evolution.

##Background and motivation
This project is made on behalf of Pylandia's Environmental Protection Agency (PEPA), 
and a direct result of the course INF200 running at the Norwegian University of Life Sciences
(NMBU) in 2022. The goal is to investigate the stability of the ecosystem on Rossumøya and
provide data on possible preservation of Rossumøya as a nature park.

##Project description
The BioSim simulation runs with the following implemented aspects:
* Two species of animals are allowed to evolve on the island. 
The species are herbivores and carnivores, with both similar and independent traits.
* Four different landscapes provides different migration and 
eating opportunities. The landscapes are lowland, highland, desert and water.
* All aspects and actions stays within the created island.

BioSim provides a simulation of animals' evolution over time on an island.
The evolution is affected both by randomness and changeable traits for each species 
and landscapes (presented as parameters).
Provided graphics visualize population evolution, heat-maps for evolution in population density,
and histograms for the evolution of the animals' age, weight and fitness.

Please find the full project description below:
https://gitlab.com/nmbu.no/emner/inf200/h2021/inf200-course-materials/-/blob/main/january_block/INF200_H21_BioSimJan_v2.pdf

##Dependencies
Python > 3.8

##Contents
* src: The source code biosim Package
* examples: Examples for using the package
* reference_examples: Examples for using the package given by EPAP
* tests: A testsuite
* documentation: for documentation go to
```
|-- docs
    |-- _build
        |-- html
           |-- index.html
```
##Further Development
For further development the authors recommend:
* optimizing the hierarchy structure
* investigate optimization possibilities in current code 
to provide better efficiency, such as:
  * provide the Landscape class with one attribute for each animal's species
population, rather than one for both. This should save some runtime for the simulation.
  
  * opportunities to make the graphics faster.
* fix bug concerning log_file. In current version log_file is created
despite any input from the user.

##Credits
Project developed and tested in a collaboration between Cassandra Hjortdahl and Hanna Lye Moum.
Lectures and guidance given by Hans Ekkehard Plesser.

##GitLab
Below is the provided link for access to the entire project repository:
https://gitlab.com/nmbu.no/emner/inf200/h2021/january-teams/a15_cassandra_hanna/biosim-a15-cassandra-hanna/-/tree/main

##Licence
MIT

