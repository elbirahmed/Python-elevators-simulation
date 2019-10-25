# elevators
The elevators simulator module
=============================

Simulation of a platform handling elevators on a building.

.. module:: elevator.py

.. author:: Ahmed EL BIR <ahmed.elbyr@gmail.com>

Rules:
-----

The ``Platform`` handles ``nb_floor`` floor in a building with ``nb_elevator`` elevators
A Call for an elevator can be external of the elevator's cabin  (just the sens UP, DOWN) or internal
of the elevator's cabin to indicate the destination floor
The destination floor number of the internal call must be in the same sens of  the sens of the external call
An elevator handles only call that are within its same sens ("UP", "DOWN")
When there is no call to handle all  elevators must be in HOLD at the first floor waiting for calls

