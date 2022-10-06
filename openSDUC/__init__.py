"""
Open Stochastic Daily Unit Commitment of Thermal and Hydro Units (openSDUC) - Version 1.3.28 - April 5, 2022

    Args:
        case:   Name of the folder where the CSV files of the case are found
        dir:    Main path where the case folder can be found
        solver: Name of the solver

    Returns:
        Output results in CSV files that are found in the case folder.

    Examples:
        >>> import openSDUC as oT
        >>> oT.routine("9n", "C:\\Users\\UserName\\Documents\\GitHub\\openTEPES", "glpk")
"""
__version__ = "1.3.28"
