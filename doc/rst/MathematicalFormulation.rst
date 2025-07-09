.. openSDUC documentation master file, created by Andres Ramos

Mathematical Formulation
========================
Here we present the mathematical formulation of the optimization problem solved by the **openSDUC** model.

* D.A. Tejada-Arango, S. Lumbreras, P. Sánchez-Martín, and A. Ramos "Which Unit-Commitment Formulation is Best? A Systematic Comparison" IEEE Transactions on Power Systems 35 (4): 2926-2936, Jul 2020 `10.1109/TPWRS.2019.2962024 <https://doi.org/10.1109/TPWRS.2019.2962024>`_

Indices
-------
===========  ========================================================
:math:`ω`    Scenario
:math:`n`    Load level
:math:`\nu`  Time step. Duration of each load level (e.g., 2 h, 3 h)
:math:`g`    Generator (thermal or hydro unit or ESS)
:math:`t`    Thermal unit
:math:`e`    Energy Storage System (ESS)
===========  ========================================================

Parameters
----------

They are written in capital letters.

==============  ====================================================  =======
**Demand**                                                   
--------------  ----------------------------------------------------  -------
:math:`D_n^ω`   Demand                                                GW
:math:`DUR_n`   Duration of each load level                           h
:math:`CENS`    Cost of energy not served. Value of Lost Load (VoLL)  €/MWh
==============  ====================================================  =======

==============  =============================  ====
**Scenarios**                                
--------------  -----------------------------  ----
:math:`P^ω`     Probability of each scenario   p.u.
==============  =============================  ====

===========================  ======================================  ==
**Operating reserves**                                         
---------------------------  --------------------------------------  --
:math:`UR_n^ω, DR_n^ω`       Upward and downward operating reserves  GW
===========================  ======================================  ==

=========================================  =======================================================================================================  ===========
**Generation system**   
-----------------------------------------  -------------------------------------------------------------------------------------------------------  -----------
:math:`\underline{CP}_g, \overline{GP}_g`  Minimum load and maximum output of a generator                                                           GW
:math:`\overline{GC}_g`                    Maximum consumption of an ESS                                                                            GW
:math:`CF_g, CV_g`                         Fixed and variable cost of a generator. Variable cost includes fuel, O&M and emission cost               €/h, €/MWh
:math:`RU_t, RD_t`                         Ramp up and ramp down of a thermal unit                                                                  MW/h
:math:`TU_t, TD_t`                         Minimum uptime and downtime of a thermal unit                                                            h
:math:`CSU_g, CSD_g`                       Startup and shutdown cost of a committed unit                                                            M€
:math:`\tau_e`                             Characteristic duration of the ESS (e.g., 24 h, 168 h, 672 h -for monthly-)                              h
:math:`EF_e`                               Round-trip efficiency of the pump/turbine cycle of a hydro power plant or charge/discharge of a battery  p.u.
:math:`I_e`                                Capacity of an ESS (e.g., hydro power plant)                                                             GWh
:math:`EI_{ne}^ω`                          Energy inflows of an ESS (e.g., hydro power plant)                                                       GWh
=========================================  =======================================================================================================  ===========

Variables
---------

They are written in lower letters.

===============  ==================  ===
**Demand**                         
---------------  ------------------  ---
:math:`ens_n^ω`  Energy not served   GW
===============  ==================  ===

=================================  ==========================================================================  =====
**Generation system**   
---------------------------------  --------------------------------------------------------------------------  -----
:math:`gp_{ng}^ω, gc_{ng}^ω`       Generator output (discharge if an ESS) and consumption (charge if an ESS)   GW
:math:`p_{ng}^ω`                   Generator output of the second block (i.e., above the minimum load)         GW
:math:`ur_{ng}^ω, dr_{ng}^ω`       Upward and downward operating reserves of a committed unit                  GW
:math:`i_{ne}^ω`                   ESS stored energy (inventory)                                               GWh
:math:`s_{ne}^ω`                   ESS spilled energy                                                          GWh
:math:`uc_{nt}, su_{nt}, sd_{nt}`  Commitment, startup and shutdown of generation unit per load level          {0,1}
=================================  ==========================================================================  =====

Equations
---------

**Objective function**: minimization of operation cost for the scope of the model

Generation operation cost [M€] («``eTotalTCost``», ``eTotalVCost``», ``eTotalECost``»)

:math:`\sum_{ωn}{P^ω DUR_n (\sum_g {CV_g gp_{ng}^ω} + CENS ens_n^ω)} + \sum_{ng}{(DUR_n CF_g uc_{ng} + CSU_g su_{ng} + CSD_g sd_{ng})}`

**Constraints**

Balance of generation and demand [GW] («``eBalance``»)

:math:`\sum_{g} gp_{ng}^ω - \sum_{g} gc_{ng}^ω + ens_n^ω = D_n^ω \quad \forall ωn`

Upward and downward operating reserves [GW] («``eOperReserveUp``», ``eOperReserveDw``»)

:math:`\sum_g ur_{ng}^ω \geq UR_n^ω \quad \forall ωn`

:math:`\sum_g dr_{ng}^ω \geq DR_n^ω \quad \forall ωn`

VRES units (i.e., those with linear variable cost equal to 0 and no storage capacity) do not contribute to the operating reserves.

ESS energy inventory (only for load levels multiple of 24, 168, or 672 h, depending on the ESS type) [GWh] («``eESSInventory``»)

