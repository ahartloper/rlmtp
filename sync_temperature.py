import datetime
import numpy as np
import matplotlib.pyplot as plt


def sync_temperature(dion_data, catman_data):
    # Get the times in seconds since epoch
    system_time_dion = dion_data.data['System Date']
    system_time_dion = np.array(get_epoch_time(system_time_dion))
    system_time_catman = catman_data.data['System Date']
    system_time_catman = np.array(get_epoch_time(system_time_catman))
    # Notify user if the dion times are outside the catman times
    if system_time_dion[0] < system_time_catman[0]:
        print('Warning: Dion7 first time is before catman first time')
    if system_time_dion[-1] > system_time_catman[-1]:
        print('Warning: Dion7 last time is after catman last time')
    # Interpolate the temperature values from catman onto the dion times
    catman_temperature = np.array(catman_data.data['Temperature[C]'], dtype=float)
    dion_temperature = np.interp(system_time_dion, system_time_catman, catman_temperature)
    synced_data = dion_data.data.copy()
    synced_data['Temperature[C]'] = dion_temperature

    # Used to output the debug figure
    # debugging = True
    # if debugging is True:
    #     plt.figure()
    #     plt.plot(system_time_catman, catman_data.data['Temperature[C]'], lw=1.5, label='Original')
    #     plt.plot(system_time_dion, synced_data['Temperature[C]'], lw=1.0, label='Interpolated')
    #     plt.xlabel('Time since epoch [s]')
    #     plt.ylabel('Temperature [C]')
    #     plt.legend()
    #     plt.savefig('../output/temperature_interp_fig.pdf')
    #     plt.close()

    return synced_data


def get_epoch_time(time_series):
    """ Returns a list of floats with the time in seconds since epoch for each entry in time_series. """
    epoch = datetime.datetime.utcfromtimestamp(0)
    new_time = []
    for i in range(len(time_series)):
        new_time.append((time_series[i].to_pydatetime() - epoch).total_seconds())
    return new_time
