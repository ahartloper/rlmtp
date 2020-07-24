"""@package yield_properties
Functions to obtain the measured elastic modulus and yield stress.q
"""

from __future__ import division
import numpy as np
import pandas as pd


def interx1(curve1, curve2):
    """ Computes the first intersection between two curves in 2D.
    :param np.ndarray curve1: (2, n1) x and y coordinates for curve 1.
    :param np.ndarray curve2: (2, n2) x and y coordinates for curve 2.
    :return np.ndarray: (2, n3) x and y coordinates of the intersection points.

    Notes:
    ======
    - This is a modified Python implementation of the Matlab function InterX, see the NS (2020) reference below.
    - The original function is modified to only return the first intersection.

    References:
    ===========
    NS (2020). Curve intersections (https://www.mathworks.com/matlabcentral/fileexchange/22441-curve-intersections),
    MATLAB Central File Exchange. Retrieved July 24, 2020.
    """

    def dfun(x, y):
        """ ?? """
        try:
            u = (x[:, :-1] - y) * (x[:, 1:] - y)
        except ValueError:
            yt = y[:, np.newaxis]
            u = (x[:, :-1] - yt) * (x[:, 1:] - yt)
        return u

    # Treat x1, y1 as column vectors
    x1 = curve1[0, :]
    y1 = curve1[1, :]
    dx1 = np.diff(x1)
    dy1 = np.diff(y1)
    s1 = dx1 * y1[:-1] - dy1 * x1[:-1]
    # Treat x2, y2 as row vectors
    x2 = curve2[0, :]
    y2 = curve2[1, :]
    dx2 = np.diff(x2)
    dy2 = np.diff(y2)
    s2 = dx2 * y2[:-1] - dy2 * x2[:-1]

    # Find the intersection points
    p1 = np.outer(dx1, y2) - np.outer(dy1, x2)
    d1 = dfun(p1, s1)
    p2 = (np.outer(y1, dx2) - np.outer(x1, dy2)).transpose()
    d2 = dfun(p2, s2).transpose()
    c = np.nonzero(np.logical_and(d1 <= 0, d2 <= 0))

    # Clean-up and interpolate
    i = c[0]
    j = c[1]
    # Select only the first intersection
    i = np.array(i[0])
    j = np.array(j[0])
    ell = dy2[j] * dx1[i] - dy1[i] * dx2[j]
    i = i[ell != 0]
    j = j[ell != 0]
    ell = ell[ell != 0]
    p = np.column_stack((dx2[j] * s1[i] - dx1[i] * s2[j], dy2[j] * s1[i] - dy1[i] * s2[j])) \
        / np.column_stack((ell, ell))

    return p


def compute_modulus(e, s, a=0.66, f_yn=345.):
    """ Returns the elastic modulus from the stress-strain data based on the interval [0, a * f_yn].

    :param np.ndarray e: (n, ) Strain data
    :param np.ndarray s: (n, ) Stress data
    :param float a: Ratio of the nominal yield stress for the upper bound
    :param float f_yn: Nominal yield stress
    :return float: Elastic modulus
    """

    # Consider the data up to 2/3 of f_yn
    s_abs = np.abs(s)
    i_limit = len(s_abs) - 1
    for i, si in enumerate(s_abs):
        if si > a * f_yn:
            i_limit = i - 1
            break
    # Linear fit based on the data up-to i_limit, modulus is first value
    pf = np.polyfit(e[:i_limit], s[:i_limit], 1)
    return pf[0]


def yield_properties(data, f_yn=345.):
    """ Returns the measured elastic modulus and yield stress from the data.

    :param pd.DataFrame data: Contains the true stress strain data.
    :param float f_yn: Nominal yield stress.
    :return list: [E_m, f_ym] Measured elastic modulus and yield stress values.

    Notes:
    ======
    - Only data upto 0.66 * f_yn is considered in the calculation of the elastic modulus.
    - Uses the 0.2% offset method to compute the yield stress.
    - The yield point is assumed to occur at less than 0.7%.
    """
    # Compute the elastic modulus
    x1 = data['e_true']
    y1 = data['Sigma_true']
    elastic_modulus = compute_modulus(x1, y1, f_yn=f_yn)

    # Compute the intersection with the 0.2% offset line
    offset = 0.002
    strain_projection = 0.005
    x2 = np.linspace(offset, offset + strain_projection)
    y2 = elastic_modulus * x2 - offset * elastic_modulus
    # Use the absolute value to be valid for initial loading in tension or compression
    c1 = np.row_stack((np.abs(x1), np.abs(y1)))
    c2 = np.row_stack((x2, y2))
    pts = interx1(c1, c2)
    yield_stress = pts[0, 1]
    return [elastic_modulus, yield_stress]
