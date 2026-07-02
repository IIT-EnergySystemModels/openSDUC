
[![openSDUC](doc/img/openSDUC.jpg)](https://opensduc.readthedocs.io/en/latest/index.html)

[![PyPI](https://badge.fury.io/py/openSDUC.svg)](https://badge.fury.io/py/openSDUC)
[![versions](https://img.shields.io/pypi/pyversions/openSDUC.svg)](https://pypi.python.org/pypi/openSDUC)
[![docs](https://img.shields.io/readthedocs/opensduc)](https://opensduc.readthedocs.io/en/latest/index.html)
[![AGPL](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://github.com/IIT-EnergySystemModels/openSDUC/blob/master/LICENSE)
[![pepy](https://static.pepy.tech/badge/openSDUC)](https://pepy.tech/project/openSDUC)

**Open Stochastic Daily Unit Commitment of Thermal and ESS Units (openSDUC)**

It determines the system operation to supply the demand at minimum cost.

The **openSDUC** model presents a decision support system for defining the generation operation of a large-scale electric system.

The scope of the model corresponds to one day or one week, divided into load levels: 01-01 00:00:00+01:00 to 01-07 23:00:00+01:00.
The time division allows a flexible representation of the periods for evaluating the system operation, for example, as 84 two-hour periods or as the 168 hours of the week.

It considers stochastic short-term uncertainties (scenarios) related to the system operation. The operation scenarios are associated with renewable energy sources and electricity demand.

The model formulates an optimization problem that includes binary and continuous operation decisions.

The **unit commitment (UC)** model is based on a **tight and compact** formulation that includes operating reserves. It considers different **energy storage systems (ESS)**, e.g., pumped-storage hydro,
batteries, etc.

The main results of the model can be structured into these topics:

- **Operation**: the output of different units and technologies (thermal, storage hydro, pumped-storage hydro, RES), RES curtailment
- **Emissions**: CO2
- **Marginal**: Short-Run Marginal Costs (SRMC)

A careful implementation has been carried out to avoid numerical problems by scaling parameters, variables, and equations of the optimization problem, allowing the model to be used for large-scale cases.

# Installation

There are 2 ways to get all the required packages under Windows. We recommend using the Python distribution Miniconda. If you don't want to use it or already have an existing Python (version 3.11) installation, you can also download the required packages by yourself.

## Miniconda (recommended)

1. [Miniconda](https://docs.conda.io/en/latest/miniconda.html). Choose the 64-bit installer if possible.

   1. During the installation procedure, keep both checkboxes "modify the PATH" and "register Python" selected! If only higher Python versions are available, you can switch to a specific Python version by typing `conda install python=<version>`
   2. **Remark:** if Anaconda or Miniconda was installed previously, please check that Python is registered in the environment variables.

2. **Packages and Solver**:

   1. Launch a new command prompt (Windows: Win+R, type "cmd", Enter)
   2. [HiGHS](https://ergo-code.github.io/HiGHS/dev/installation/#Precompiled-Binaries) is our recommendation if you want a free and open-source solver.
   3. Install openSDUC via pip by `pip install openSDUC`

# Solvers

## HiGHS

The [HiGHS solver](https://ergo-code.github.io/HiGHS/dev/interfaces/python/#python-getting-started) can also be used. It can be installed using: `pip install highspy`.
This solver is activated by calling the openSDUC model with the solver name 'appsi_highs'.

## Gurobi

Another recommendation is the use of [Gurobi solver](https://www.gurobi.com/). However, it is a commercial solver, more powerful than open-source solvers for large-scale problems.
As a commercial solver, it needs a license that is free of charge for academic usage by signing up on the [Gurobi webpage](https://pages.gurobi.com/registration/). You can also ask for an [evaluation license](https://www.gurobi.com/downloads/request-an-evaluation-license/) for 30 days to test the solver.
It can be installed using: `conda install -c gurobi gurobi` and then ask for an academic or commercial license. Activate the license on your computer using the `grbgetkey` command (you need to be in a university internet domain if you are installing an academic license).

## GLPK

As an easy option for installation, we have the free and open-source [GLPK solver](https://www.gnu.org/software/glpk/). However, it takes too much time for large-scale problems. It can be installed using: `conda install glpk`.

## CBC

The [CBC solver](https://github.com/coin-or/Cbc) is also another free and open-source solver. For Windows users, the effective way to install the CBC solver is to download the binaries from this [site](https://www.coin-or.org/download/binary/Cbc/), copy and paste the *cbc.exe* file to the PATH that is the "bin" directory of the Anaconda or Miniconda environment. Under Linux, it can be installed using: `conda install -c conda-forge coincbc`.

## Mosek

Another alternative is the [Mosek solver](https://www.mosek.com/). Note that it is a commercial solver, and you need a license for it. Mosek is a good alternative to deal with QP, SOCP, and SDP problems. You only need to use `conda install -c mosek mosek` for installation and request a license (academic or commercial). To request the academic one, you can request [here](https://www.mosek.com/products/academic-licenses/).
Mosek also provides a [license guide](https://docs.mosek.com/9.2/licensing/index.html). If you request an academic license, you will receive it by email and only need to place it in the path `C:\Users\<username>\mosek` on your computer.

## Users

If you are not planning on developing, please follow the instructions in the [Installation](#installation).

Once installation is complete, [openSDUC](https://github.com/IIT-EnergySystemModels/openSDUC/tree/master) can be executed in a test mode by using a command prompt.
In the directory of your choice, open and execute the openSDUC_run.py script by using the following on the command prompt (Windows) or Terminal (Linux). (Depending on what your standard Python version is, you might need to call `python3` instead of `python`.):

> `openSDUC_Main`

Then, three parameters (case, dir, and solver) will be asked for.

**Remark:** at this step, only press enter for each input and openSDUC will be executed with the default parameters.

After this, in a directory of your choice, make a copy of the [16g](https://github.com/IIT-EnergySystemModels/openSDUC/tree/master/openSDUC/16g) case to create a new case of your choice but using the current format of the CSV files.
A proper execution by `openSDUC_Main` can be made by introducing the new case and the directory of your choice. Note that the solver is **glpk** by default, but it can be changed to other solvers that Pyomo supports (e.g., gurobi, mosek).

Then, the **results** are written to the folder named after the case. The results contain plots and summary spreadsheets for multiple optimized scenarios and load levels.

**Note that** there is an alternative way to run the model: create a new script **script.py** and write the following:

> `from openSDUC.openSDUC_main import openSDUC_run`
>
> `openSDUC_run(<dir>, <case>, <solver>)`
