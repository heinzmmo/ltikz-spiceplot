import numpy as np
import matplotlib.pyplot as plt
import importlib.resources as pkg_resources
import ltikz_spiceplot.plot_styles

from pathlib import Path
from itertools import cycle

from .parser import (
    get_signal_info,
    get_all_voltage_data,
    get_all_current_data
)
from .utils import (
    signal_name_tex,
    auto_scale,
    create_latex_preamble,
    tranform_secondary_axis_data
)

def figure_show(fig):
    cf = fig
    plt.show()


def figure_export(fig, output_arg):
    """
    Export figure

    Args:
        fig (plt.figure()): Figure to export
        output_arg (str): Output file, including filename extension

    Return:
        None
    """
    _validate_output_format(output_arg)

    if output_arg.lower().endswith('.tex'):
        import matplot2tikz
        output_file = Path(output_arg)
        tikz_code_raw = matplot2tikz.get_tikz_code(figure=fig)
        # Remove tex code that producess arrow on seconadry axis
        tikz_code = tikz_code_raw.replace(
        r"""\begin{axis}[
axis y line=right,""", r"\begin{axis}[")

        with open(output_file, 'w') as f:
            f.write(tikz_code)
        preamble_file = create_latex_preamble(output_arg)
        print(f"Plot saved to: {output_arg}")
        print(f"Preamble saved to: {preamble_file}")
    else:
        fig.savefig(output_arg, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_arg}")


def figure_create(simulation_data,
                  legend_pos_arg,
                  fig_title_arg,
                  grid_arg,
                  style_arg):
    """
    Create basic plot of all signals

    Args:
        simulation_data (pd.DataFrame): Simulation data
        legend_pos_arg (str): Legends position - default: 'best'
        fig_title_arg (str): Figure title
        style_arg (str): Plot style

    Return:
        plt.figure(): Figure containing plots
    """
    info = get_signal_info(simulation_data)
    has_voltage = len(info['voltage_signals']) > 0
    has_current = len(info['current_signals']) > 0

    v_colors, v_linestyles, i_colors, i_linestyles = _apply_plot_style(style_arg)

    fig, ax1 = plt.subplots()
    ax2 = None
    voltage_ylims = None
    current_ylims = None

    # Time -------------------------------------------------------------------
    time_unit_tex, time_scaling_factor = auto_scale(
                           simulation_data[info['time_column']], r'\mathrm{s}')
    scaled_time = simulation_data[info['time_column']] / time_scaling_factor
    if style_arg in ['de', 'de_bw']:
        ax1.set_xlabel(rf'$t/{time_unit_tex}$')
    elif style_arg in ['ieee', 'ieee_bw']:
        ax1.set_xlabel(rf'Time (${time_unit_tex}$)')

    # Voltage signals --------------------------------------------------------
    if has_voltage:
        voltage_unit_tex, voltage_scaling_factor = auto_scale(
                          get_all_voltage_data(simulation_data), r'\mathrm{V}')
        voltage_ylims = _calc_ylims(np.concatenate([simulation_data[v] / voltage_scaling_factor
                                     for v in info['voltage_signals']]))
        ax1.set_ylim(voltage_ylims)

        if style_arg in ['de', 'de_bw']:
            ax1.set_ylabel(rf'$U/{voltage_unit_tex}$')
        elif style_arg in ['ieee', 'ieee_bw']:
            ax1.set_ylabel(rf'Voltage (${voltage_unit_tex}$)')

        # Plot all voltage signals
        for voltage in info['voltage_signals']:
            scaled_voltage = simulation_data[voltage] / voltage_scaling_factor
            ax1.plot(scaled_time,
                     scaled_voltage,
                     color=next(v_colors),
                     linestyle=next(v_linestyles),
                     label=rf'{signal_name_tex(voltage, style_arg)}')

    # Current signals --------------------------------------------------------
    if has_current:
        current_unit_tex, current_scaling_factor = auto_scale(
                          get_all_current_data(simulation_data), r'\mathrm{A}')
        current_ylims = _calc_ylims(np.concatenate([simulation_data[i] / current_scaling_factor
                                     for i in info['current_signals']]))

        if has_voltage:
            # Current and voltage signal
            # Secondary axis only for ticks and label
            ax2 = ax1.twinx()
            ax2.set_ylim(current_ylims)

            if style_arg in ['de', 'de_bw']:
                ax2.set_ylabel(rf'$I/{current_unit_tex}$')
            elif style_arg in ['ieee', 'ieee_bw']:
                ax2.set_ylabel(rf'Current (${current_unit_tex}$)')

            # Plot all current signals
            for current in info['current_signals']:
                scaled_current = simulation_data[current] / current_scaling_factor
                transformed_current = tranform_secondary_axis_data(scaled_current,
                                                               current_ylims,
                                                               voltage_ylims)
                ax1.plot(scaled_time,
                         transformed_current,
                         color=next(i_colors),
                         linestyle=next(i_linestyles),
                         label=rf'{signal_name_tex(current, style_arg)}')
        # Only current
        else:
            ax1.set_ylim(current_ylims)

            if style_arg in ['de', 'de_bw']:
                ax1.set_ylabel(rf'$I/{current_unit_tex}$')
            elif style_arg in ['ieee', 'ieee_bw']:
                ax1.set_ylabel(rf'Current (${current_unit_tex}$)')

            # Plot all current signals
            for current in info['current_signals']:
                scaled_current = simulation_data[current] / current_scaling_factor
                ax1.plot(scaled_time,
                         scaled_current,
                         color=next(i_colors),
                         linestyle=next(i_linestyles),
                         label=rf'{signal_name_tex(current, style_arg)}')

    # Legend
    ax1.legend(loc=legend_pos_arg)

    # Figure titel
    if fig_title_arg:
        ax1.set_title(label=rf'{fig_title_arg}')

    # Grid
    if grid_arg:
        ax1.grid(True, linewidth=0.5)

    return fig


