#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys 

from .plotter import plot_all_singls
from .txt_parser import parse_ltspice_txt

def main():
    """
    Main function with CLI-Interface
    """

    parser = argparse.ArgumentParser(
        description="Plotting LTspice simulation data",
        epilog="Example: ltspice-plot data.txt -o plot.pdf"
    )

    parser.add_argument(
        "filepath",
        help="Path to .txt file, created by LTspice"
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

    args = parser.parse_args()

    # Validate output format 
    if args.output is not None:
        supported_formats = ('.pdf', '.jpg', '.jpeg', '.png')
        if not args.output.lower().endswith(supported_formats):
            print(f"Error: Unsupported format. Use: {', '.join(supported_formats)}")
            sys.exit(1)

    try:
        simulation_data = parse_ltspice_txt(args.filepath)
        plot_all_singls(simulation_data, args.output)

    # Error handeling for main.py
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

    
if __name__ == "__main__":
    main()
