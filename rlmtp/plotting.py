"""@package plotting
Functions to plot the stress-strain and temperature-time according to the pre-specified figure format.
"""

import os
import numpy as np
import warnings
from .mpl_import import *


def safe_savefig(path):
    """ Saves the figure to path, but raises a warning if the file cannot be overwritten. """
    try:
        plt.savefig(path)
    except PermissionError:
        warnings.warn('Cannot write the file {0}, it''s likely already open!'.format(path))
    return


def stress_strain_plotter(data, output_dir, pre_name):
    """ Plots the true stress versus true strain. """
    file_name = pre_name + '_' + 'stress_strain_plot.pdf'
    out_path = os.path.join(output_dir, file_name)
    plt.figure()
    plt.plot(data['e_true'], data['Sigma_true'], c='0.15', label='Test', lw=0.5)
    plt.xlabel(r'True Strain, $\varepsilon$')
    plt.ylabel(r'True Stress, $\sigma$ [MPa]')
    plt.tight_layout()
    safe_savefig(out_path)
    plt.close()
    return


def strain_rate_plotter(data, output_dir, pre_name):
    """ Plots the strain-rate vs. accumulated strain. """
    if 'C_1_Temps[s]' in data.columns:
        time_name = 'C_1_Temps[s]'
    else:
        time_name = 'Time[s]'
    file_name = pre_name + '_' + 'stress_rate_plot.pdf'
    out_path = os.path.join(output_dir, file_name)
    accum_strain = np.cumsum(np.abs(np.diff(data['e_true'])))
    strain_rate = np.diff(data['e_true']) / np.diff(data[time_name])
    plt.figure()
    plt.plot(accum_strain, strain_rate, c='0.15', label='Test', lw=0.5)
    plt.xlabel(r'Accumulated Strain, $\int |\dot{\varepsilon}| \mathrm{d}t$')
    plt.ylabel(r'Strain Rate, $\dot{\varepsilon}$ [s$^{-1}$]')
    plt.tight_layout()
    safe_savefig(out_path)
    plt.close()
    return


def temp_strain_plotter(data, output_dir, pre_name):
    """ Plots the temperature vs true strain. """
    file_name = pre_name + '_' + 'temperature_strain_plot.pdf'
    out_path = os.path.join(output_dir, file_name)
    plt.figure()
    plt.plot(data['e_true'], data['Temperature[C]'], c='0.15', label='Test', lw=0.5)
    plt.xlabel(r'True Strain, $\varepsilon$')
    plt.ylabel(r'Temperature, $T$ [$^\circ$C]')
    plt.tight_layout()
    safe_savefig(out_path)
    plt.close()
    return


def temp_time_plotter(data, output_dir, pre_name):
    """ Plots the temperature versus time. """
    if 'C_1_Temps[s]' in data.columns:
        time_name = 'C_1_Temps[s]'
    else:
        time_name = 'Time[s]'
    file_name = pre_name + '_' + 'temperature_time_plot.pdf'
    out_path = os.path.join(output_dir, file_name)
    plt.figure()
    plt.plot(data[time_name], data['Temperature[C]'], c='0.15', label='Test', lw=0.5)
    plt.xlabel(r'Time, $t$ [s]')
    plt.ylabel(r'Temperature, $T$ [$^\circ$C]')
    plt.tight_layout()
    safe_savefig(out_path)
    plt.close()
    return
