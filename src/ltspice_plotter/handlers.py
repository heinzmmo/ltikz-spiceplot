import sys

from .parser import (
    get_all_signals,
    get_signal_info
)
from .utils import(
    filter_data_frame
)

from .plotter import(
    figure_create,
    figure_export,
    figure_show
)


def handel_list_available_signals(simulation_df):
    """Handle --available flag: list all available signal names""" 
    print(f"Total available singals: {get_signal_info(simulation_df)
          ['total_signals']}\nTrace names: {get_all_signals(simulation_df)}")
    sys.exit(0)


def handle_plot_signals(simulation_df,
                        signals_arg=None,
                        title_arg=None,
                        legend_loc_arg=None):
    """Handle plotting with optional signal selection"""
    if signals_arg is None:
        fig = figure_create(simulation_df, legend_loc_arg, title_arg)
    else:
        filtered_data = filter_data_frame(simulation_df, signals_arg)         
        fig = figure_create(filtered_data, legend_loc_arg, title_arg)

    return fig


def handle_output(figure, output_arg=None):
    """Handle output: export or show figure"""
    if output_arg:
        figure_export(figure, output_arg)
    else:
        figure_show(figure)

