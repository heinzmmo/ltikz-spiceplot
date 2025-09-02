"""
@author: Moritz Heinzmann
"""

import pandas as pd
from .txt_parser import get_all_signals

def filter_data_frame(simulation_df, signals):
    """
    Filter only the desired signals from the data frame

    Args:
        simulation_df (pd.dataFrame): Parsed simulation data 
        singals (list): List of desired signal names 

    Return:
        pd.dataFrame(): Filtered simulation data

    Raises:
        VaulueError: Desired signal doesn't exist 
    """
    available_signals = get_all_signals(simulation_df)

    if not set(signals).issubset(available_signals):
        raise ValueError("One or more of the desired signals are not present in the simulation data")


    return pd.concat([simulation_df['time'], simulation_df[signals]], axis=1)


def signal_name_tex(signal_name):
    """
    Convert the LTspice signal names into LaTeX math format

    Arg:
        signal_name (str): LTspice signal name

    Return: 
        label_tex (str): singal label in LaTeX math format
    """
    index = []
    label_tex = []

    if signal_name.startswith('V'):
        index = signal_name[1:].strip("()")
        label_tex = r'$V_{\mathrm{' + index + '}}$'
        return label_tex

    elif signal_name.startswith('I'):
        index = signal_name[1:].strip("()")
        label_tex = r'$I_{\mathrm{' + index[0] + '_{' + index[1:] + '}}}$'
        return label_tex
    
    else:
        return signal_name
