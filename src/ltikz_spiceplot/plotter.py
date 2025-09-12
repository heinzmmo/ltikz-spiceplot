import matplotlib.pyplot as plt
from .parser import (
    get_signal_info,
    get_all_voltage_data,
    get_all_current_data
)
from .utils import (
    signal_name_tex,
    auto_scale,
    create_latex_preamble
)

def figure_show(fig):
    cf = fig
    plt.show()


def figure_export(fig, output_arg):
    _validate_output_format(output_arg)

    if output_arg.lower().endswith('.tex'):
        import matplot2tikz
        matplot2tikz.save(output_arg, figure=fig)
        preamble_file = create_latex_preamble(output_arg) 
        print(f"Plot saved to: {output_arg}")
        print(f"Preamble saved to: {preamble_file}")
    else:
        fig.savefig(output_arg, dpi=300, bbox_inches='tight') 
        print(f"Plot saved to {output_arg}")


def figure_create(simulation_data, legend_pos_arg, fig_title_arg):
    """
    Create basic plot of all signals 

    Args: 
        simulation_data (pd.DataFrame): Simulation data
        legend_pos_arg (str): Legends position - default: 'best'
        fig_title_arg (str): Figure title

    Return:
        plt.figure(): Figure containing plots        
    """

    info = get_signal_info(simulation_data)  # Dict containing name of columns
    # Check which signal types are present
    has_voltage = len(info['voltage_signals']) > 0
    has_current = len(info['current_signals']) > 0
    # Plot setup
    plt.rcParams.update({
        "text.usetex": True,
        "font.size": 11,
        "axes.labelsize": 14,
    })
    fig, ax1 = plt.subplots()
    ax2 = None

    # Time
    time_unit_tex, time_scaling_factor = auto_scale(
                           simulation_data[info['time_column']], r'\mathrm{s}')
    scaled_time = simulation_data[info['time_column']] / time_scaling_factor
    ax1.set_xlabel(rf'$t/{time_unit_tex}$')

    # Voltage signals
    if has_voltage:
        voltage_unit_tex, voltage_scaling_factor = auto_scale(
                          get_all_voltage_data(simulation_data), r'\mathrm{V}') 
        ax1.set_ylabel(rf'$U/{voltage_unit_tex}$')
        ax1.set_prop_cycle('color', ['b', 'g', 'c', 'm'])
        # Plot all voltages
        for voltage in info['voltage_signals']:
            scaled_voltage = simulation_data[voltage] / voltage_scaling_factor
            ax1.plot(scaled_time, scaled_voltage,
                     label=rf'{signal_name_tex(voltage)}')

    # Current signals
    if has_current:
        current_unit_tex, current_scaling_factor = auto_scale(
                          get_all_current_data(simulation_data), r'\mathrm{A}')
        # Seconardy y-axis only if data has voltage and current signals
        if has_voltage:
            ax2 = ax1.twinx() 
            current_axis = ax2
        else:
            current_axis = ax1

        current_axis.set_ylabel(rf'$I/{current_unit_tex}$')
        current_axis.set_prop_cycle('color', ['r', 'y', 'k', 'm'])
        # Plot all current signals
        for current in info['current_signals']:
            scaled_current = simulation_data[current] / current_scaling_factor
            current_axis.plot(scaled_time, scaled_current,
                              label=rf'{signal_name_tex(current)}')

    # Legend
    if has_voltage and has_current and ax2 is not None:
        # Combine the legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc=legend_pos_arg)
    elif has_voltage or has_current: 
        ax1.legend(loc=legend_pos_arg)

    # Figure titel
    if fig_title_arg:
        ax1.set_title(label=rf'{fig_title_arg}')

    return fig


def _validate_output_format(output_arg:str):
    supported_output_formats = ('.pdf', '.jpg', '.jpeg', '.png', '.tex')

    if not output_arg.lower().endswith(supported_output_formats):
        msg = f"Unsupported format. Use: {', '.join(supported_output_formats)}"
        raise ValueError(msg)
