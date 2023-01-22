#                     GNU GENERAL PUBLIC LICENSE
#                        Version 3, 29 June 2007
#
#  Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
#  Everyone is permitted to copy and distribute verbatim copies
#  of this license document, but changing it is not allowed.
#
#                             Preamble
#
#   The GNU General Public License is a free, copyleft license for
# software and other kinds of works.
#
#   The licenses for most software and other practical works are designed
# to take away your freedom to share and change the works.  By contrast,
# the GNU General Public License is intended to guarantee your freedom to
# share and change all versions of a program--to make sure it remains free
# software for all its users.  We, the Free Software Foundation, use the
# GNU General Public License for most of our software; it applies also to
# any other work released this way by its authors.  You can apply it to
# your programs, too.
#
#   When we speak of free software, we are referring to freedom, not
# price.  Our General Public Licenses are designed to make sure that you
# have the freedom to distribute copies of free software (and charge for
# them if you wish), that you receive source code or can get it if you
# want it, that you can change the software or use pieces of it in new
# free programs, and that you know you can do these things.
#
#   To protect your rights, we need to prevent others from denying you
# these rights or asking you to surrender the rights.  Therefore, you have
# certain responsibilities if you distribute copies of the software, or if
# you modify it: responsibilities to respect the freedom of others.
#
#   For example, if you distribute copies of such a program, whether
# gratis or for a fee, you must pass on to the recipients the same
# freedoms that you received.  You must make sure that they, too, receive
# or can get the source code.  And you must show them these terms so they
# know their rights.
#
#   Developers that use the GNU GPL protect your rights with two steps:
# (1) assert copyright on the software, and (2) offer you this License
# giving you legal permission to copy, distribute and/or modify it.
#
#   For the developers' and authors' protection, the GPL clearly explains
# that there is no warranty for this free software.  For both users' and
# authors' sake, the GPL requires that modified versions be marked as
# changed, so that their problems will not be attributed erroneously to
# authors of previous versions.
#
#   Some devices are designed to deny users access to install or run
# modified versions of the software inside them, although the manufacturer
# can do so.  This is fundamentally incompatible with the aim of
# protecting users' freedom to change the software.  The systematic
# pattern of such abuse occurs in the area of products for individuals to
# use, which is precisely where it is most unacceptable.  Therefore, we
# have designed this version of the GPL to prohibit the practice for those
# products.  If such problems arise substantially in other domains, we
# stand ready to extend this provision to those domains in future versions
# of the GPL, as needed to protect the freedom of users.
#
#   Finally, every program is threatened constantly by software patents.
# States should not allow patents to restrict development and use of
# software on general-purpose computers, but in those that do, we wish to
# avoid the special danger that patents applied to a free program could
# make it effectively proprietary.  To prevent this, the GPL assures that
# patents cannot be used to render the program non-free.

# Open Stochastic Daily Unit Commitment of Thermal and ESS Units (openSDUC) - Version 1.3.29 - January 22, 2023
# simplicity and transparency in power systems planning

# Developed by

#    Andres Ramos
#    Instituto de Investigacion Tecnologica
#    Escuela Tecnica Superior de Ingenieria - ICAI
#    UNIVERSIDAD PONTIFICIA COMILLAS
#    Alberto Aguilera 23
#    28015 Madrid, Spain
#    Andres.Ramos@comillas.edu
#    https://pascua.iit.comillas.edu/aramos/Ramos_CV.htm

#    with the very valuable collaboration from David Dominguez (david.dominguez@comillas.edu) and Alejandro Rodriguez (argallego@comillas.edu), our local Python gurus

#%% Libraries
import argparse
import os
import pandas        as pd
import time          # count clock time
import psutil        # access the number of CPUs
import pyomo.environ as pyo
from   pyomo.environ import Set, Var, Binary, NonNegativeReals, RealSet, Constraint, ConcreteModel, Objective, minimize, Suffix, DataPortal
from   pyomo.opt     import SolverFactory

import matplotlib.pyplot as plt

print('\n #### Academic research license - for non-commercial use only #### \n')

StartTime = time.time()

parser = argparse.ArgumentParser(description='Introducing main parameters...')
parser.add_argument('--case',   type=str, default=None)
parser.add_argument('--dir',    type=str, default=None)
parser.add_argument('--solver', type=str, default=None)

DIR    = os.path.dirname(__file__)
CASE   = '16g'
SOLVER = 'gurobi'

def main():
    args = parser.parse_args()
    if args.dir is None:
        args.dir    = input('Input Dir    Name (Default {}): '.format(DIR))
        if args.dir == '':
            args.dir = DIR
    if args.case is None:
        args.case   = input('Input Case   Name (Default {}): '.format(CASE))
        if args.case == '':
            args.case = CASE
    if args.solver is None:
        args.solver = input('Input Solver Name (Default {}): '.format(SOLVER))
        if args.solver == '':
            args.solver = SOLVER
    print(args.case)
    print(args.dir)
    print(args.solver)
    import sys
    print(sys.argv)
    print(args)
    openSDUC_run(args.dir, args.case, args.solver)

