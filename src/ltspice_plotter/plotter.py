import matplotlib.pyplot as plt
from .parser import get_signal_info, get_all_voltage_data, get_all_current_data
from .utils import signal_name_tex, auto_scale, create_latex_preamble

def plot_all_signals(simulation_data, fig_title=None, output_file=None):
    """
    Create basic plot of all signals 

    Arg: 
        simulation_data (pd.DataFrame): Simulation data
        fig_title (str): Figure title
        output_file (str): Output file name (including data type)
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
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')
    elif has_voltage or has_current: 
        ax1.legend(loc='best')

    # Figure titel
    if fig_title:
        ax1.set_title(label=rf'{fig_title}')

    # Output either as file (if output_file is given) or just show plot
    if output_file:
        if output_file.lower().endswith('.tex'):
            import matplot2tikz
            matplot2tikz.save(output_file)
            preamble_file = create_latex_preamble(output_file) 
            print(f"Plot saved to: {output_file}")
            print(f"Preamble saved to: {preamble_file}")

        else:
            plt.savefig(output_file, dpi=300, bbox_inches='tight') 
            print(f"Plot saved to {output_file}")
    else:
        plt.show()
