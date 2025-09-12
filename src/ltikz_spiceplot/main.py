#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys

from .parser import read_simulation_data

from .handlers import(
    handel_list_available_signals,
    handle_plot_signals,
    handle_output
)

def parse_arguments():
    """
    Parse CL arguments
    """
    epilog = r"""
  _   _____ _ _     _____    ____        _          ____  _       _   
 | | |_   _(_) | __|__  /   / ___| _ __ (_) ___ ___|  _ \| | ___ | |_ 
 | |   | | | | |/ /  / /____\___ \| '_ \| |/ __/ _ \ |_) | |/ _ \| __|
 | |___| | | |   <  / /|_____|__) | |_) | | (_|  __/  __/| | (_) | |_ 
 |_____|_| |_|_|\_\/____|   |____/| .__/|_|\___\___|_|   |_|\___/ \__|
                                  |_|                                  
    """
    parser = argparse.ArgumentParser(
        prog='lt2tikzplot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Plotting LTspice simulation data",
        epilog=epilog
    )

    parser.add_argument(
        "filepath",
        help="Path to .txt file, created by LTspice"
    )
    
    parser.add_argument(
        "-a",
        "--available",
        action='store_true',
        help="Print available singal names"
    )

    parser.add_argument(
        "-s",
        "--signals",
        default=None,
        nargs='+',
        help="Name of signals to plot. Must be identical to LTspice singal names"
    )

    parser.add_argument(
        "--legend-loc",
        default='best',
        metavar='LEGEND LOCATION',
        help="Location of legend."
    )

    parser.add_argument(
        "-t",
        "--title",
        default=None,
        metavar='FIG TITLE',
        help="Title of the figure/plot"
    )

    parser.add_argument(
        "-o",
        "--output",
        default=None,
        metavar='FILE',
        help="Output filename. Supported formats: .pdf, .jpg, .jpeg, .png"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="ltspice-plotter v0.1"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    try:
        # Parse simulation data
        simulation_df = read_simulation_data(args.filepath)

        if args.available is True:
            handel_list_available_signals(simulation_df)     
        else:
            # Create figure
            fig = handle_plot_signals(simulation_df,
                                      args.signals,
                                      args.title,
                                      args.legend_loc) 
            # Export or show figure
            handle_output(fig, args.output)

    # Error handeling
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

    
if __name__ == "__main__":
    main()
