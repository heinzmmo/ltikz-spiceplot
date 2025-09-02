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
