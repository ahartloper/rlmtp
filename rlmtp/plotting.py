import os
import matplotlib.pyplot as plt


def stress_strain_plotter(data, output_dir):
    """ Plots the true stress versus true strain. """
    file_name = 'stress_strain_plot.pdf'
    out_path = os.path.join(output_dir, file_name)
    plt.figure()
    plt.plot(data['e_true'], data['Sigma_true'], c='k', label='Test', lw=1.0)
    plt.xlabel(r'True Strain, $\varepsilon$')
    plt.ylabel(r'True Stress, $\sigma$ [MPa]')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return


def temp_strain_plotter(data, output_dir):
    """ Plots the temperature vs true strain. """
    file_name = 'temperature_strain_plot.pdf'
    out_path = os.path.join(output_dir, file_name)
    plt.figure()
    plt.plot(data['e_true'], data['Temperature[C]'], c='k', label='Test', lw=1.0)
    plt.xlabel(r'True Strain, $\varepsilon$')
    plt.ylabel(r'Temperature, $T$ [$^\circ$C]')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return


def temp_time_plotter(data, output_dir):
    """ Plots the temperature versus time. """
    file_name = 'temperature_time_plot.pdf'
    out_path = os.path.join(output_dir, file_name)
    plt.figure()
    plt.plot(data['C_1_Temps[s]'], data['Temperature[C]'], c='k', label='Test', lw=1.0)
    plt.xlabel(r'Time, t [s]')
    plt.ylabel(r'Temperature, $T$ [$^\circ$C]')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return
