============================================
Inglourious Basterds' Hashcode 2018 Solution
============================================

This repo contains Inglourious Basterds team soulution
to `Google Hashcode 2018`_ problem.

The idea of the solution changed during the competition in the following way:

1. Randomly choosing rides for cars
2. Choosing the closest ride to the car
3. Do not take the rides, which won't be completed in time
4. Chose ride based on its value per step

Solution is implemented using `Python`_ programming language without any
library dependencies.

Requirements:
-------------

- Python 3.6 or higher

Running:
--------

.. code::
   bash

   python main.py in/a_example.in out/a_example.out


Here ``in/a_example.in`` is the problem input file and
``out/a_example.out`` is file to which problem solution will be output.

.. _`Google Hashcode 2018`: https://g.co/hashcode
.. _`Python`: https://python.org
