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

Examples:
  %(prog)s simulation.raw --available
      List all available signals in the file

  %(prog)s simulation.raw
      Plot all signals (interactive matplotlib window)

  %(prog)s simulation.raw -s V(out) I(R1) -o output.pdf
      Plot specific signals and save as PDF

  %(prog)s simulation.raw --style ieee -t "Buck Converter" -o plot.tex
      Create TikZ plot with IEEE style and custom title

For more information: https://github.com/heinzmmo/ltikz-spiceplot
    """
    parser = argparse.ArgumentParser(
        prog='ltplot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Create plots from LTspice simulation data",
        epilog=epilog
    )

    parser.add_argument(
        "filepath",
        help="Path to LTspice .raw (binary) or .txt (text export) file"
    )

    parser.add_argument(
        "-a",
        "--available",
        action='store_true',
        help="List all available signal names and exit"
    )

    parser.add_argument(
        "-s",
        "--signals",
        default=None,
        nargs='+',
        metavar='SIGNAL',
        help="Signal names to plot (e.g., 'V(out)' 'I(R1)'). Must match LTspice signal names / --available output exactly"
    )

    parser.add_argument(
        "--legend-loc",
        default='best',
        metavar='LOC',
        help="Legend location: 'best', 'upper right', 'lower left', etc. (default: best)"
    )

    parser.add_argument(
        "-t",
        "--title",
        default=None,
        metavar='TITLE',
        help="Figure title (optional)"
    )

    parser.add_argument(
        "--style",
        default="ieee",
        choices=['de', 'ieee', 'ieee_bw', 'de_bw'],
        metavar="STYLE",
        help="Plot style: 'de' (U/I), 'ieee' (V/I), 'ieee_bw/de_bw' (black & white). Default: ieee"
    )

    parser.add_argument(
        "-o",
        "--output",
        default=None,
        metavar='FILE',
        help="Output filename (.pdf, .tex). If omitted, shows interactive plot"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s v0.1.0-beta"
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
                                      args.legend_loc,
                                      args.style)
            # Export or show figure
            handle_output(fig, args.output)

    # Error handeling
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Please report this issue at: https://github.com/heinzmmo/ltikz-spiceplot/issues", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
