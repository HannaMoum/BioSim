Simulation and Island
=========================

The simulation module
---------------------
The simulation module simulates the entire evolution from start to end.
This module works as the user interface for running the simulation,
and complete examples are provided in the examples repository available from GitLab (see README).

The main events of one annual simulation cycle for the evolution is:

    #. Regrowth of all fodder
    #. All animals eat in order; Herbivores before carnivores.
    #. Procreation
    #. Migration
    #. Aging and weightloss
    #. Death

.. automodule:: biosim.simulation
   :members:
   :private-members:

The island module
---------------------
The island module provides necessary maps for the island, to ensure a dynamic evolution
consisting of migration and interaction for all animals. All life and actions stays within
the island.

.. automodule:: biosim.world
   :members:
   :private-members:



