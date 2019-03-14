"""@package filtering
Functions to filter and reduce the stress-strain data.
"""

import numpy as np
import pandas as pd


def reduce_data(x, y, t, anchors, window, poly_order=1):
    """ Returns the data sampled at particular points between the specified anchor points.

    :param np.array x: Independent data.
    :param np.array y: Dependent data.
    :param np.array t: Time of each independent data measurement.
    :param list anchors: (int) Indices of x,y,t that will be included in the reduced data.
    :param int window: Window length that specifies the maximum number of points between samples.
    :param int poly_order: Polynomial order for the fitting for the y data.
    :return list: (np.array) The reduced data in the form [x_new, y_new, t_new].

    - The first data point is defined by anchors[0], and the last by anchors[-1].
    - Within each anchor interval data is sampled at points defined by the window length following
        x_k = x[anchors[i] + n * window], n = 0, 1, 2, ...
    where n resets at each new anchor interval.
    - One point is added at the mid point of each window based on a best-fit polynomial of order = poly_order.
    """
    x_new = np.array([])
    y_new = np.array([])
    t_new = np.array([])
    at_end = False
    i_current = anchors[0]  # start at the first anchor point
    j_anchor = 1  # specifies the next anchor point
    i_next = i_current + window
    while not at_end:
        # Check if the next point should be at an anchor
        if i_next >= anchors[j_anchor]:
            i_next = anchors[j_anchor]
            if j_anchor < len(anchors) - 1:
                j_anchor += 1
            else:
                # Reached last anchor point
                at_end = True
        # Add one point at the middle between the current and next points
        x_current = x[i_current]
        x_next = x[i_next]
        x_mid = 0.5 * (x_current + x_next)
        # Fit the mid point based on the specified polynomial order
        z = np.polyfit(x[i_current:i_next], y[i_current:i_next], poly_order)
        p = np.poly1d(z)
        y_mid = p(x_mid)
        x_new = np.append(x_new, [x_current, x_mid])
        y_new = np.append(y_new, [y[i_current], y_mid])
        t_mid = 0.5 * (t[i_current] + t[i_next])  # assumes that the rate is constant between the two points
        t_new = np.append(t_new, [t[i_current], t_mid])
        # Update the indices
        i_current = i_next
        i_next = i_current + window
    # Add the last anchor point
    x_new = np.append(x_new, [x[anchors[-1]]])
    y_new = np.append(y_new, [y[anchors[-1]]])
    t_new = np.append(t_new, [t[anchors[-1]]])
    return [x_new, y_new, t_new]


def clean_data(data, filter_info):
    """ Returns the filtered and cleaned data.

    :param pd.DataFrame data: As loaded stress-strain and time data.
    :param dict filter_info: Information from the filter file, see rlmtp.readers.read_filter_info().
    :return pd.DataFrame: Cleaned data.

    Notes:
        - Requires that the columns 'Sigma_true', 'e_true', and 'C_1_Temps[s]' exist in data.
        - Column 'Temperature[C]' is optional
    """
    # Filter the specified columns given the e_true column
    cols_to_include = ['Sigma_true', 'Temperature[C]']
    columns = [c for c in data.columns if c in cols_to_include]
    x = data['e_true']
    t = data['C_1_Temps[s]']
    cleaned_data = pd.DataFrame()
    # Get the info for the filtering
    anchors = filter_info['anchors']
    windows = filter_info['window']
    poly_orders = filter_info['poly_order']
    for i, c in enumerate(columns):
        x_stack = np.array([])
        t_stack = np.array([])
        y_stack = np.array([])
        for j in range(len(windows)):
            # Process each set separately and append the data
            a = anchors[j]
            w = windows[j]
            po = poly_orders[j]
            # Process stress-strain and temperature-strain separately
            y = data[c]
            # If not the first set, add the last anchor point from the previous set to have continuous data
            if j > 0:
                # Prepend last value of previous set
                a = [anchors[j - 1][-1]] + a
            [x_clean, y_clean, t_clean] = reduce_data(x, y, t, a, w, po)
            # For the first column we need to add all the data
            if i == 0:
                if j == 0:
                    # Add all the data in the first set
                    x_stack = np.append(x_stack, x_clean)
                    t_stack = np.append(t_stack, t_clean)
                    y_stack = np.append(y_stack, y_clean)
                else:
                    # Don't add the first data point since it was included in the previous set
                    x_stack = np.append(x_stack, x_clean[1:])
                    t_stack = np.append(t_stack, t_clean[1:])
                    y_stack = np.append(y_stack, y_clean[1:])
            else:
                # After the first column the x and t don't change so just add the y data
                y_stack = np.append(y_stack, y_clean)
        # If first column add all the data to cleaned data
        if i == 0:
            cleaned_data['e_true'] = x_stack
            cleaned_data['C_1_Temps[s]'] = t_stack
            cleaned_data[c] = y_stack
        else:
            # Just add the y data since the x and t are the same
            cleaned_data[c] = y_stack

    print('Data reduced from {0} to {1} data points.'.format(len(x), len(y_stack)))
    return cleaned_data