def _validate_output_format(output_arg:str):
    supported_output_formats = ('.pdf', '.jpg', '.jpeg', '.png', '.tex')

    if not output_arg.lower().endswith(supported_output_formats):
        msg = f"Unsupported format. Use: {', '.join(supported_output_formats)}"
        raise ValueError(msg)


def _apply_plot_style(style:str):
    """
    Apply plot style and return their color and linestyle cycles

    Arg:
        style (str): style name without format (.mplstyle)

    Return:
        tuple: Voltage and current color and linestyle cycles
    """
    if style in ['ieee', 'de']:
        voltage_colors = cycle(['#000000', '#0021F3', '#009E73', '#9467BD'])
        current_colors = cycle(['#C10001', '#FF7F0E', '#F0E442', '#7F7F7F'])
        voltage_linestyles = cycle(['-'])
        current_linestyles = cycle(['-'])
    elif style in ['ieee_bw', 'de_bw']:
        voltage_colors = cycle(['#000000'])
        current_colors = cycle(['#000000'])
        voltage_linestyles = cycle(['-', '--', '-.', ':'])
        current_linestyles = cycle([':', '-.', '--', '-'])
    else:
        msg = "Invalid style"
        raise ValueError(msg)

    # Apply style
    with pkg_resources.path(ltikz_spiceplot.plot_styles,
                            f"{style}.mplstyle") as style_path:
            plt.style.use(style_path)

    return voltage_colors, voltage_linestyles, current_colors, current_linestyles


def _calc_ylims(axis_data):
    """
    Calculate y-limits with 5% margin

    Arg:
        axis_data (np.array): Array containing all data from axis (voltage or
                              current)
    """
    max_abs = abs(max(axis_data, key=abs))
    max_value = axis_data.max()
    min_value = axis_data.min()

    if min_value < 0:
        upper_lim = max_value + 2 * (max_abs * 0.05)
        lower_lim = min_value - 2 * (max_abs * 0.05)
    else:
        upper_lim = max_value + (max_abs * 0.05)
        lower_lim = min_value - (max_abs * 0.05)

    return (lower_lim, upper_lim)

