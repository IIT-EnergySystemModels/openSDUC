.. openSDUC documentation master file, created by Andres Ramos

Download & Installation
=======================
The **openSDUC** has been developed using `Python 3.13.2 <https://www.python.org/>`_ and `Pyomo 6.9.2 <https://pyomo.readthedocs.io/en/stable/>`_, and it uses `Gurobi 12.0.2 <https://www.gurobi.com/products/gurobi-optimizer/>`_ as a commercial MIP solver for which a free academic license is available.
It uses Pyomo so that it is independent of the preferred solver.  You can alternatively use one of the free solvers `HiGHS 1.11.0 <https://ergo-code.github.io/HiGHS/dev/installation/#Precompiled-Binaries>`_, `SCIP 9.2.2 <https://www.scipopt.org/index.php#download>`_, `GLPK 5.0 <https://www.gnu.org/software/glpk/>`_
and `CBC 2.10.12 <https://github.com/coin-or/Cbc/releases>`_. List the serial solver interfaces under Pyomo with this call::

  pyomo help -s

Gurobi, HiGHS, SCIP, or GLPK  solvers can be installed as a package::

  conda install -c gurobi      gurobi
  pip   install                highspy
  conda install -c conda-forge pyscipopt
  conda install                glpk

Besides, it also requires the following packages:

- `Pandas <https://pandas.pydata.org/>`_ for inputting data and outputting results
- `Matplotlib <https://matplotlib.org/>`_ for plotting some results

Cases
-----
Here, you have the input files of a small case study of 16 generators.

Code
----

The **openSDUC** code is provided under the `GNU Affero General Public License <https://www.gnu.org/licenses/agpl-3.0.en.html>`_:

- the code can't become part of a closed-source commercial software product
- any future changes and improvements to the code remain free and open

Source code can be downloaded from `GitHub <https://github.com/IIT-EnergySystemModels/openSDUC>`_.

This model is a work in progress and will be updated accordingly. If you want to subscribe to the **openSDUC** model updates send an email to andres.ramos@comillas.edu
