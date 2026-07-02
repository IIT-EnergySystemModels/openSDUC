% openSDUC documentation master file, created by Andres Ramos

# Output Results

Some figures for technology output, RES curtailment, and SRMC are plotted.

```{image} /../img/oUC_SRMC_16g.png
:align: center
:scale: 60%
```

```{image} /../img/oUC_TechnologyOutput_scen1_16g.png
:align: center
:scale: 60%
```

The CSV files used for outputting the results are briefly described in the following items.

File `oUC_Result_GenerationCommitment.csv`

```{eval-rst}
==========  ==========  =============  ===================================
Identifier              Header         Description
======================  =============  ===================================
Scenario    Load level  Generator      Commitment decision [p.u.]
==========  ==========  =============  ===================================
```

File `oUC_Result_GenerationStartUp.csv`

```{eval-rst}
==========  ==========  =============  ===================================
Identifier              Header         Description
======================  =============  ===================================
Scenario    Load level  Generator      Startup decision [p.u.]
==========  ==========  =============  ===================================
```

File `oUC_Result_GenerationShutDown.csv`

```{eval-rst}
==========  ==========  =============  ===================================
Identifier              Header         Description
======================  =============  ===================================
Scenario    Load level  Generator      Shutdown decision [p.u.]
==========  ==========  =============  ===================================
```

File `oUC_Result_GenerationReserveUp.csv`

```{eval-rst}
==========  ==========  =============  ===================================
Identifier              Header         Description
======================  =============  ===================================
Scenario    Load level  Generator      Upward operating reserve [MW]
==========  ==========  =============  ===================================
```

File `oUC_Result_GenerationReserveDown.csv`

```{eval-rst}
==========  ==========  =============  ===================================
Identifier              Header         Description
======================  =============  ===================================
Scenario    Load level  Generator      Downward operating reserve [MW]
==========  ==========  =============  ===================================
```

File `oUC_Result_Generation.csv`

```{eval-rst}
==========  ==========  =============  ===================================
Identifier              Header         Description
======================  =============  ===================================
Scenario    Load level  Generator      Output (discharge in ESS) [MW]
==========  ==========  =============  ===================================
```

File `oUC_Result_Consumption.csv`

```{eval-rst}
==========  ==========  =============  ===================================
Identifier              Header         Description
======================  =============  ===================================
Scenario    Load level  Generator      Charged power in ESS [MW]
==========  ==========  =============  ===================================
```

File `oUC_Result_GenerationEnergy.csv`

```{eval-rst}
==========  ==========  =============  ===================================
Identifier              Header         Description
======================  =============  ===================================
Scenario    Load level  Generator      Energy (discharge in ESS) [GWh]
==========  ==========  =============  ===================================
```

File `oUC_Result_ConsumptionEnergy.csv`

```{eval-rst}
==========  ==========  =============  ===================================
Identifier              Header         Description
======================  =============  ===================================
Scenario    Load level  Generator      Charged energy in ESS [GWh]
==========  ==========  =============  ===================================
```

File `oUC_Result_GenerationCurtailment.csv`

```{eval-rst}
==========  ==========  =============  ===================================
Identifier              Header         Description
======================  =============  ===================================
Scenario    Load level  RES Generator  Curtailed power of RES [MW]
==========  ==========  =============  ===================================
```

File `oUC_Result_GenerationEmission.csv`

```{eval-rst}
==========  ==========  =============  ===================================
Identifier              Header         Description
======================  =============  ===================================
Scenario    Load level  Generator      CO2 emission [tCO2]
==========  ==========  =============  ===================================
```

File `oUC_Result_TechnologyGeneration.csv`

```{eval-rst}
==========  ==========  =============  ===================================
Identifier              Header         Description
======================  =============  ===================================
Scenario    Load level  Technology     Output (discharge in ESS) [MW]
==========  ==========  =============  ===================================
```

File `oUC_Result_TechnologyConsumption.csv`

```{eval-rst}
==========  ==========  =============  ===================================
Identifier              Header         Description
======================  =============  ===================================
Scenario    Load level  Technology     Consumption (charge in ESS) [MW]
==========  ==========  =============  ===================================
```

File `oUC_Result_TechnologyGenerationEnergy.csv`

```{eval-rst}
==========  ==========  =============  ===================================
Identifier              Header         Description
======================  =============  ===================================
Scenario    Load level  Technology     Generation (discharge in ESS) [GWh]
==========  ==========  =============  ===================================
```

File `oUC_Result_TechnologyConsumptionEnergy.csv`

```{eval-rst}
==========  ==========  =============  ===================================
Identifier              Header         Description
======================  =============  ===================================
Scenario    Load level  Technology     Consumption (charge in ESS) [GWh]
==========  ==========  =============  ===================================
```

File `oUC_Result_ESSInventory.csv`

```{eval-rst}
==========  ==========  =============  =============================================================================================
Identifier              Header         Description
======================  =============  =============================================================================================
Scenario    Load level  Generator      Stored energy (SoC in batteries, reservoir energy in pumped-storage hydro power plants) [GWh]
==========  ==========  =============  =============================================================================================
```

File `oUC_Result_ESSSpillage.csv`

```{eval-rst}
==========  ==========  =============  ===================================
Identifier              Header         Description
======================  =============  ===================================
Scenario    Load level  Generator      Spilled energy in ESS [GWh]
==========  ==========  =============  ===================================
```

File `oUC_Result_PNS.csv`

```{eval-rst}
==========  ==========  ===============================
Identifier              Description
======================  ===============================
Scenario    Load level  Power not served [MW]
==========  ==========  ===============================
```

File `oUC_Result_ENS.csv`

```{eval-rst}
==========  ==========  ===============================
Identifier              Description
======================  ===============================
Scenario    Load level  Energy not served [GWh]
==========  ==========  ===============================
```

File `oUC_Result_SRMC.csv`

```{eval-rst}
==========  ==========  ===============================
Identifier              Description
======================  ===============================
Scenario    Load level  Short-Run Marginal Cost [€/MWh]
==========  ==========  ===============================
```
