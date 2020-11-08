"""@package find_peaks
Functions to find peaks in cyclic data.
"""


def find_peaks(x):
    """ Gets the 'peaks' in each cycle of the data x.
    :param pd.Series x: Data to search for peaks.
    :return list: [int] Indicies of the peaks in x.
    """

    current_max = 0.
    max_ind = 0
    current_min = 0.
    min_ind = 0
    if x[x.index[0]] > 0.:
        is_positive = True
    else:
        is_positive = False
    peaks = []
    # Keep track of the min/max and after cross-axis then add the min/max as a peak
    for i, xi in x.items():
        if xi > 0.:
            if not is_positive:
                peaks.append(min_ind)
                is_positive = True
                current_min = 0.
            if xi > current_max:
                current_max = xi
                max_ind = i
        else:
            if is_positive:
                peaks.append(max_ind)
                is_positive = False
                current_max = 0.
            if xi < current_min:
                current_min = xi
                min_ind = i
    # Add the last peak + the last point
    if current_min == 0.:
        peaks.append(max_ind)
    else:
        peaks.append(min_ind)
    peaks.append(len(x) - 1)
    return peaks


def find_peaks2(x, y):
    """ Gets the 'peaks' in each cycle of the data x with cycles defined by y.
    :param pd.Series x: Data to search for peaks.
    :param pd.Series y: Data to define cycles.
    :return list: [int] Indicies of the peaks in x.
    """

    current_max = 0.
    max_ind = 0
    current_min = 0.
    min_ind = 0
    if y[y.index[0]] > 0.:
        is_positive = True
    else:
        is_positive = False
    peaks = []
    # Keep track of the min/max and after cross-axis then add the min/max as a peak
    for i, xi in x.items():
        yi = y.loc[i]
        if yi > 0.:
            if not is_positive:
                peaks.append(min_ind)
                is_positive = True
                current_min = 0.
                current_max = xi
            if xi > current_max:
                current_max = xi
                max_ind = i
        else:
            if is_positive:
                peaks.append(max_ind)
                is_positive = False
                current_max = 0.
                current_min = xi
            if xi < current_min:
                current_min = xi
                min_ind = i
    # Add the last peak + the last point
    if current_min == 0.:
        peaks.append(max_ind)
    else:
        peaks.append(min_ind)
    peaks.append(len(x) - 1)
    return peaks
