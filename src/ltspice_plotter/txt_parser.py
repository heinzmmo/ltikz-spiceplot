"""
LTspice .txt parser module
"""
import pandas as pd
from pathlib import Path


def parse_ltspice_txt(filename):
    """
    Load LTspice .txt export into pandas DataFrame

    Arg: 
        filename (str): Path to to LTspice .txt file 

    Return: 
        pd.DataFrame(): Parsed simulation data

    Raises:
        FileNotFoundError: If file doesn't exist
        pd.errors.EmptyDataError: If file is empty
    """

    filepath = Path(filename)

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filename}")

    try: 
        df = pd.read_csv(filepath, sep='\t')
        return df
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(f"File is empty: {filename}")


def get_time_column(df):
    """
    Get the time column for DataFrame

    Args:
        df (pd.DataFrame): Simulation data

    Return:
        str: Name of time column

    Raises:
        ValueErros: If no time column found
    """
    
    # Ltspice ueses 'time' als column name
    if 'time' in df.columns:
        return 'time'

    # Fallback: First column is usually time
    if len(df.columns) > 0:
        return df.columns[0]


def get_voltage_signals(df):
    """
    Get all voltage signal column names

    Args: 
        df (pd.DataFrame): Simulation data

    Return:
        list: List of all voltage column names (V(xxx))
    """
    
    return [col for col in df.columns if col.startswith('V(')]


def get_current_signals(df):
    """
    Get all current signal column names

    Args: 
        df (pd.DataFrame): Simulation data

    Return:
        list: List of all current column names (V(xxx))
    """
    
    return [col for col in df.columns if col.startswith('I(')]


def get_all_signals(df):
    """
    Get all signal column names (excluding time)

    Args: 
        df (pd.DataFrame): Simulation data

    Return:
        list: List of all signal column names
    """

    time_col = get_time_column(df) 
    return [col for col in df.columns if col != time_col]


def get_signal_info(df):
    """
    Get summary information about available signals

    Args: 
        df (pd.DataFrame): Simulation data

    Retuns:
        dict: Dictionary with signal information
    """

    time_col = get_time_column(df)
    voltages = get_voltage_signals(df) 
    currents = get_current_signals(df)

    return {
        'time_column': time_col,
        'voltage_signals': voltages,
        'current_signals': currents,
        'total_signals': len(voltages) + len(currents),
        'time_range': (df[time_col].min(), df[time_col].max()),
        'data_points': len(df)
    }

