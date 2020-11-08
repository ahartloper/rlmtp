"""@package plotting
Functions to plot the stress-strain and temperature-time according to the pre-specified figure format.
"""

import os
import numpy as np
import warnings
from .mpl_import import *
from .yield_properties import yield_properties


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


def yield_properties_plotter(data, output_dir, pre_name, f_yn=345.):
    """ Plots the data and the 0.2% offset yield stress point.

    :param pd.DataFrame data: Contains the stress-strain data.
    :param str output_dir: Directory to save the figure.
    :param str pre_name: Name prepended to the generic plot name.
    :param float f_yn: Nominal yield stress.
    :return:
    """
    e_and_fy = yield_properties(data, f_yn)
    offset = 0.002
    projection = 0.005
    x = np.linspace(offset, projection)
    fy_offset_line = e_and_fy[0] * x - offset * e_and_fy[0]
    ey = e_and_fy[1] / e_and_fy[0] + offset

    plt.figure()
    plt.plot(data['e_true'], data['Sigma_true'], '0.7')
    plt.plot(x, fy_offset_line, 'k')
    plt.plot([ey], [e_and_fy[1]], 'ko')

    file_name = pre_name + '_' + 'yield_props_plot.pdf'
    out_path = os.path.join(output_dir, file_name)
    plt.savefig(out_path)
