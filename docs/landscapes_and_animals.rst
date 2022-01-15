Landscapes and Animals
=========================

The landscape module
---------------------
The landscape module provides a class Landscape.
Each landscape has its' own specific terrain type, and keeps track of
the animals currently living there, as well as control all interaction between animals
and their evolution.

.. automodule:: biosim.landscape
   :members:


The animal module
---------------------
The animal module provides a class Animal with two subclasses; Herbivore and Carnivore.
Each animal represents an object with specified characteristics.
Different characteristics are given as attributes/parameters/properties,
while abilities and actions are given by methods.

Each animal is given a set of default parameters that by option can be changed.
Overview and explanation is to be found in table below:

+-------------------------+------------+------------+
| Parameter               | Herbivore  | Carnivore  |
+=========================+============+============+
| :math:`w_{birth}`       | 8.0        | 6.0        |
+-------------------------+------------+------------+
| :math:`\sigma_{birth}`  | 1.5        | 1.0        |
+-------------------------+------------+------------+
| :math:`\beta`           | 0.9        | 0.75       |
+-------------------------+------------+------------+
| :math:`\eta`            | 0.05       | 0.125      |
+-------------------------+------------+------------+
| :math:`a_{\frac{1}{2}}` | 40.0       | 40.0       |
+-------------------------+------------+------------+
| :math:`\phi_{age}`      | 0.6        | 0.3        |
+-------------------------+------------+------------+
| :math:`w_{\frac{1}{2}}` | 10.0       | 4.0        |
+-------------------------+------------+------------+
| :math:`\phi_{weight}`   | 0.1        | 0.4        |
+-------------------------+------------+------------+
| :math:`\mu`             | 0.25       | 0.4        |
+-------------------------+------------+------------+
| :math:`\gamma`          | 0.2        | 0.8        |
+-------------------------+------------+------------+
| :math:`\zeta`           | 3.5        | 3.5        |
+-------------------------+------------+------------+
| :math:`\xi`             | 1.2        | 1.1        |
+-------------------------+------------+------------+
| :math:`\omega`          | 0.4        | 0.8        |
+-------------------------+------------+------------+
| :math:`F`               | 10.0       | 50.0       |
+-------------------------+------------+------------+
| :math:`\Delta\Phi_{max}`| ---        | 10.0       |
+-------------------------+------------+------------+



.. automodule:: biosim.animals
   :members:
