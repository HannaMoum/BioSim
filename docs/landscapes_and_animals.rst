Landscapes and Animals
=========================

The landscape module
---------------------
The landscape module provides a class Landscape.
Each landscape has its' own specific terrain type, and keeps track of
the animals currently living there, as well as control all interaction between animals
and their evolution.

Landscapes are given a default parametervalue that by option can be changed for two of the landscapes,
while the others are unchangeable. See below:

+-------------------+---------+----------+-------------+-------------+-----------------------------------+
| Parameter         | Lowland | Highland | Desert      | Water       | Explanation                       |
+===================+=========+==========+=============+=============+===================================+
| :math:`f_{max}`   | 800.0   | 300.0    | 0.00        | 0.00        | Total available fodder.           |
|                   |         |          | (static)    | (static)    | Unchangeable for desert and water.|
+-------------------+---------+----------+-------------+-------------+-----------------------------------+

.. automodule:: biosim.landscape
   :members:


The animal module
---------------------
The animal module provides a class Animal with two subclasses; Herbivore and Carnivore.
Each animal represents an object with specified characteristics.
Different characteristics are given as attributes/parameters/properties,
while the traits are given as methods.

Each animal is given a set of default parameters affecting their evolution that by
option can be changed. Overview and explanation is to be found in table below:

+-------------------------+------------+------------+----------------------------------------------+
| Parameter               | Herbivore  | Carnivore  | Explanation                                  |
+=========================+============+============+==============================================+
| :math:`w_{birth}`       | 8.0        | 6.0        | mean birth weight                            |
+-------------------------+------------+------------+----------------------------------------------+
| :math:`\sigma_{birth}`  | 1.5        | 1.0        | standard deviation for birth weight          |
+-------------------------+------------+------------+----------------------------------------------+
| :math:`\beta`           | 0.9        | 0.75       | weight increase factor                       |
+-------------------------+------------+------------+----------------------------------------------+
| :math:`\eta`            | 0.05       | 0.125      | weight decrease factor                       |
+-------------------------+------------+------------+----------------------------------------------+
| :math:`a_{\frac{1}{2}}` | 40.0       | 40.0       | age factor for fitness calculation           |
+-------------------------+------------+------------+----------------------------------------------+
| :math:`\phi_{age}`      | 0.6        | 0.3        | factor for fitness calculation               |
+-------------------------+------------+------------+----------------------------------------------+
| :math:`w_{\frac{1}{2}}` | 10.0       | 4.0        | weight factor for fitness calculation        |
+-------------------------+------------+------------+----------------------------------------------+
| :math:`\phi_{weight}`   | 0.1        | 0.4        | factor for fitness calculation               |
+-------------------------+------------+------------+----------------------------------------------+
| :math:`\mu`             | 0.25       | 0.4        | factor for migration probability             |
+-------------------------+------------+------------+----------------------------------------------+
| :math:`\gamma`          | 0.2        | 0.8        | factor providing probability to give birth   |
+-------------------------+------------+------------+----------------------------------------------+
| :math:`\zeta`           | 3.5        | 3.5        | factor providing probability to give birth   |
+-------------------------+------------+------------+----------------------------------------------+
| :math:`\xi`             | 1.2        | 1.1        | weight reduction factor after birth          |
+-------------------------+------------+------------+----------------------------------------------+
| :math:`\omega`          | 0.4        | 0.8        | factor for death probability                 |
+-------------------------+------------+------------+----------------------------------------------+
| :math:`F`               | 10.0       | 50.0       | yearly wanted food amount                    |
+-------------------------+------------+------------+----------------------------------------------+
| :math:`\Delta\Phi_{max}`| ---        | 10.0       | denominator for hunting success probability  |
+-------------------------+------------+------------+----------------------------------------------+



.. automodule:: biosim.animals
   :members:
   :private-members:

