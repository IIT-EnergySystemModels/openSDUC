.. openSDUC documentation master file, created by Andres Ramos

Input Data
==========

All the input files must be in the same folder of the openSDUC python file.

Dictionaries. Sets
------------------
The dictionaries include all the possible elements of the corresponding sets included in the optimization problem

==========================  ========================================================================================================================
File                        Description
==========================  ========================================================================================================================
``oT_Dict_Scenario.csv``    Scenario. Short-term uncertainties (scenarios) (e.g., s001 to s100)
``oT_Dict_LoadLevel.csv``   Load level (e.g., 2020-01-01T00:00:00+01:00 to 2020-01-07T23:00:00+01:00). Load levels with duration 0 are ignored
``oT_Dict_Generation.csv``  Generation units (thermal, ESS and variable)
``oT_Dict_Technology.csv``  Generation technologies
``oT_Dict_Company.csv``     Companies
``oT_Dict_Storage.csv``     ESS type (daily, weekly, monthly)
==========================  ========================================================================================================================

Input files
-----------
This is the list of the input data files and their brief description.

======================================  ==========================================================================================================
File                                    Description
======================================  ==========================================================================================================
``oT_Data_Parameter.csv``               General system parameters
``oT_Data_Duration.csv``                Duration of the load levels
``oT_Data_Scenario.csv``                Short-term uncertainties
``oT_Data_Demand.csv``                  Demand
``oT_Data_OperatingReserve.csv``        Upward and downward operating reserves (include aFRR, mFRR and RR for electricity balancing from ENTSO-E)
``oT_Data_Generation.csv``              Generation data
``oT_Data_EnergyInflows.csv``           Energy inflows for ESS (e.g., storage hydro or open-loop pumped-storage hydro) by load level
``oT_Data_MinimumGeneration.csv``       Variable minimum power generation by load level
``oT_Data_MaximumGeneration.csv``       Variable minimum power generation by load level
``oT_Data_MaximumStorage.csv``          Variable maximum storage by load level
``oT_Data_MinimumStorage.csv``          Variable minimum storage by load level
======================================  ==========================================================================================================

Parameters
----------
A description of the system parameters included in the file ``oT_Data_Parameter.csv`` follows:

================  =======================================================================================  ================
File              Description                                                                              
================  =======================================================================================  ================
ENSCost           Cost of energy not served. Cost of load curtailment. Value of Lost Load (VoLL)           €/MWh   
CO2Cost           Cost of CO2 emissions                                                                    €/tCO2
TimeStep          Duration of the time step for the load levels (hourly, bi-hourly, trihourly, etc.).      h
================  =======================================================================================  ================

A time step greater than one hour it is a convenient way to reduce the load levels of the time scope. The moving average of the demand, operating reserve, variable generation and ESS energy inflows over
the time step load levels is assigned to active load levels (e.g., the mean value of the three hours is associated to the third hour in a trihourly time step).

Duration
--------

A description of the data included in the file ``oT_Data_Duration.csv`` follows:

==========  ========  ===================================================================  ==
Identifier  Header    Description
==========  ========  ===================================================================  ==
Load level  Duration  Duration of the load level. Load levels with duration 0 are ignored  h
==========  ========  ===================================================================  ==

It is a simple way to use isolated snapshots or representative days or just the first three months instead of all the hours of a year to simplify the optimization problem.

Scenario
--------

A description of the data included in the file ``oT_Data_Scenario.csv`` follows:

==============  ============  ===========================  ====
Identifier      Header        Description
==============  ============  ===========================  ====
Scenario        Probability   Probability of the scenario  p.u.
==============  ============  ===========================  ====

Demand
------

A description of the data included in the file ``oT_Data_Demand.csv`` follows:

==============  ==========  ===============================  ==
Identifier      Identifier  Description
==============  ==========  ===============================  ==
Scenario        Load level  Power demand in the load level   MW
==============  ==========  ===============================  ==

Internally, all the values below 1e-5 times the maximum system demand will be converted into 0 by the model.

Operating reserves
------------------

A description of the data included in the file ``oT_Data_OperatingReserve.csv`` follows:

