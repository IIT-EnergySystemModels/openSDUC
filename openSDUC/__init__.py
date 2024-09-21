"""
Open Stochastic Daily Unit Commitment of Thermal and ESS Units (openSDUC) - Version 1.3.31 - September 21, 2024

    Args:
        case:   Name of the folder where the CSV files of the case are found
        dir:    Main path where the case folder can be found
        solver: Name of the solver

    Returns:
        Output results in CSV files that are found in the case folder.

    Examples:
        >>> import openSDUC as oT
        >>> oT.routine("16g", "C:\\Users\\UserName\\Documents\\GitHub\\openSDUC", "glpk")
"""
__version__ = "1.3.31"

from .openSDUC_main             import main
