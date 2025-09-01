import matplotlib.pyplot as plt
from txt_parser import parse_ltspice_txt, get_signal_info

def plot_all_singls(filename, output_file=None):
    """
    Create basic plot of all signals 

    Arg: 
        filename (str): Path to to LTspice .txt file 
    """

    simulation_data = parse_ltspice_txt(filename)
    info = get_signal_info(simulation_data)  # Dict containing name of columns
    
    # Plot setup
    plt.rcParams.update({
        "text.usetex": True,
        "font.size": 11,
        "axes.labelsize": 14,
    })

    fig, ax1 = plt.subplots()

    ## TODO: Find out if LTspice allways outputs in 10^0 -- I think pandas does convert in 10^0
    ax1.set_xlabel(r'$t\mathrm{/s}$')
    ax1.set_ylabel(r'$U\mathrm{/V}$')
    ax2 = ax1.twinx()
    ax2.set_ylabel(r'$I\mathrm{/A}$')
    ax1.set_prop_cycle('color', ['b', 'g', 'c', 'm'])
    ax2.set_prop_cycle('color', ['r', 'y', 'k', 'm'])
    
    # Plot all voltages
    for voltage in info['voltage_signals']:
        ax1.plot(simulation_data[info['time_column']], simulation_data[voltage], label=voltage)

    # Plot all currents
    for current in info['current_signals']:
        ax2.plot(simulation_data[info['time_column']], simulation_data[current], label=current)
   
    # Combine the legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')

    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight') 
        print(f"Plot saved to {output_file}")
    else:
        plt.show()