:math:`i_{n-\tau_e,e}^ω + \sum_{n' = n+\nu-\tau_e}^n DUR_n (EI_{ne}^ω - qp_{ne}^ω + EF_e gc_{ne}^ω) = i_{ne}^ω + s_{ne}^ω \quad \forall ωne`

Maximum and minimum output of the second block of a committed unit (all except the VRES units) [p.u.] («``eMaxOutput2ndBlock``», ``eMinOutput2ndBlock``»)

* D.A. Tejada-Arango, S. Lumbreras, P. Sánchez-Martín, and A. Ramos "Which Unit-Commitment Formulation is Best? A Systematic Comparison" IEEE Transactions on Power Systems 35 (4):2926-2936 Jul 2020 `10.1109/TPWRS.2019.2962024 <https://doi.org/10.1109/TPWRS.2019.2962024>`_

* C. Gentile, G. Morales-España, and A. Ramos "A tight MIP formulation of the unit commitment problem with start-up and shut-down constraints" EURO Journal on Computational Optimization 5 (1), 177-201 Mar 2017. `10.1007/s13675-016-0066-y <http://dx.doi.org/10.1007/s13675-016-0066-y>`_

* G. Morales-España, A. Ramos, and J. Garcia-Gonzalez "An MIP Formulation for Joint Market-Clearing of Energy and Reserves Based on Ramp Scheduling" IEEE Transactions on Power Systems 29 (1): 476-488, Jan 2014. `10.1109/TPWRS.2013.2259601 <http://dx.doi.org/10.1109/TPWRS.2013.2259601>`_

* G. Morales-España, J.M. Latorre, and A. Ramos "Tight and Compact MILP Formulation for the Thermal Unit Commitment Problem" IEEE Transactions on Power Systems 28 (4): 4897-4908, Nov 2013. `10.1109/TPWRS.2013.2251373 <http://dx.doi.org/10.1109/TPWRS.2013.2251373>`_

:math:`\frac{p_{ng}^ω + ur_{ng}^ω}{\overline{GP}_g - \underline{GP}_g} \leq uc_{ng} \quad \forall ωng`

:math:`\frac{p_{ng}^ω - dr_{ng}^ω}{\overline{GP}_g - \underline{GP}_g} \geq 0       \quad \forall ωng`

Total output of a committed unit (all except the VRES units) [GW] («``eTotalOutput``»)

:math:`\frac{qp_{ng}^ω}{\underline{GP}_g} = uc_{ng} + \frac{p_{ng}^ω}{\underline{GP}_g} \quad \forall ωng`

Logical relation between commitment, startup, and shutdown status of a committed unit (all except the VRE units) [p.u.] («``eUCStrShut``»)

:math:`uc_{ng} - uc_{n-\nu,g} = su_{ng} - sd_{ng} \quad \forall ng`

Initial commitment of the units is determined by the model based on the merit order loading, including the VRES and ESS units.

Maximum ramp up and ramp down for the second block of a thermal unit [p.u.] («``eRampUp``», ``eRampDw``»)

- P. Damcı-Kurt, S. Küçükyavuz, D. Rajan, and A. Atamtürk, “A polyhedral study of production ramping,” Math. Program., vol. 158, no. 1–2, pp. 175–205, Jul. 2016. `10.1007/s10107-015-0919-9 <https://doi.org/10.1007/s10107-015-0919-9>`_

:math:`\frac{p_{nt}^ω - p_{n-\nu,t}^ω + ur_{nt}^ω}{DUR_n RU_t} \leq   uc_{nt}      - su_{nt} \quad \forall ωnt`

:math:`\frac{p_{nt}^ω - p_{n-\nu,t}^ω - dr_{nt}^ω}{DUR_n RD_t} \geq - uc_{n-\nu,t} + sd_{nt} \quad \forall ωnt`

Minimum up time and down time of thermal unit [h] («``eMinUpTime``», ``eMinDownTime``»)

- D. Rajan and S. Takriti, “Minimum up/down polytopes of the unit commitment problem with start-up costs,” IBM, New York, Technical Report RC23628, 2005. https://pdfs.semanticscholar.org/b886/42e36b414d5929fed48593d0ac46ae3e2070.pdf

:math:`\sum_{n'=n+\nu-TU_t}^n su_{n't} \leq     uc_{nt} \quad \forall nt`

:math:`\sum_{n'=n+\nu-TD_t}^n sd_{n't} \leq 1 - uc_{nt} \quad \forall nt`

Bounds on generation variables [GW]

:math:`0 \leq qp_{ng}^ω \leq \overline{GP}_g                    \quad \forall ωng`

:math:`0 \leq qc_{ne}^ω \leq \overline{GC}_e                    \quad \forall ωne`

:math:`0 \leq ur_{ng}^ω \leq \overline{CP}_g - \underline{GP}_g \quad \forall ωng`

:math:`0 \leq dr_{ng}^ω \leq \overline{CP}_g - \underline{GP}_g \quad \forall ωng`

:math:`0 \leq  p_{ng}^ω \leq \overline{GP}_g - \underline{GP}_g \quad \forall ωng`

:math:`0 \leq i_{ne}^ω \leq I_e \quad \forall ωpe`

:math:`0 \leq s_{ne}^ω          \quad \forall ωne`

:math:`0 \leq ens_n^ω \leq D_n^ω \quad \forall ωn`
