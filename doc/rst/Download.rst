.. openSDUC documentation master file, created by Andres Ramos

Download
========
The **openSDUC** has been developed using `Python 3.9.13 <https://www.python.org/>`_ and `Pyomo 6.4.2 <https://pyomo.readthedocs.io/en/stable/>`_ and it uses `Gurobi 9.5.2 <https://www.gurobi.com/products/gurobi-optimizer/>`_ as commercial MIP solver for which a free academic license is available.
It uses Pyomo so that it is independent of the preferred solver. You can alternatively use one of the free solvers `SCIP 8.0.1 <https://www.scipopt.org/>`_, `GLPK 5.0 <https://www.gnu.org/software/glpk/>`_
and `CBC 2.10.8 <https://github.com/coin-or/Cbc>`_. List the serial solver interfaces under Pyomo with this call::

  pyomo help -s

Gurobi solver is installed as a package::

  conda install -c gurobi gurobi

Besides, it also requires the following packages:

- `Pandas <https://pandas.pydata.org/>`_ for inputting data and outputting results
- `Matplotlib <https://matplotlib.org/>`_ for plotting some results

Cases
-----
Here, you have the input files of a small case study of 16 generators.

Code
----

The **openSDUC** code is provided under the `GNU General Public License <https://www.gnu.org/licenses/gpl-3.0.html>`_:

- the code can't become part of a closed-source commercial software product nor can be used for commercial purposes (only for research purposes)
- any future changes and improvements to the code remain free and open

Source code can be downloaded from `GitHub <https://github.com/IIT-EnergySystemModels/openSDUC>`_.

This model is a work in progress and will be updated accordingly. If you want to subscribe to the **openSDUC** model updates send an email to andres.ramos@comillas.edu
