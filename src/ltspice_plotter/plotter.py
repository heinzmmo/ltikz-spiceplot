import matplotlib.pyplot as plt
from .txt_parser import get_signal_info

def plot_all_singls(simulation_data, fig_title=None, output_file=None):
    """
    Create basic plot of all signals 

    Arg: 
        simulation_data (pd.DataFrame): Simulation data
        fig_title (str): Figure title
        output_file (str): Output file name (including data type)
    """

    info = get_signal_info(simulation_data)  # Dict containing name of columns

    # Check whats signals we have
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
    ax1.set_xlabel(r'$t\mathrm{/s}$')

    if has_voltage:
        ax1.set_ylabel(r'$U\mathrm{/V}$')

        ax1.set_prop_cycle('color', ['b', 'g', 'c', 'm'])
        # Plot all voltages
        for voltage in info['voltage_signals']:
            ax1.plot(simulation_data[info['time_column']], simulation_data[voltage], label=voltage)


    if has_current:
        if has_voltage:
            ax2 = ax1.twinx() # Seconardy y-axis only if data has voltage and current signals
            current_axis = ax2
        else:
            current_axis = ax1
    
        current_axis.set_ylabel(r'$I\mathrm{/A}$')
        current_axis.set_prop_cycle('color', ['r', 'y', 'k', 'm'])
        # Plot all currents
        for current in info['current_signals']:
            current_axis.plot(simulation_data[info['time_column']], simulation_data[current], label=current)

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

    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight') 
        print(f"Plot saved to {output_file}")
    else:
        plt.show()
