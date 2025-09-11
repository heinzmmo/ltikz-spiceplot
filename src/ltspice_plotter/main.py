#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys 

from .plotter import plot_all_signals
from .parser import parse_ltspice_txt, parse_ltspice_raw, get_all_signals
from .utils import filter_data_frame

def parse_arguments():
    """
    Parse CL arguments
    """

    parser = argparse.ArgumentParser(
        description="Plotting LTspice simulation data",
        epilog="Example: ltspice-plot data.txt -s 'I(R2)' -o plot.pdf"
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


def read_simulation_data(filepath_arg:str):
    supported_input_formats = ('.raw', '.txt')
    if filepath_arg.lower().endswith(supported_input_formats):
        if filepath_arg.lower().endswith('.txt'):
            return parse_ltspice_txt(filepath_arg)
        elif filepath_arg.lower().endswith('.raw'):
            return parse_ltspice_raw(filepath_arg)
    else:
        raise ValueError('Unsupported file type. Use .txt or .raw')


def validate_output_format(output_arg:str):
    supported_output_formats = ('.pdf', '.jpg', '.jpeg', '.png', '.tex')
    if not output_arg.lower().endswith(supported_output_formats):
        raise ValueError(f"Unsupported format. Use: {', '.join(supported_output_formats)}")


def main():

    args = parse_arguments()

    try:
        # Read simulation data
        simulation_data = read_simulation_data(args.filepath)

        # Validate output format, if given
        if args.output is not None:
            validate_output_format(args.output)

        if args.available is True:
            print(get_all_signals(simulation_data))
            sys.exit(0)
        
        if args.signals is not None:
            filtered_data = filter_data_frame(simulation_data, args.signals)         
            plot_all_signals(filtered_data,args.title, args.output)
        else:
            plot_all_signals(simulation_data, args.title, args.output)

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
