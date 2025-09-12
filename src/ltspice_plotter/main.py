#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys

from .plotter import figure_create, figure_show, figure_export
from .parser import read_simulation_data, get_all_signals, get_signal_info
from .utils import filter_data_frame

def parse_arguments():
    """
    Parse CL arguments
    """
    epilog = r"""
██╗  ████████╗██╗██╗  ██╗███████╗     ███████╗██████╗ ██╗ ██████╗███████╗██████╗ ██╗      ██████╗ ████████╗
██║  ╚══██╔══╝██║██║ ██╔╝╚══███╔╝     ██╔════╝██╔══██╗██║██╔════╝██╔════╝██╔══██╗██║     ██╔═══██╗╚══██╔══╝
██║     ██║   ██║█████╔╝   ███╔╝█████╗███████╗██████╔╝██║██║     █████╗  ██████╔╝██║     ██║   ██║   ██║   
██║     ██║   ██║██╔═██╗  ███╔╝ ╚════╝╚════██║██╔═══╝ ██║██║     ██╔══╝  ██╔═══╝ ██║     ██║   ██║   ██║   
███████╗██║   ██║██║  ██╗███████╗     ███████║██║     ██║╚██████╗███████╗██║     ███████╗╚██████╔╝   ██║   
╚══════╝╚═╝   ╚═╝╚═╝  ╚═╝╚══════╝     ╚══════╝╚═╝     ╚═╝ ╚═════╝╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝   
    """
    parser = argparse.ArgumentParser(
        prog='lt2tikz',
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
        "-lp",
        "--legend-pos",
        default='best',
        metavar='LEGEND POSITION',
        help="Position of legend."
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
        # Read simulation data
        simulation_data = read_simulation_data(args.filepath)

        if args.available is True:
            print(f"Total available singals: {get_signal_info(simulation_data)
                  ['total_signals']}\nTrace names: {get_all_signals(simulation_data)}")
            sys.exit(0)
        
        # Create figure (plots)
        if args.signals:
            filtered_data = filter_data_frame(simulation_data, args.signals)         
            fig = figure_create(filtered_data,args.legend_pos, args.title)
        else:
            fig = figure_create(simulation_data, args.legend_pos, args.title)
        
        # Export or show figure
        if args.output:
            figure_export(fig, args.output)
        elif args.output is None:
            figure_show(fig)

    # Error handeling for main.py
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
