.. openSDUC documentation master file, created by Andres Ramos

Output Results
==============

Some figures for technology output, RES curtailment and SRMC are plotted.

.. image:: /../img/oUC_SRMC_16g.png
   :scale: 60%
   :align: center

.. image:: /../img/oUC_TechnologyOutput_scen1_16g.png
   :scale: 60%
   :align: center

Besides, the csv files used for outputting the results are briefly described in the following items.

File ``oUC_Result_GenerationCommitment.csv``

============  ==========  =========  ===========================
Identifier    Identifier  Header     Description
============  ==========  =========  ===========================
Scenario      Load level  Generator  Commitment decision [p.u.]
============  ==========  =========  ===========================

File ``oUC_Result_GenerationStartUp.csv``

============  ==========  =========  ===========================
Identifier    Identifier  Header     Description
============  ==========  =========  ===========================
Scenario      Load level  Generator  Startup decision [p.u.]
============  ==========  =========  ===========================

File ``oUC_Result_GenerationShutDown.csv``

============  ==========  =========  ===========================
Identifier    Identifier  Header     Description
============  ==========  =========  ===========================
Scenario      Load level  Generator  Shutdown decision [p.u.]
============  ==========  =========  ===========================

File ``oUC_Result_GenerationReserveUp.csv``

============  ==========  =========  ==============================
Identifier    Identifier  Header     Description
============  ==========  =========  ==============================
Scenario      Load level  Generator  Upward operating reserve [MW]
============  ==========  =========  ==============================

File ``oUC_Result_GenerationReserveDown.csv``

============  ==========  =========  ===============================
Identifier    Identifier  Header     Description
============  ==========  =========  ===============================
Scenario      Load level  Generator  Downward operating reserve [MW]
============  ==========  =========  ===============================

File ``oUC_Result_Generation.csv``

============  ==========  =========  ==============================
Identifier    Identifier  Header     Description
============  ==========  =========  ==============================
Scenario      Load level  Generator  Output (discharge in ESS) [MW]
============  ==========  =========  ==============================

File ``oUC_Result_Consumption.csv``

============  ==========  =========  ===========================
Identifier    Identifier  Header     Description
============  ==========  =========  ===========================
Scenario      Load level  Generator  Charged power in ESS [MW]
============  ==========  =========  ===========================

File ``oUC_Result_GenerationEnergy.csv``

============  ==========  =========  ===============================
Identifier    Identifier  Header     Description
============  ==========  =========  ===============================
Scenario      Load level  Generator  Energy (discharge in ESS) [GWh]
============  ==========  =========  ===============================

File ``oUC_Result_ConsumptionEnergy.csv``

============  ==========  =========  ===========================
Identifier    Identifier  Header     Description
============  ==========  =========  ===========================
Scenario      Load level  Generator  Charged energy in ESS [GWh]
============  ==========  =========  ===========================

File ``oUC_Result_GenerationCurtailment.csv``

============  ==========  =============  ===========================
Identifier    Identifier  Header         Description
============  ==========  =============  ===========================
Scenario      Load level  RES Generator  Curtailed power of RES [MW]
============  ==========  =============  ===========================

File ``oUC_Result_GenerationEmission.csv``

============  ==========  =========  ===============================
Identifier    Identifier  Header     Description
============  ==========  =========  ===============================
Scenario      Load level  Generator  CO2 emission [tCO2]
============  ==========  =========  ===============================

File ``oUC_Result_TechnologyGeneration.csv``

============  ==========  ==========  ==============================
Identifier    Identifier  Header      Description
============  ==========  ==========  ==============================
Scenario      Load level  Technology  Output (discharge in ESS) [MW]
============  ==========  ==========  ==============================

File ``oUC_Result_TechnologyConsumption.csv``

============  ==========  ==========  ==================================
Identifier    Identifier  Header      Description
============  ==========  ==========  ==================================
Scenario      Load level  Technology  Consumption (charge in ESS) [GWh]
============  ==========  ==========  ==================================

File ``oUC_Result_TechnologyGenerationEnergy.csv``

============  ==========  ==========  ====================================
Identifier    Identifier  Header      Description
============  ==========  ==========  ====================================
Scenario      Load level  Technology  Generation (discharge in ESS) [GWh]
============  ==========  ==========  ====================================

File ``oUC_Result_TechnologyConsumptionEnergy.csv``

============  ==========  ==========  =================================
Identifier    Identifier  Header      Description
============  ==========  ==========  =================================
Scenario      Load level  Technology  Consumption (charge in ESS) [GWh]
============  ==========  ==========  =================================

File ``oUC_Result_ESSInventory.csv``

============  ==========  =========  ==============================================================================================
Identifier    Identifier  Header     Description
============  ==========  =========  ==============================================================================================
Scenario      Load level  Generator  Stored energy (SoC in batteries, reservoir energy in pumped-storage hydro power plants) [GWh]
============  ==========  =========  ==============================================================================================

File ``oUC_Result_ESSSpillage.csv``

============  ==========  =========  =============================
Identifier    Identifier  Header     Description
============  ==========  =========  =============================
Scenario      Load level  Generator  Spilled energy in ESS [GWh]
============  ==========  =========  =============================

File ``oUC_Result_PNS.csv``

============  ==========  =======================
Identifier    Identifier  Description
============  ==========  =======================
Scenario      Load level  Power not served [MW]
============  ==========  =======================

File ``oUC_Result_ENS.csv``

============  ==========  =======================
Identifier    Identifier  Description
============  ==========  =======================
Scenario      Load level  Energy not served [GWh]
============  ==========  =======================

File ``oUC_Result_SRMC.csv``

============  ==========  ====================================
Identifier    Identifier  Description
============  ==========  ====================================
Scenario      Load level  Short-Mun Marginal Cost [€/MWh]
============  ==========  ====================================
