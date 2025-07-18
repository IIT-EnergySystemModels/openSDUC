.. openSDUC documentation master file, created by Andres Ramos

Introduction
============
The *Open Stochastic Daily Unit Commitment of Thermal and ESS Units* **(openSDUC)** determines the system operation for supplying the demand at minimum cost.

The **openSDUC** model presents a decision support system for defining the generation operation of a large-scale electric system.

The model's scope corresponds to one day or one week, divided into load levels: 01-01 00:00:00+01:00 to 01-21 23:00:00+01:00.
The time division allows a flexible representation of the periods for evaluating the system operation, for example, by 84 periods of two hours or by the 168 hours of the week.

It considers stochastic short-term yearly uncertainties (scenarios) related to the system operation. The operation scenarios are associated with renewable energy sources and electricity demand.
  
The model formulates an optimization problem that includes binary and continuous operation decisions.

The **unit commitment (UC)** model is based on a **tight and compact** formulation including operating reserves. It considers different **energy storage systems (ESS)**, e.g., pumped-storage hydro,
battery, etc. 

The main results of the model can be structured into these topics:
  
- **Operation**: the output of different units and technologies (thermal, storage hydro, pumped-storage hydro, RES), RES curtailment
- **Emissions**: CO2
- **Marginal**: Short-Run Marginal Costs (SRMC)

A careful implementation has been done to avoid numerical problems by scaling parameters, variables, and equations of the optimization problem, allowing the model to be used for large-scale cases.
