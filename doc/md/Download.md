% openSDUC documentation master file, created by Andres Ramos

# Download & Installation

The **openSDUC** has been tested using these latest versions [Python 3.13.7](https://www.python.org/) and [Pyomo 6.10.0](https://pyomo.readthedocs.io/en/stable/), and it uses [Gurobi 13.0.1](https://www.gurobi.com/products/gurobi-optimizer/) as a commercial MIP solver for which a free academic license is available.
It uses Pyomo so that it is independent of the preferred solver. You can alternatively use one of the free solvers [HiGHS 1.14.0](https://pypi.org/project/highspy/), [SCIP 10.0.2](https://www.scipopt.org/index.php#download), [GLPK 5.0](https://www.gnu.org/software/glpk/)
and [CBC 2.10.13](https://github.com/coin-or/Cbc/releases). List the serial solver interfaces under Pyomo with this call:

```
pyomo help -s
```

Gurobi, HiGHS, SCIP, or GLPK solvers can be installed as a package:

```
conda install -c gurobi      gurobi
pip   install                highspy
conda install -c conda-forge pyscipopt
conda install                glpk
```

Besides, it also requires the following packages:

- [Pandas](https://pandas.pydata.org/) for inputting data and outputting results
- [Matplotlib](https://matplotlib.org/) for plotting some results

## Cases

Here, you have the input files of a small case study of [16 generators](https://github.com/IIT-EnergySystemModels/openSDUC/tree/main/openSDUC/16g).

## Code

The **openSDUC** code is provided under the [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html):

- the code can't become part of a closed-source commercial software product
- any future changes and improvements to the code remain free and open

Source code can be downloaded from [GitHub](https://github.com/IIT-EnergySystemModels/openSDUC) or installed with [pip](https://pypi.org/project/openSDUC/)

This model is a work in progress and will be updated accordingly. If you want to subscribe to the **openSDUC** model updates send an email to <mailto:andres.ramos@comillas.edu>