def openSDUC_run(DirName, CaseName, SolverName):

    _path = os.path.join(DirName, CaseName)
    StartTime = time.time()

    #%% model declaration
    mSDUC = ConcreteModel('Open Stochastic Daily Unit Commitment of Thermal and ESS Units (openSDUC) - Version 1.3.29 - January 22, 2023')

    #%% reading the sets
    dictSets = DataPortal()
    dictSets.load(filename=_path+'/oUC_Dict_Scenario_'  +CaseName+'.csv', set='sc', format='set')
    dictSets.load(filename=_path+'/oUC_Dict_LoadLevel_' +CaseName+'.csv', set='n' , format='set')
    dictSets.load(filename=_path+'/oUC_Dict_Generation_'+CaseName+'.csv', set='g' , format='set')
    dictSets.load(filename=_path+'/oUC_Dict_Storage_'   +CaseName+'.csv', set='st', format='set')
    dictSets.load(filename=_path+'/oUC_Dict_Technology_'+CaseName+'.csv', set='gt', format='set')
    dictSets.load(filename=_path+'/oUC_Dict_Company_'   +CaseName+'.csv', set='co', format='set')

    mSDUC.sc = Set(initialize=dictSets['sc'], ordered=True,  doc='scenarios'   )
    mSDUC.nn = Set(initialize=dictSets['n' ], ordered=True,  doc='load levels' )
    mSDUC.gg = Set(initialize=dictSets['g' ], ordered=False, doc='units'       )
    mSDUC.gt = Set(initialize=dictSets['gt'], ordered=False, doc='technologies')
    mSDUC.co = Set(initialize=dictSets['co'], ordered=False, doc='companies'   )
    mSDUC.st = Set(initialize=dictSets['st'], ordered=False, doc='ESS types'   )

    #%% reading data from CSV files
    dfParameter          = pd.read_csv(_path+'/oUC_Data_Parameter_'        +CaseName+'.csv', index_col=[0  ])
    dfDuration           = pd.read_csv(_path+'/oUC_Data_Duration_'         +CaseName+'.csv', index_col=[0  ])
    dfScenario           = pd.read_csv(_path+'/oUC_Data_Scenario_'         +CaseName+'.csv', index_col=[0  ])
    dfDemand             = pd.read_csv(_path+'/oUC_Data_Demand_'           +CaseName+'.csv', index_col=[0,1])
    dfOperatingReserve   = pd.read_csv(_path+'/oUC_Data_OperatingReserve_' +CaseName+'.csv', index_col=[0,1])
    dfGeneration         = pd.read_csv(_path+'/oUC_Data_Generation_'       +CaseName+'.csv', index_col=[0  ])
    dfVariableMinPower   = pd.read_csv(_path+'/oUC_Data_MinimumGeneration_'+CaseName+'.csv', index_col=[0,1])
    dfVariableMaxPower   = pd.read_csv(_path+'/oUC_Data_MaximumGeneration_'+CaseName+'.csv', index_col=[0,1])
    dfVariableMinStorage = pd.read_csv(_path+'/oUC_Data_MinimumStorage_'   +CaseName+'.csv', index_col=[0,1])
    dfVariableMaxStorage = pd.read_csv(_path+'/oUC_Data_MaximumStorage_'   +CaseName+'.csv', index_col=[0,1])
    dfEnergyInflows      = pd.read_csv(_path+'/oUC_Data_EnergyInflows_'    +CaseName+'.csv', index_col=[0,1])

    # substitute NaN by 0
    dfParameter.fillna         (0.0, inplace=True)
    dfDuration.fillna          (0.0, inplace=True)
    dfScenario.fillna          (0.0, inplace=True)
    dfDemand.fillna            (0.0, inplace=True)
    dfOperatingReserve.fillna  (0.0, inplace=True)
    dfGeneration.fillna        (0.0, inplace=True)
    dfVariableMinPower.fillna  (0.0, inplace=True)
    dfVariableMaxPower.fillna  (0.0, inplace=True)
    dfVariableMinStorage.fillna(0.0, inplace=True)
    dfVariableMaxStorage.fillna(0.0, inplace=True)
    dfEnergyInflows.fillna     (0.0, inplace=True)

    #%% general parameters
    pENSCost            = dfParameter['ENSCost' ][0] * 1e-3                                                                        # cost of energy not served        [MEUR/GWh]
    pCO2Cost            = dfParameter['CO2Cost' ][0]                                                                               # cost of CO2 emission             [EUR/CO2 ton]
    pTimeStep           = dfParameter['TimeStep'][0].astype('int')                                                                 # duration of the unit time step   [h]

    pDuration           = dfDuration          ['Duration'    ] * pTimeStep                                                         # duration of load levels          [h]
    pScenProb           = dfScenario          ['Probability' ]                                                                     # probabilities of scenarios       [p.u.]
    pDemand             = dfDemand            ['Demand'      ] * 1e-3                                                              # demand                           [GW]
    pOperReserveUp      = dfOperatingReserve  ['Up'          ] * 1e-3                                                              # operating reserve up             [GW]
    pOperReserveDw      = dfOperatingReserve  ['Down'        ] * 1e-3                                                              # operating reserve down           [GW]
    pVariableMinPower   = dfVariableMinPower  [list(mSDUC.gg)] * 1e-3                                                              # dynamic variable minimum power   [GW]
    pVariableMaxPower   = dfVariableMaxPower  [list(mSDUC.gg)] * 1e-3                                                              # dynamic variable maximum power   [GW]
    pVariableMinStorage = dfVariableMinStorage[list(mSDUC.gg)]                                                                     # dynamic variable minimum storage [GWh]
    pVariableMaxStorage = dfVariableMaxStorage[list(mSDUC.gg)]                                                                     # dynamic variable maximum storage [GWh]
    pEnergyInflows      = dfEnergyInflows     [list(mSDUC.gg)] * 1e-3                                                              # dynamic energy inflows           [GW]

    # compute the demand as the mean over the time step load levels and assign it to active load levels. Idem for operating reserve, variable max power, variable min and max storage capacity and inflows
    pDemand             = pDemand.rolling            (pTimeStep).mean()
    pOperReserveUp      = pOperReserveUp.rolling     (pTimeStep).mean()
    pOperReserveDw      = pOperReserveDw.rolling     (pTimeStep).mean()
    pVariableMinPower   = pVariableMinPower.rolling  (pTimeStep).mean()
    pVariableMaxPower   = pVariableMaxPower.rolling  (pTimeStep).mean()
    pVariableMinStorage = pVariableMinStorage.rolling(pTimeStep).mean()
    pVariableMaxStorage = pVariableMaxStorage.rolling(pTimeStep).mean()
    pEnergyInflows      = pEnergyInflows.rolling     (pTimeStep).mean()

    pDemand.fillna            (0.0, inplace=True)
    pOperReserveUp.fillna     (0.0, inplace=True)
    pOperReserveDw.fillna     (0.0, inplace=True)
    pVariableMinPower.fillna  (0.0, inplace=True)
    pVariableMaxPower.fillna  (0.0, inplace=True)
    pVariableMinStorage.fillna(0.0, inplace=True)
    pVariableMaxStorage.fillna(0.0, inplace=True)
    pEnergyInflows.fillna     (0.0, inplace=True)

    if pTimeStep > 1:
        # assign duration 0 to load levels not being considered, active load levels are at the end of every pTimeStep
        for i in range(pTimeStep-2,-1,-1):
            pDuration[range(i,len(mSDUC.nn),pTimeStep)] = 0

    #%% generation parameters
    pGenToTechnology  = dfGeneration['Technology'     ]                                                                            # generator association to technology
    pGenToCompany     = dfGeneration['Company'        ]                                                                            # generator association to company
    pRatedMinPower    = dfGeneration['MinimumPower'   ] * 1e-3                                                                     # rated minimum power                 [GW]
    pRatedMaxPower    = dfGeneration['MaximumPower'   ] * 1e-3                                                                     # rated maximum power                 [GW]
    pLinearVarCost    = dfGeneration['LinearTerm'     ] * 1e-3 * dfGeneration['FuelCost'] + dfGeneration['OMVariableCost'] * 1e-3  # linear   term variable cost         [MEUR/GWh]
    pConstantVarCost  = dfGeneration['ConstantTerm'   ] * 1e-6 * dfGeneration['FuelCost']                                          # constant term variable cost         [MEUR/h]
    pStartUpCost      = dfGeneration['StartUpCost'    ]                                                                            # startup  cost                       [MEUR]
    pShutDownCost     = dfGeneration['ShutDownCost'   ]                                                                            # shutdown cost                       [MEUR]
    pRampUp           = dfGeneration['RampUp'         ] * 1e-3                                                                     # ramp up   rate                      [GW/h]
    pRampDw           = dfGeneration['RampDown'       ] * 1e-3                                                                     # ramp down rate                      [GW/h]
    pCO2EmissionRate  = dfGeneration['CO2EmissionRate'] * 1e-3                                                                     # emission  rate                      [t CO2/MWh]
    pUpTime           = dfGeneration['UpTime'         ]                                                                            # minimum up   time                   [h]
    pDwTime           = dfGeneration['DownTime'       ]                                                                            # minimum down time                   [h]
    pMaxCharge        = dfGeneration['MaximumCharge'  ] * 1e-3                                                                     # maximum ESS charge                  [GW]
    pInitialInventory = dfGeneration['InitialStorage' ]                                                                            # initial ESS storage                 [GWh]
    pRatedMinStorage  = dfGeneration['MinimumStorage' ]                                                                            # minimum ESS storage                 [GWh]
    pRatedMaxStorage  = dfGeneration['MaximumStorage' ]                                                                            # maximum ESS storage                 [GWh]
    pEfficiency       = dfGeneration['Efficiency'     ]                                                                            #         ESS efficiency              [p.u.]
    pStorageType      = dfGeneration['StorageType'    ]                                                                            #         ESS type

    ReadingDataTime = time.time() - StartTime
    StartTime       = time.time()
    print('Reading    input data                 ... ', round(ReadingDataTime), 's')

    #%% defining subsets: active load levels (n), thermal units (t), ESS units (es), all the lines (la), candidate lines (lc) and lines with losses (ll)
    mSDUC.n  = Set(initialize=mSDUC.nn, ordered=True , doc='load levels'     , filter=lambda mSDUC,nn: nn in mSDUC.nn and pDuration     [nn] >  0  )
    mSDUC.n2 = Set(initialize=mSDUC.nn, ordered=True , doc='load levels'     , filter=lambda mSDUC,nn: nn in mSDUC.nn and pDuration     [nn] >  0  )
    mSDUC.g  = Set(initialize=mSDUC.gg, ordered=False, doc='generating units', filter=lambda mSDUC,gg: gg in mSDUC.gg and pRatedMaxPower[gg] >  0.0)
    mSDUC.t  = Set(initialize=mSDUC.g , ordered=False, doc='thermal    units', filter=lambda mSDUC,g : g  in mSDUC.g  and pLinearVarCost [g] >  0.0)
    mSDUC.r  = Set(initialize=mSDUC.g , ordered=False, doc='RES        units', filter=lambda mSDUC,g : g  in mSDUC.g  and pLinearVarCost [g] == 0.0 and pRatedMaxStorage[g] == 0.0)
    mSDUC.es = Set(initialize=mSDUC.g , ordered=False, doc='ESS        units', filter=lambda mSDUC,g : g  in mSDUC.g  and                               pRatedMaxStorage[g] >  0.0)

    # non-RES units
    mSDUC.nr = mSDUC.g - mSDUC.r

    if pTimeStep > 1:
        # drop levels with duration 0
        pDuration           = pDuration.loc          [mSDUC.sc*mSDUC.n]
        pDemand             = pDemand.loc            [mSDUC.sc*mSDUC.n]
        pOperReserveUp      = pOperReserveUp.loc     [mSDUC.sc*mSDUC.n]
        pOperReserveDw      = pOperReserveDw.loc     [mSDUC.sc*mSDUC.n]
        pVariableMinPower   = pVariableMinPower.loc  [mSDUC.sc*mSDUC.n]
        pVariableMaxPower   = pVariableMaxPower.loc  [mSDUC.sc*mSDUC.n]
        pVariableMinStorage = pVariableMinStorage.loc[mSDUC.sc*mSDUC.n]
        pVariableMaxStorage = pVariableMaxStorage.loc[mSDUC.sc*mSDUC.n]
        pEnergyInflows      = pEnergyInflows.loc     [mSDUC.sc*mSDUC.n]

    # variable minimum and maximum power
    pVariableMinPower = pVariableMinPower.replace(0.0, float('nan'))
    pVariableMaxPower = pVariableMaxPower.replace(0.0, float('nan'))
    pMinPower         = pd.DataFrame([pRatedMinPower]*len(pVariableMaxPower.index), index=pd.MultiIndex.from_tuples(pVariableMaxPower.index), columns=pRatedMinPower.index)
    pMaxPower         = pd.DataFrame([pRatedMaxPower]*len(pVariableMaxPower.index), index=pd.MultiIndex.from_tuples(pVariableMaxPower.index), columns=pRatedMaxPower.index)
    pMinPower         = pMinPower.reindex        (sorted(pMinPower.columns        ), axis=1)
    pMaxPower         = pMaxPower.reindex        (sorted(pMaxPower.columns        ), axis=1)
    pVariableMinPower = pVariableMinPower.reindex(sorted(pVariableMinPower.columns), axis=1)
    pVariableMaxPower = pVariableMaxPower.reindex(sorted(pVariableMaxPower.columns), axis=1)
    pMinPower         = pVariableMinPower.where(pVariableMinPower > pMinPower, other=pMaxPower)
    pMaxPower         = pVariableMaxPower.where(pVariableMaxPower < pMaxPower, other=pMaxPower)
    pMaxPower2ndBlock = pMaxPower - pMinPower

    # variable minimum and maximum storage capacity
    pVariableMinStorage = pVariableMinStorage.replace(0.0, float('nan'))
    pVariableMaxStorage = pVariableMaxStorage.replace(0.0, float('nan'))
    pMinStorage         = pd.DataFrame([pRatedMinStorage]*len(pVariableMinStorage.index), index=pd.MultiIndex.from_tuples(pVariableMinStorage.index), columns=pRatedMinStorage.index)
    pMaxStorage         = pd.DataFrame([pRatedMaxStorage]*len(pVariableMaxStorage.index), index=pd.MultiIndex.from_tuples(pVariableMaxStorage.index), columns=pRatedMaxStorage.index)
    pMinStorage         = pMinStorage.reindex        (sorted(pMinStorage.columns        ), axis=1)
    pMaxStorage         = pMaxStorage.reindex        (sorted(pMaxStorage.columns        ), axis=1)
    pVariableMinStorage = pVariableMinStorage.reindex(sorted(pVariableMinStorage.columns), axis=1)
    pVariableMaxStorage = pVariableMaxStorage.reindex(sorted(pVariableMaxStorage.columns), axis=1)
    pMinStorage         = pVariableMinStorage.where(pVariableMinStorage > pMinStorage, other=pMinStorage)
    pMaxStorage         = pVariableMaxStorage.where(pVariableMaxStorage < pMaxStorage, other=pMaxStorage)

    # values < 1e-5 times the maximum system demand are converted to 0
    pEpsilon = pDemand.max()*1e-5
    # these parameters are in GW
    pDemand          [pDemand           < pEpsilon] = 0.0
    pOperReserveUp   [pOperReserveUp    < pEpsilon] = 0.0
    pOperReserveDw   [pOperReserveDw    < pEpsilon] = 0.0
    pMinPower        [pMinPower         < pEpsilon] = 0.0
    pMaxPower        [pMaxPower         < pEpsilon] = 0.0
    pMaxPower2ndBlock[pMaxPower2ndBlock < pEpsilon] = 0.0
    pMaxCharge       [pMaxCharge        < pEpsilon] = 0.0
    pEnergyInflows   [pEnergyInflows    < pEpsilon/pTimeStep] = 0.0
    # these parameters are in GWh
    pMinStorage      [pMinStorage       < pEpsilon] = 0.0
    pMaxStorage      [pMaxStorage       < pEpsilon] = 0.0

    # this option avoids a warning in the following assignments
    pd.options.mode.chained_assignment = None

    # minimum up- and downtime converted to an integer number of time steps
    pUpTime = round(pUpTime/pTimeStep).astype('int')
    pDwTime = round(pDwTime/pTimeStep).astype('int')

    # thermal and variable units ordered by increasing variable cost
    mSDUC.go = pLinearVarCost.sort_values().index

    # determine the initial committed units and their output
    pInitialOutput = pd.Series([0.0]*len(mSDUC.g), dfGeneration.index)
    pInitialUC     = pd.Series([0.0]*len(mSDUC.g), dfGeneration.index)
    pSystemOutput  = 0.0
    for go in mSDUC.go:
        n1 = next(iter(mSDUC.sc*mSDUC.n))
        if pSystemOutput < pDemand[n1]:
            if go in mSDUC.r:
                pInitialOutput[go] = pMaxPower[go][n1]
            else:
                pInitialOutput[go] = pMinPower[go][n1]
            pInitialUC    [go] = 1
            pSystemOutput     += pInitialOutput[go]

    #%% variables
    mSDUC.vTotalVCost     = Var(                             within=NonNegativeReals,                                                                            doc='total system variable cost [MEUR]')
    mSDUC.vTotalECost     = Var(                             within=NonNegativeReals,                                                                            doc='total system emission cost [MEUR]')
    mSDUC.vTotalOutput    = Var(mSDUC.sc, mSDUC.n, mSDUC.g , within=NonNegativeReals, bounds=lambda mSDUC,sc,n,g :(0.0,pMaxPower          [g ][sc,n]),           doc='total output of the unit     [GW]')
    mSDUC.vOutput2ndBlock = Var(mSDUC.sc, mSDUC.n, mSDUC.nr, within=NonNegativeReals, bounds=lambda mSDUC,sc,n,nr:(0.0,pMaxPower2ndBlock  [nr][sc,n]),           doc='second block of the unit     [GW]')
    mSDUC.vReserveUp      = Var(mSDUC.sc, mSDUC.n, mSDUC.nr, within=NonNegativeReals, bounds=lambda mSDUC,sc,n,nr:(0.0,pMaxPower2ndBlock  [nr][sc,n]),           doc='operating reserve up         [GW]')
    mSDUC.vReserveDown    = Var(mSDUC.sc, mSDUC.n, mSDUC.nr, within=NonNegativeReals, bounds=lambda mSDUC,sc,n,nr:(0.0,pMaxPower2ndBlock  [nr][sc,n]),           doc='operating reserve down       [GW]')
    mSDUC.vESSInventory   = Var(mSDUC.sc, mSDUC.n, mSDUC.es, within=NonNegativeReals, bounds=lambda mSDUC,sc,n,es:(pMinStorage[es][sc,n],pMaxStorage[es][sc,n]), doc='ESS inventory               [GWh]')
    mSDUC.vESSSpillage    = Var(mSDUC.sc, mSDUC.n, mSDUC.es, within=NonNegativeReals,                                                                            doc='ESS spillage                [GWh]')
    mSDUC.vESSCharge      = Var(mSDUC.sc, mSDUC.n, mSDUC.es, within=NonNegativeReals, bounds=lambda mSDUC,sc,n,es:(0.0,pMaxCharge         [es]      ),           doc='ESS    charge power          [GW]')
    mSDUC.vENS            = Var(mSDUC.sc, mSDUC.n,           within=NonNegativeReals, bounds=lambda mSDUC,sc,n   :(0.0,pDemand                [sc,n]),           doc='energy not served in node    [GW]')

    mSDUC.vCommitment     = Var(          mSDUC.n, mSDUC.nr, within=Binary,                                                                                      doc='commitment of the unit      {0,1}')
    mSDUC.vStartUp        = Var(          mSDUC.n, mSDUC.nr, within=Binary,                                                                                      doc='StartUp    of the unit      {0,1}')
    mSDUC.vShutDown       = Var(          mSDUC.n, mSDUC.nr, within=Binary,                                                                                      doc='ShutDown   of the unit      {0,1}')

    # fixing the ESS inventory at the last load level at the end of the time scope
    for sc,es in mSDUC.sc*mSDUC.es:
        mSDUC.vESSInventory[sc,mSDUC.n.last(),es].fix(pInitialInventory[es])

    #%% definition of the time-steps leap to observe the stored energy at ESS
    pCycleTimeStep = pUpTime*0
    for es in mSDUC.es:
        if  pStorageType[es] == 'Daily'  :
            pCycleTimeStep[es] =        1
        if  pStorageType[es] == 'Weekly'  :
            pCycleTimeStep[es] = int(  24/pTimeStep)
        if  pStorageType[es] == 'Monthly' :
            pCycleTimeStep[es] = int( 168/pTimeStep)

    # fixing the ESS inventory at the end of the following pCycleTimeStep (weekly, yearly), i.e., for daily ESS is fixed at the end of the week, for weekly/monthly ESS is fixed at the end of the year
    for sc,n,es in mSDUC.sc*mSDUC.n*mSDUC.es:
         if pStorageType[es] == 'Daily'   and mSDUC.n.ord(n) % ( 168/pTimeStep) == 0:
             mSDUC.vESSInventory[sc,n,es].fix(pInitialInventory[es])
         if pStorageType[es] == 'Weekly'  and mSDUC.n.ord(n) % (8736/pTimeStep) == 0:
             mSDUC.vESSInventory[sc,n,es].fix(pInitialInventory[es])
         if pStorageType[es] == 'Monthly' and mSDUC.n.ord(n) % (8736/pTimeStep) == 0:
             mSDUC.vESSInventory[sc,n,es].fix(pInitialInventory[es])

    SettingUpDataTime = time.time() - StartTime
    StartTime         = time.time()
    print('Setting up input data                 ... ', round(SettingUpDataTime), 's')

    def eTotalVCost(mSDUC):
        return mSDUC.vTotalVCost == (sum(pScenProb[sc] * pDuration[n] * pENSCost             * mSDUC.vENS        [sc,n   ] for sc,n    in mSDUC.sc*mSDUC.n         ) +
                                     sum(pScenProb[sc] * pDuration[n] * pLinearVarCost  [nr] * mSDUC.vTotalOutput[sc,n,nr] for sc,n,nr in mSDUC.sc*mSDUC.n*mSDUC.nr) +
                                     sum(                pDuration[n] * pConstantVarCost[nr] * mSDUC.vCommitment [   n,nr]                                           +
                                                                        pStartUpCost    [nr] * mSDUC.vStartUp    [   n,nr]                                           +
                                                                        pShutDownCost   [nr] * mSDUC.vShutDown   [   n,nr] for    n,nr in          mSDUC.n*mSDUC.nr) )
    mSDUC.eTotalVCost = Constraint(rule=eTotalVCost, doc='total system variable cost [MEUR]')

    def eTotalECost(mSDUC):
        return mSDUC.vTotalECost == sum(pScenProb[sc] * pCO2Cost * pCO2EmissionRate[nr] * mSDUC.vTotalOutput[sc,n,nr] for sc,n,nr in mSDUC.sc*mSDUC.n*mSDUC.nr)
    mSDUC.eTotalECost = Constraint(rule=eTotalECost, doc='total system emission cost [MEUR]')

    def eTotalTCost(mSDUC):
        return mSDUC.vTotalVCost + mSDUC.vTotalECost
    mSDUC.eTotalTCost = Objective(rule=eTotalTCost, sense=minimize, doc='total system cost [MEUR]')

    GeneratingOFTime = time.time() - StartTime
    StartTime        = time.time()
    print('Generating objective function         ... ', round(GeneratingOFTime), 's')

    #%% constraints
    def eOperReserveUp(mSDUC,sc,n):
        if pOperReserveUp[sc,n]:
            return sum(mSDUC.vReserveUp  [sc,n,nr] for nr in mSDUC.nr) >= pOperReserveUp[sc,n]
        else:
            return Constraint.Skip
    mSDUC.eOperReserveUp = Constraint(mSDUC.sc, mSDUC.n, rule=eOperReserveUp, doc='up   operating reserve [GW]')

    def eOperReserveDw(mSDUC,sc,n):
        if pOperReserveDw[sc,n]:
            return sum(mSDUC.vReserveDown[sc,n,nr] for nr in mSDUC.nr) >= pOperReserveDw[sc,n]
        else:
            return Constraint.Skip
    mSDUC.eOperReserveDw = Constraint(mSDUC.sc, mSDUC.n, rule=eOperReserveDw, doc='down operating reserve [GW]')

    def eBalance(mSDUC,sc,n):
        return sum(mSDUC.vTotalOutput[sc,n,g] for g in mSDUC.g) - sum(mSDUC.vESSCharge[sc,n,es] for es in mSDUC.es) + mSDUC.vENS[sc,n] == pDemand[sc,n]
    mSDUC.eBalance = Constraint(mSDUC.sc, mSDUC.n, rule=eBalance, doc='load generation balance [GW]')

    def eESSInventory(mSDUC,sc,n,es):
        if   mSDUC.n.ord(n) == pCycleTimeStep[es]:
            return pInitialInventory[es]                                         + sum(pDuration[n2]*(pEnergyInflows[es][sc,n2] - mSDUC.vTotalOutput[sc,n2,es] + pEfficiency[es]*mSDUC.vESSCharge[sc,n2,es]) for n2 in list(mSDUC.n2)[mSDUC.n.ord(n)-pCycleTimeStep[es]:mSDUC.n.ord(n)]) == mSDUC.vESSInventory[sc,n,es] + mSDUC.vESSSpillage[sc,n,es]
        elif mSDUC.n.ord(n) >  pCycleTimeStep[es] and mSDUC.n.ord(n) % pCycleTimeStep[es] == 0:
            return mSDUC.vESSInventory[sc,mSDUC.n.prev(n,pCycleTimeStep[es]),es] + sum(pDuration[n2]*(pEnergyInflows[es][sc,n2] - mSDUC.vTotalOutput[sc,n2,es] + pEfficiency[es]*mSDUC.vESSCharge[sc,n2,es]) for n2 in list(mSDUC.n2)[mSDUC.n.ord(n)-pCycleTimeStep[es]:mSDUC.n.ord(n)]) == mSDUC.vESSInventory[sc,n,es] + mSDUC.vESSSpillage[sc,n,es]
        else:
            return Constraint.Skip
    mSDUC.eESSInventory = Constraint(mSDUC.sc, mSDUC.n, mSDUC.es, rule=eESSInventory, doc='ESS inventory balance [GWh]')

    GeneratingRBITime = time.time() - StartTime
    StartTime         = time.time()
    print('Generating reserves/balance/inventory ... ', round(GeneratingRBITime), 's')

    #%%
    def eMaxOutput2ndBlock(mSDUC,sc,n,nr):
        if   pOperReserveUp[sc,n] and pMaxPower2ndBlock[nr][sc,n]:
            return (mSDUC.vOutput2ndBlock[sc,n,nr] + mSDUC.vReserveUp  [sc,n,nr]) / pMaxPower2ndBlock[nr][sc,n] <= mSDUC.vCommitment[n,nr]
        else:
            return Constraint.Skip
    mSDUC.eMaxOutput2ndBlock = Constraint(mSDUC.sc, mSDUC.n, mSDUC.nr, rule=eMaxOutput2ndBlock, doc='max output of the second block of a committed unit [p.u.]')

    def eMinOutput2ndBlock(mSDUC,sc,n,nr):
        if   pOperReserveDw[sc,n] and pMaxPower2ndBlock[nr][sc,n]:
            return (mSDUC.vOutput2ndBlock[sc,n,nr] + mSDUC.vReserveDown[sc,n,nr]) / pMaxPower2ndBlock[nr][sc,n] >= 0.0
        else:
            return Constraint.Skip
    mSDUC.eMinOutput2ndBlock = Constraint(mSDUC.sc, mSDUC.n, mSDUC.nr, rule=eMinOutput2ndBlock, doc='min output of the second block of a committed unit [p.u.]')

    def eTotalOutput(mSDUC,sc,n,nr):
        if pMinPower[nr][sc,n] == 0.0:
            return mSDUC.vTotalOutput[sc,n,nr]                       ==                           mSDUC.vOutput2ndBlock[sc,n,nr]
        else:
            return mSDUC.vTotalOutput[sc,n,nr] / pMinPower[nr][sc,n] == mSDUC.vCommitment[n,nr] + mSDUC.vOutput2ndBlock[sc,n,nr] / pMinPower[nr][sc,n]
    mSDUC.eTotalOutput = Constraint(mSDUC.sc, mSDUC.n, mSDUC.nr, rule=eTotalOutput, doc='total output of a unit [GW]')

    def eUCStrShut(mSDUC,n,nr):
        if n == mSDUC.n.first():
            return mSDUC.vCommitment[n,nr] - pInitialUC[nr]                        == mSDUC.vStartUp[n,nr] - mSDUC.vShutDown[n,nr]
        else:
            return mSDUC.vCommitment[n,nr] - mSDUC.vCommitment[mSDUC.n.prev(n),nr] == mSDUC.vStartUp[n,nr] - mSDUC.vShutDown[n,nr]
    mSDUC.eUCStrShut = Constraint(mSDUC.n, mSDUC.nr, rule=eUCStrShut, doc='relation among commitment startup and shutdown')

    GeneratingGenConsTime = time.time() - StartTime
    StartTime             = time.time()
    print('Generating generation constraints     ... ', round(GeneratingGenConsTime), 's')

    #%%
    def eRampUp(mSDUC,sc,n,t):
        if   pRampUp[t] and pRampUp[t] < pMaxPower2ndBlock[t][sc,n] and n == mSDUC.n.first():
            return (mSDUC.vOutput2ndBlock[sc,n,t] - max(pInitialOutput[t]-pMinPower[t][sc,n],0.0) + mSDUC.vReserveUp  [sc,n,t]) / pDuration[n] / pRampUp[t] <= mSDUC.vCommitment[n,t] - mSDUC.vStartUp[n,t]
        elif pRampUp[t] and pRampUp[t] < pMaxPower2ndBlock[t][sc,n]:
            return (mSDUC.vOutput2ndBlock[sc,n,t] - mSDUC.vOutput2ndBlock[sc,mSDUC.n.prev(n),t]   + mSDUC.vReserveUp  [sc,n,t]) / pDuration[n] / pRampUp[t] <= mSDUC.vCommitment[n,t] - mSDUC.vStartUp[n,t]
        else:
            return Constraint.Skip
    mSDUC.eRampUp = Constraint(mSDUC.sc, mSDUC.n, mSDUC.t, rule=eRampUp, doc='maximum ramp up   [p.u.]')

    def eRampDw(mSDUC,sc,n,t):
        if   pRampDw[t] and pRampDw[t] < pMaxPower2ndBlock[t][sc,n] and n == mSDUC.n.first():
            return (mSDUC.vOutput2ndBlock[sc,n,t] - max(pInitialOutput[t]-pMinPower[t][sc,n],0.0) - mSDUC.vReserveDown[sc,n,t]) / pDuration[n] / pRampDw[t] >= - pInitialUC[t]                        + mSDUC.vShutDown[n,t]
        elif pRampDw[t] and pRampDw[t] < pMaxPower2ndBlock[t][sc,n]:
            return (mSDUC.vOutput2ndBlock[sc,n,t] - mSDUC.vOutput2ndBlock[sc,mSDUC.n.prev(n),t]   - mSDUC.vReserveDown[sc,n,t]) / pDuration[n] / pRampDw[t] >= - mSDUC.vCommitment[mSDUC.n.prev(n),t] + mSDUC.vShutDown[n,t]
        else:
            return Constraint.Skip
    mSDUC.eRampDw = Constraint(mSDUC.sc, mSDUC.n, mSDUC.t, rule=eRampDw, doc='maximum ramp down [p.u.]')

    GeneratingRampsTime = time.time() - StartTime
    StartTime           = time.time()
    print('Generating ramps   up/down            ... ', round(GeneratingRampsTime), 's')

    #%%
    def eMinUpTime(mSDUC,n,t):
        if pUpTime[t] > 1 and mSDUC.n.ord(n) >= pUpTime[t]:
            return sum(mSDUC.vStartUp [n2,t] for n2 in list(mSDUC.n2)[mSDUC.n.ord(n)-pUpTime[t]:mSDUC.n.ord(n)]) <=     mSDUC.vCommitment[n,t]
        else:
            return Constraint.Skip
    mSDUC.eMinUpTime   = Constraint(mSDUC.n, mSDUC.t, rule=eMinUpTime  , doc='minimum up   time [h]')

    def eMinDownTime(mSDUC,n,t):
        if pDwTime[t] > 1 and mSDUC.n.ord(n) >= pDwTime[t]:
            return sum(mSDUC.vShutDown[n2,t] for n2 in list(mSDUC.n2)[mSDUC.n.ord(n)-pDwTime[t]:mSDUC.n.ord(n)]) <= 1 - mSDUC.vCommitment[n,t]
        else:
            return Constraint.Skip
    mSDUC.eMinDownTime = Constraint(mSDUC.n, mSDUC.t, rule=eMinDownTime, doc='minimum down time [h]')

    GeneratingMinUDTime = time.time() - StartTime
    StartTime           = time.time()
    print('Generating minimum up/down time       ... ', round(GeneratingMinUDTime), 's')

    #%% solving the problem
    mSDUC.write(_path+'/openSDUC_'+CaseName+'.lp', io_options={'symbolic_solver_labels': True}) # create lp-format file
    Solver = SolverFactory(SolverName)                                                   # select solver
    if SolverName == 'gurobi':
        Solver.options['LogFile'       ] = _path+'/openSDUC_'+CaseName+'.log'
        #Solver.options['IISFile'      ] = 'openSDUC_'+CaseName+'.ilp'                   # should be uncommented to show results of IIS
        #Solver.options['Method'       ] = 2                                             # barrier method
        Solver.options['MIPGap'        ] = 0.02
        Solver.options['Threads'       ] = int((psutil.cpu_count(logical=True) + psutil.cpu_count(logical=False))/2)
        #Solver.options['TimeLimit'     ] = 7200
        #Solver.options['IterationLimit'] = 7200000
    SolverResults = Solver.solve(mSDUC, tee=True)                                        # tee=True displays the output of the solver
    SolverResults.write()                                                                # summary of the solver results

    #%% fix values of binary variables to get dual variables and solve it again
    for n,nr in mSDUC.n*mSDUC.nr:
        mSDUC.vCommitment[n,nr].fix(round(mSDUC.vCommitment[n,nr]()))
        mSDUC.vStartUp   [n,nr].fix(round(mSDUC.vStartUp   [n,nr]()))
        mSDUC.vShutDown  [n,nr].fix(round(mSDUC.vShutDown  [n,nr]()))

    if SolverName == 'gurobi':
        Solver.options['relax_integrality'] = 1                                          # introduced to show results of the dual variables
    mSDUC.dual    = Suffix(direction=Suffix.IMPORT)
    SolverResults = Solver.solve(mSDUC, tee=True)                                        # tee=True displays the output of the solver
    SolverResults.write()                                                                # summary of the solver results

    SolvingTime = time.time() - StartTime
    StartTime   = time.time()
    print('Solving                               ... ', round(SolvingTime), 's')

    print('Objective function value                  ', mSDUC.eTotalTCost.expr())

    #%% inverse index generator to technology and to company
    pTechnologyToGen = pGenToTechnology.reset_index().set_index('Technology').set_axis(['Generator'], axis=1, copy=False)[['Generator']]
    pTechnologyToGen = pTechnologyToGen.loc[pTechnologyToGen['Generator'].isin(mSDUC.g)]
    pTechnology2Gen  = pTechnologyToGen.reset_index().set_index(['Technology', 'Generator'])

    mSDUC.t2g = Set(initialize=pTechnology2Gen.index, ordered=False, doc='technology to generator')

    #%% outputting the generation operation

    OutputResults = pd.Series(data=[mSDUC.vCommitment[n,nr]() for n,nr in mSDUC.n*mSDUC.nr], index=pd.MultiIndex.from_tuples(list(mSDUC.n*mSDUC.nr)))
    OutputResults.to_frame(name='p.u.').reset_index().pivot_table(index=['level_0'], columns='level_1', values='p.u.').rename_axis(['LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_GenerationCommitment_'+CaseName+'.csv', sep=',')
    OutputResults = pd.Series(data=[mSDUC.vStartUp   [n,nr]() for n,nr in mSDUC.n*mSDUC.nr], index=pd.MultiIndex.from_tuples(list(mSDUC.n*mSDUC.nr)))
    OutputResults.to_frame(name='p.u.').reset_index().pivot_table(index=['level_0'], columns='level_1', values='p.u.').rename_axis(['LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_GenerationStartUp_'   +CaseName+'.csv', sep=',')
    OutputResults = pd.Series(data=[mSDUC.vShutDown  [n,nr]() for n,nr in mSDUC.n*mSDUC.nr], index=pd.MultiIndex.from_tuples(list(mSDUC.n*mSDUC.nr)))
    OutputResults.to_frame(name='p.u.').reset_index().pivot_table(index=['level_0'], columns='level_1', values='p.u.').rename_axis(['LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_GenerationShutDown_'  +CaseName+'.csv', sep=',')

    if sum(pOperReserveUp[sc,n] for sc,n in mSDUC.sc*mSDUC.n):
        OutputResults = pd.Series(data=[mSDUC.vReserveUp  [sc,n,nr]()*1e3 for sc,n,nr in mSDUC.sc*mSDUC.n*mSDUC.nr], index=pd.MultiIndex.from_tuples(list(mSDUC.sc*mSDUC.n*mSDUC.nr)))
        OutputResults.to_frame(name='MW').reset_index().pivot_table(index=['level_0','level_1'], columns='level_2', values='MW').rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_GenerationReserveUp_'+CaseName+'.csv', sep=',')

    if sum(pOperReserveDw[sc,n] for sc,n in mSDUC.sc*mSDUC.n):
        OutputResults = pd.Series(data=[mSDUC.vReserveDown[sc,n,nr]()*1e3 for sc,n,nr in mSDUC.sc*mSDUC.n*mSDUC.nr], index=pd.MultiIndex.from_tuples(list(mSDUC.sc*mSDUC.n*mSDUC.nr)))
        OutputResults.to_frame(name='MW').reset_index().pivot_table(index=['level_0','level_1'], columns='level_2', values='MW').rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_GenerationReserveDown_'+CaseName+'.csv', sep=',')

    OutputResults = pd.Series(data=[mSDUC.vTotalOutput[sc,n,g]()*1e3 for sc,n,g in mSDUC.sc*mSDUC.n*mSDUC.g], index=pd.MultiIndex.from_tuples(list(mSDUC.sc*mSDUC.n*mSDUC.g)))
    OutputResults.to_frame(name='MW').reset_index().pivot_table(index=['level_0','level_1'], columns='level_2', values='MW').rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_GenerationOutput_'+CaseName+'.csv', sep=',')

    OutputResults = pd.Series(data=[mSDUC.vENS[sc,n]()*1e3 for sc,n in mSDUC.sc*mSDUC.n], index=pd.MultiIndex.from_tuples(list(mSDUC.sc*mSDUC.n)))
    OutputResults.to_frame(name='MW').reset_index().pivot_table(index=['level_0','level_1'], values='MW').rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_PNS_'+CaseName+'.csv', sep=',')

    OutputResults = pd.Series(data=[mSDUC.vENS[sc,n]()*pDuration[n] for sc,n in mSDUC.sc*mSDUC.n], index=pd.MultiIndex.from_tuples(list(mSDUC.sc*mSDUC.n)))
    OutputResults.to_frame(name='GWh').reset_index().pivot_table(index=['level_0','level_1'], values='GWh').rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_ENS_'+CaseName+'.csv', sep=',')

    OutputResults = pd.Series(data=[(mSDUC.vTotalOutput[sc,n,g].ub-mSDUC.vTotalOutput[sc,n,g]())*1e3 for sc,n,g in mSDUC.sc*mSDUC.n*mSDUC.r], index=pd.MultiIndex.from_tuples(list(mSDUC.sc*mSDUC.n*mSDUC.r)))
    OutputResults.to_frame(name='MW').reset_index().pivot_table(index=['level_0','level_1'], columns='level_2', values='MW').rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_RESCurtailment_'+CaseName+'.csv', sep=',')

    #%% plot SRMC for all the scenarios
    RESCurtailment = OutputResults.loc[:,:,:]

    fig, fg = plt.subplots()
    for r in mSDUC.r:
        fg.plot(range(len(mSDUC.sc*mSDUC.n)), RESCurtailment[:,:,r], label=r)
    fg.set(xlabel='Hours', ylabel='MW')
    fg.set_ybound(lower=0)
    plt.title('RES Curtailment')
    fg.tick_params(axis='x', rotation=90)
    fg.legend()
    plt.tight_layout()
    #plt.show()
    plt.savefig(_path+'/oUC_Plot_RESCurtailment_'+CaseName+'.png', bbox_inches=None)

    OutputResults = pd.Series(data=[mSDUC.vTotalOutput[sc,n,g]()*pDuration[n]                                      for sc,n,g in mSDUC.sc*mSDUC.n*mSDUC.g], index=pd.MultiIndex.from_tuples(list(mSDUC.sc*mSDUC.n*mSDUC.g)))
    OutputResults.to_frame(name='GWh' ).reset_index().pivot_table(index=['level_0','level_1'], columns='level_2', values='GWh' ).rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_GenerationEnergy_'+CaseName+'.csv', sep=',')

    OutputResults = pd.Series(data=[mSDUC.vTotalOutput[sc,n,nr]()*pCO2EmissionRate[nr]*1e3                         for sc,n,nr in mSDUC.sc*mSDUC.n*mSDUC.t], index=pd.MultiIndex.from_tuples(list(mSDUC.sc*mSDUC.n*mSDUC.t)))
    OutputResults.to_frame(name='tCO2').reset_index().pivot_table(index=['level_0','level_1'], columns='level_2', values='tCO2').rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_GenerationEmission_'+CaseName+'.csv', sep=',')

    #%% outputting the ESS operation
    if len(mSDUC.es):
        OutputResults = pd.Series(data=[mSDUC.vESSCharge[sc,n,es]()*1e3                                        for sc,n,es in mSDUC.sc*mSDUC.n*mSDUC.es], index=pd.MultiIndex.from_tuples(list(mSDUC.sc*mSDUC.n*mSDUC.es)))
        OutputResults.to_frame(name='MW' ).reset_index().pivot_table(index=['level_0','level_1'], columns='level_2', values='MW' ).rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_ESSChargeOutput_'+CaseName+'.csv', sep=',')

        OutputResults = pd.Series(data=[sum(OutputResults[sc,n,es] for es in mSDUC.es if (gt,es) in mSDUC.t2g) for sc,n,gt in mSDUC.sc*mSDUC.n*mSDUC.gt if sum(1 for es in mSDUC.es if (gt,es) in mSDUC.t2g)], index=pd.MultiIndex.from_tuples([(sc,n,gt) for sc,n,gt in mSDUC.sc*mSDUC.n*mSDUC.gt if sum(1 for es in mSDUC.es if (gt,es) in mSDUC.t2g)]))
        OutputResults.to_frame(name='MW' ).reset_index().pivot_table(index=['level_0','level_1'], columns='level_2', values='MW' ).rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_TechnologyCharge_'+CaseName+'.csv', sep=',')

        TechnologyCharge = OutputResults.loc[:,:,:]

        OutputResults = pd.Series(data=[mSDUC.vESSCharge[sc,n,es]()*pDuration[n]                               for sc,n,es in mSDUC.sc*mSDUC.n*mSDUC.es], index=pd.MultiIndex.from_tuples(list(mSDUC.sc*mSDUC.n*mSDUC.es)))
        OutputResults.to_frame(name='GWh').reset_index().pivot_table(index=['level_0','level_1'], columns='level_2', values='GWh').rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_ESSChargeEnergy_'+CaseName+'.csv', sep=',')

        OutputResults = pd.Series(data=[sum(OutputResults[sc,n,es] for es in mSDUC.es if (gt,es) in mSDUC.t2g) for sc,n,gt in mSDUC.sc*mSDUC.n*mSDUC.gt if sum(1 for es in mSDUC.es if (gt,es) in mSDUC.t2g)], index=pd.MultiIndex.from_tuples([(sc,n,gt) for sc,n,gt in mSDUC.sc*mSDUC.n*mSDUC.gt if sum(1 for es in mSDUC.es if (gt,es) in mSDUC.t2g)]))
        OutputResults.to_frame(name='GWh').reset_index().pivot_table(index=['level_0','level_1'], columns='level_2', values='GWh').rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_ESSTechnologyEnergy_'+CaseName+'.csv', sep=',')

        OutputResults = pd.Series(data=[mSDUC.vESSInventory[sc,n,es]()                                         for sc,n,es in mSDUC.sc*mSDUC.n*mSDUC.es], index=pd.MultiIndex.from_tuples(list(mSDUC.sc*mSDUC.n*mSDUC.es)))
        OutputResults.to_frame(name='GWh').reset_index().pivot_table(index=['level_0','level_1'], columns='level_2', values='GWh', dropna=False).rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_ESSInventory_'+CaseName+'.csv', sep=',')

        OutputResults = pd.Series(data=[mSDUC.vESSSpillage [sc,n,es]()                                         for sc,n,es in mSDUC.sc*mSDUC.n*mSDUC.es], index=pd.MultiIndex.from_tuples(list(mSDUC.sc*mSDUC.n*mSDUC.es)))
        OutputResults.to_frame(name='GWh').reset_index().pivot_table(index=['level_0','level_1'], columns='level_2', values='GWh', dropna=False).rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_ESSSpillage_'+CaseName+'.csv', sep=',')

    OutputResults = pd.Series(data=[mSDUC.vTotalOutput[sc,n,g]()*1e3                                           for sc,n,g  in mSDUC.sc*mSDUC.n*mSDUC.g ], index=pd.MultiIndex.from_tuples(list(mSDUC.sc*mSDUC.n*mSDUC.g )))
    OutputResults = pd.Series(data=[sum(OutputResults[sc,n,g] for g  in mSDUC.g  if (gt,g ) in mSDUC.t2g)      for sc,n,gt in mSDUC.sc*mSDUC.n*mSDUC.gt if sum(1 for g in mSDUC.g if (gt,g) in mSDUC.t2g)], index=pd.MultiIndex.from_tuples([(sc,n,gt) for sc,n,gt in mSDUC.sc*mSDUC.n*mSDUC.gt if sum(1 for g in mSDUC.g if (gt,g) in mSDUC.t2g)]))
    OutputResults.to_frame(name='MW').reset_index().pivot_table(index=['level_0','level_1'], columns='level_2', values='MW').rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_TechnologyOutput_'+CaseName+'.csv', sep=',')

    TechnologyOutput = OutputResults.loc[:,:,:]

    for sc in mSDUC.sc:
        fig, fg = plt.subplots()
        fg.stackplot(range(len(mSDUC.n)),  TechnologyOutput.loc[sc,:,:].values.reshape(len(mSDUC.n),len(mSDUC.gt)).transpose().tolist(), baseline='zero', labels=list(mSDUC.gt))
        fg.plot     (range(len(mSDUC.n)), -TechnologyCharge.loc[sc,:,'ESS'], label='ESSCharge', linewidth=0.5, color='b')
        fg.plot     (range(len(mSDUC.n)),  pDemand[sc]*1e3,                  label='Demand'   , linewidth=0.5, color='k')
        fg.set(xlabel='Hours', ylabel='MW')
        plt.title(sc)
        fg.tick_params(axis='x', rotation=90)
        fg.legend()
        plt.tight_layout()
        #plt.show()
        plt.savefig(_path+'/oUC_Plot_TechnologyOutput_'+sc+'_'+CaseName+'.png', bbox_inches=None)

    OutputResults = pd.Series(data=[mSDUC.vTotalOutput[sc,n,g]()*pDuration[n]                          for sc,n,g in mSDUC.sc*mSDUC.n*mSDUC.g], index=pd.MultiIndex.from_tuples(list(mSDUC.sc*mSDUC.n*mSDUC.g)))
    OutputResults = pd.Series(data=[sum(OutputResults[sc,n,g] for g in mSDUC.g if (gt,g) in mSDUC.t2g) for sc,n,gt in mSDUC.sc*mSDUC.n*mSDUC.gt if sum(1 for g in mSDUC.g if (gt,g) in mSDUC.t2g)], index=pd.MultiIndex.from_tuples([(sc,n,gt) for sc,n,gt in mSDUC.sc*mSDUC.n*mSDUC.gt if sum(1 for g in mSDUC.g if (gt,g) in mSDUC.t2g)]))
    OutputResults.to_frame(name='GWh').reset_index().pivot_table(index=['level_0','level_1'], columns='level_2', values='GWh').rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_TechnologyEnergy_'+CaseName+'.csv', sep=',')

    #%% outputting the SRMC
    if SolverName == 'gurobi':
        OutputResults = pd.Series(data=[mSDUC.dual[mSDUC.eBalance[sc,n]]*1e3/pScenProb[sc]/pDuration[n] for sc,n in mSDUC.sc*mSDUC.n], index=pd.MultiIndex.from_tuples(list(mSDUC.sc*mSDUC.n)))
        OutputResults.to_frame(name='SRMC').reset_index().pivot_table(index=['level_0','level_1'], values='SRMC').rename_axis(['Scenario','LoadLevel'], axis=0).rename_axis([None], axis=1).to_csv(_path+'/oUC_Result_SRMC_'+CaseName+'.csv', sep=',')

        #%% plot SRMC for all the scenarios
        SRMC = OutputResults.loc[:,:]

        fig, fg = plt.subplots()
        for sc in mSDUC.sc:
            fg.plot(range(len(mSDUC.n)), SRMC[sc], label=sc)
            fg.set(xlabel='Hours', ylabel='EUR/MWh')
            fg.set_ybound(lower=0, upper=100)
            plt.title('SRMC')
            fg.tick_params(axis='x', rotation=90)
            fg.legend()
            plt.tight_layout()
            #plt.show()
            plt.savefig(_path+'/oUC_Plot_SRMC_'+CaseName+'.png', bbox_inches=None)

    WritingResultsTime = time.time() - StartTime
    StartTime          = time.time()
    print('Writing output results                ... ', round(WritingResultsTime), 's')
    print('Total time                            ... ', round(ReadingDataTime + GeneratingOFTime + GeneratingRBITime + GeneratingGenConsTime + GeneratingRampsTime + GeneratingMinUDTime + SolvingTime + WritingResultsTime), 's')
    print('\n #### Academic research license - for non-commercial use only #### \n')

if __name__ == '__main__':
    main()
