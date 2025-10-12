# LTikZ-SpicePlot
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg) ![Status](https://img.shields.io/badge/status-beta-yellow.svg) ![Tests](https://img.shields.io/badge/tests-in%20progress-orange.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg)

A Python bridge between LTspice and Matplotlib/Matplot2TikZ for creating beautiful, publication-ready plots from LTspice simulation data.

## Status

**Note**: This project is functional. Test coverage is currently being expanded. Contributions are welcome!

## Featurtes

LTspice is a powerful circuit simulator, but its built-in plotting capabilities are limited and not suitable for publications or presentations. **LTikZ-SpicePlot** features:

- **Beautiful matplotlib plots** with style prestes
- **Multiple input formats**: `.raw` (binary) and `.txt` (exported) LTspice files
- **Direct TikZ export** for seamless LaTeX integration
- **Easy CLI interface** for quick visualizations

## Installation

```bash
pipx install git+https://github.com/heinzmmo/ltikz_spiceplot.git
```

### Requirements
- Python 3.8+
- TeX Live

## Usage

### Command Line Interface

```bash
# Show all available signals in your simulation
ltplot simulation.raw --available

# Plot all signals (opens matplotlib window)
ltplot simulation.raw

# Plot specific signals
ltplot simulation.raw --signals 'V(out)' 'I(R1)'

# Export as PDF
ltplot simulation.raw --output plot.pdf

# Export as TikZ for LaTeX
ltplot simulation.raw --output plot.tex

# Use IEEE style with custom title
ltplot simulation.raw --style ieee --title "Buck Converter Output"
```

## Style Options

### DE Style
- Uses $U$ for voltage (European convention)
- Format: $U/\mathrm{mV}$, $I/\mathrm{\mu A}$

### IEEE Style (default)
- Uses $V$ for voltage (US convention)
- Format: Voltage ($\mathrm{mV}$), Current ($\mathrm{\mu A}$)

### Black and White Style
- Optimized for black & white printing
- Uses different line styles instead of colors

```bash
ltplot data.raw --style ieee     # Default
ltplot data.raw --style de       # DE style
ltplot data.raw --style ieee_bw  # IEEE black & white
ltplot data.raw --style de_bw    # DE black & white
```

## Examples

## CLI Reference

## Roadmap

- [ ] Complete test coverage
- [ ] Additional plot styles
- [ ] Support for AC analysis plots

## Ackolagements

- **LTspice**: Circuit simulator by Analog Devices
- **spicelib**: Python library for reading LTspice files
- **matplotlib**: Plotting library
- **matplot2tikz**: Converting matplotlib to TikZ/PGFPlots