==============  ==========  ======  =============================================  ==
Identifier      Identifier  Header  Description
==============  ==========  ======  =============================================  ==
Scenario        Load level  Up      Upward   operating reserves in the load level  MW
Scenario        Load level  Down    Downward operating reserves in the load level  MW
==============  ==========  ======  =============================================  ==

These operating reserves must include Automatic Frequency Restoration Reserves (aFRR), Manual Frequency Restoration Reserves (mFRR) and Replacement Reserves (RR) for electricity balancing from ENTSO-E.
Internally, all the values below 1e-5 times the maximum system demand will be converted into 0 by the model.

Generation
----------
A description of the data included for each generating unit in the file ``oT_Data_Generation.csv`` follows:

====================  ===================================================================  ============================
Header                Description   
====================  ===================================================================  ============================  
Technology            Technology of the generator (nuclear, coal, CCGT, OCGT, ESS, etc.)   
Company               Name of the company owning the generator  
StorageType           Storage type (daily, weekly, monthly, etc.)                          Daily/Weekly/Monthly
MaximumPower          Maximum power output (discharge for ESS units)                       MW
MinimumPower          Minimum power output                                                 MW
MaximumCharge         Maximum charge when storing energy the ESS unit                      MW
InitialStorage        Initial energy stored at the first instant of the time scope         GWh
MaximumStorage        Maximum energy that can be stored by the ESS unit                    GWh
MinimumStorage        Minimum energy that can be stored by the ESS unit                    GWh
Efficiency            Round-trip efficiency in the charge/discharge cycle                  p.u.
RampUp                Ramp up   rate                                                       MW/h
RampDown              Ramp down rate                                                       MW/h
UpTime                Minimum uptime                                                       h
DownTime              Minimum downtime                                                     h
FuelCost              Fuel cost                                                            €/Mcal
LinearTerm            Linear term (slope) of the heat rate straight line                   Mcal/MWh
ConstantTerm          Constant term (intercept) of the heat rate straight line             Mcal/h
OMVariableCost        O&M variable cost                                                    €/MWh
StartUpCost           Startup  cost                                                        M€
ShutDownCost          Shutdown cost                                                        M€
CO2EmissionRate       CO2 emission rate                                                    tCO2/MWh
====================  ===================================================================  ============================  

A generator with linear variable cost > 0 is considered a thermal unit. If its maximum storage > 0 is considered an ESS.
Internally, all the maximum and minimum power values below 1e-5 times the maximum system demand will be converted into 0 by the model.

The startup cost of a generating unit refers to the expenses incurred when bringing a power generation unit online, from an idle state to a point where it can produce electricity.

Energy inflows
--------------

A description of the data included in the file ``oT_Data_EnergyInflows.csv`` follows:

==============  ==========  =========  =============================  ==
Identifier      Identifier  Header     Description
==============  ==========  =========  =============================  ==
Scenario        Load level  Generator  Energy inflows by load level   MW
==============  ==========  =========  =============================  ==

Internally, all the values below 1e-5 times the maximum system demand will be converted into 0 by the model.

Variable maximum and minimum generation
---------------------------------------

A description of the data included in the file ``oT_Data_MaximumGeneration.csv`` and ``oT_Data_MinimumGeneration.csv`` follows:

==============  ==========  =========  =============================================================  ==
Identifier      Identifier  Header     Description
==============  ==========  =========  =============================================================  ==
Scenario        Load level  Generator  Maximum (minimum) power generation of the unit by load level   MW
==============  ==========  =========  =============================================================  ==

To force a generator to produce 0 a lower value (e.g., 0.1 MW) strictly > 0, but not 0 (in which case the value will be ignored), must be introduced. Internally, all the values below 1e-5 times the maximum system demand will be converted into 0 by the model.
Columns of this file (names of the generators) must be in the same order that in the generation dictionary.

Variable maximum and minimum storage
---------------------------------------------

A description of the data included in the files ``oT_Data_MaximumStorage.csv`` and ``oT_Data_MinimumStorage.csv`` follows:

==============  ==========  =========  ====================================================  ===
Identifier      Identifier  Header     Description
==============  ==========  =========  ====================================================  ===
Scenario        Load level  Generator  Maximum (minimum) storage of the ESS by load level    GWh
==============  ==========  =========  ====================================================  ===

All the generators must be defined as columns of these files.
Internally, all the values below 1e-5 times the maximum system demand will be converted into 0 by the model.
