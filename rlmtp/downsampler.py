import numpy as np
from scipy.signal import savgol_filter
from find_peaks import find_peaks, find_peaks2
from yield_properties import yield_properties


def rlmtp_downsampler(data, max_dev_tol=0.001, last_ind=None, removal_ranges=[],
                      n_elastic_region=7, apply_filter=True, sat_tol=0.99):
    """ Returns the indices of points to keep.
    :param data pd.DataFrame: Contains the true stress-strain data.
    :param max_dev_tol float: Maximum allowable perpindicular distance between sampled points.
    :param last_ind int: Last index to keep in the data.
    :param removal_ranges list: (list) Each list specifies ranges of indices to remove.
    :param n_elastic_region int: Number of extra points to keep in the initial elastic range.
    :param apply_filter bool: If True, filter the stress data before downsampling.

    Notes:
    ======
        - Uses two downsampling strategies:
            1. Keep the "peaks" of the stress-strain data
            2. Max deviation downsampler to remove points inbetween peaks
        - Can specify where the data should end with last_ind
        - Can specify ranges of indices to remove with removal_ranges as follows:
            - removal_ranges = [[i_0, i_1], [i_2, i_3], ...]
            - Indices i_0, i_1, i_2, i_3, ... are added to the data
            - Any indicies i with i_0 < i < i_1, i_2 < i < i_3, ... will be removed
        - Adds extra data to the initial elastic region to have fidelity in this area
        - If apply_filter=True, a moving average filter is applied to the stress after the
        peaks have been selected, but before the max deviation downsampler is applied. Therefore,
        the peaks of the stress-strain data are maintained and the result is somewhat robust to
        noise in the stress data.
    """
    # Obtain the "peaks" in the stress-strain data
    ind_ss, ind_2prct = stress_strain_peaks(data, last_ind=last_ind)
    print('Last ind: ', ind_ss[-1])

    # Only use cycles up to saturation for constant amplitude tests
    # Constant amplitude if ind_2prct=None many peaks found
    if ind_2prct is None and len(ind_ss) > 55:
        ind_ss = keep_upto_saturation(data, ind_ss, sat_tol=sat_tol)

    # Run max deviation downsampler
    # Remove noise in the stress with a moving average filter
    d = np.array(data[['e_true', 'Sigma_true']])
    if apply_filter:
        d[:, 1] = filter_stress(d, ind_2prct)
    # Scale the x,y to have unit max length in both axes
    d[:, 0] = d[:, 0] / (d[:, 0].max() - d[:, 0].min())
    d[:, 1] = d[:, 1] / (d[:, 1].max() - d[:, 1].min())
    # Only use the data up to the last index from the stress-strain peaks
    d = d[0:ind_ss[-1]+1, :]
    ind_max_dev = max_deviation_downsampler(d, max_dev_tol)

    # Combine the points, remove any points that lie between the removal ranges
    ind_final = ind_ss + ind_max_dev
    for rr in removal_ranges:
        r_start = rr[0]
        r_end = rr[1]
        # Keep the points at the start and end
        ind_final += [r_start, r_end]
        # Remove any points between start and end
        ind_final = [i for i in ind_final if not (r_start < i < r_end)]
    # Remove any duplicates and sort
    ind_final = sorted(list(set(ind_final)))

    # Keep extra points in initial elastic region
    ind_final += add_to_elastic(d, [ind_final[0], ind_final[1]], n_elastic_region)
    # Sort again and return
    ind_final = sorted(list(set(ind_final)))
    return ind_final


def filter_stress(d, ind_2prct, wl_base=5, wl_factor=11, poly_order=1):
    """ Returns the filtered stress using a moving average filter.
    :param d np.array: (n, 2) Stress-strain data.
    :param ind_2prct int: Index for the switch for greater / less than 2 % strain.
    :param wl_base int: Base window-length.
    :param wl_factor int: Multiplier for the window length pre-2% strain.
    :param poly_order int: Interpolation order in the filter.

    Notes:
    ======
        - Different windowlengths are used pre- and post- 2% strain because of the
        different strain rates.
        - The pre-2% is around 26 times slower (26x more points)
        - Suggested to use a factor of 11 for the pre-2% part
        - The poly_order=1 handles noise better, but leads to increased aliasing,
        the aliasing is OK because we keep the peaks with another method
    """
    if ind_2prct is not None:
        # Split data on pre 2% strain, and post 2%
        s1 = d[:ind_2prct, 1]
        s2 = d[ind_2prct:, 1]
        # Filter each
        s1 = savgol_filter(s1, wl_base * wl_factor, poly_order)
        s2 = savgol_filter(s2, wl_base, poly_order)
        # Return combined
        s_final = np.array(list(s1) + list(s2))
    else:
        # Never passed 2%, therefore just use pre-2% for all
        s_final = savgol_filter(d[:, 1], wl_base * wl_factor, poly_order)
    return s_final


def add_to_elastic(d, elastic_ind, n_elastic_region):
    """ Adds indices to the elastic region. """
    e_elastic = d[elastic_ind[0]:elastic_ind[1], 0]
    e_add = np.linspace(e_elastic[0], e_elastic[-1], num=n_elastic_region, endpoint=False)
    additional_ind = []
    for e in e_add:
        additional_ind.append(elastic_ind[0] + int(np.argmin(np.abs(e_elastic - e))))
    return additional_ind


def perp_dist(x, y, z):
    """x, z are endpoints, y is a point on the curve"""
    a = y - x
    a2 = np.dot(a, a)
    b = y - z
    b2 = np.dot(b, b)
    c = z - x
    l2 = np.dot(c, c)
    c = l2**0.5
    return (a2 - ((l2 + a2 - b2) / (2 * c)) ** 2) ** 0.5


def max_dist(pos, n0, n1):
    """ Returns the maximum perpindicular distance between all the points in pos within n0 and n1.
    :param pos np.array: (n, 2) Set of 2-dimensional points.
    :param n0 int: Starting index.
    :param n1 int: Ending index.
    :return float: Maximum perpindicular distance.
    """
    return np.array([perp_dist(pos[n0, :], pos[n2, :], pos[n1, :]) for n2 in range(n0, n1)]).max()


# The mid point method can be used instead of max_dist to be much faster
def mid_dist(pos, n0, n1):
    return perp_dist(pos[n0, :], pos[int((n1 + n0)/2), :], pos[n1, :])


def max_deviation_downsampler(pos, thresh=0.1):
    """ Downsamples pos by removing points within a perpindicular distance of the last point.
    :param pos np.array: (n, 2) Set of 2-dimensional points.
    :param thresh float: Maximum allowable perpindicular distance between sampled points.
    :return list: Indices of points to keep.

    Notes:
    ======
        - The set of 2-dimensional points should have the same scale in both axes
        - Keeps the first point
        - Later points are kept if the perpindicular distance between points are outside of "thresh"
        - Keeps more points in regions of higher curvature, and less otherwise

    References:
    ===========
        - https://kaushikghose.wordpress.com/2017/11/25/adaptively-downsampling-a-curve/
        - https://github.com/kghose/groho/blob/stable/docs/dev/adaptive-display-points.ipynb
    """
    adaptive_ind = [0]
    last_n = 0
    for n in range(1, pos.shape[0]):
        if max_dist(pos, last_n, n) > thresh:
            adaptive_ind.append(n - 1)
            last_n = n - 1
    return adaptive_ind


def stress_strain_peaks(d, last_ind=None):
    """ Extracted from rlmtp.auto_filter_file.py """
    # Get the stress peaks
    i = find_peaks(d['Sigma_true'])
    # Get the strain peak of the first cycle
    i2 = find_peaks2(d['e_true'], d['Sigma_true'])
    i2 = i2[0]
    # Get the upper yield point -> maximum stress up-to 0.2% offset point
    em, fym = yield_properties(d)
    fy_limit = 0.2 / 100. + fym / em
    i_plateau = d[d['e_true'].gt(fy_limit)].index[0]
    i_fyupper = int(d['Sigma_true'].loc[:i_plateau].idxmax())
    # Locate the points crossing 2% strain amplitude
    # Use a bit extra past the point
    amp_limit = 0.02 * 1.025
    iamp = d[d['e_true'].gt(amp_limit)]
    # Find the point before 12.5%
    amp_limit = 0.125 / 1.02
    ilast = d[d['e_true'].gt(amp_limit)]
    if len(iamp) > 0:
        passes_2prct = True
        iamp = iamp.index[0]
        i_final = [0] + i + [i2, i_fyupper, int(iamp)]
    else:
        passes_2prct = False
        iamp = None
        i_final = [0] + i + [i2, i_fyupper]
    # Remove data past 12.5% and remove after the last specified index
    if len(ilast) > 0 or last_ind is not None:
        # Use either the point at 12.5% or the last_ind
        if len(ilast) > 0:
            i_ult = ilast.index[0]
        else:
            i_ult = last_ind
        if last_ind is not None and len(ilast) > 0:
            # Use the specified last index if it is less than the auto determined one
            if last_ind < i_ult:
                i_ult = last_ind
        i_final = [i for i in i_final if i < i_ult]
        i_final.append(i_ult)
    else:
        # Go until the end of the data
        i_final.append(len(d) - 1)
    return i_final, iamp


def downsample_error(d, ind):
    """ Returns the accumulated relative energy error between the original and downsampled data. """
    x = np.array([0.0] + list(np.cumsum(np.abs(np.diff(d[:ind[-1] + 1, 0])))))
    y = d[:ind[-1] + 1, 1]
    xi = x[ind]
    yi = y[ind]
    y2 = np.interp(x, xi, yi)
    e1 = np.trapz(y**2, x=x)
    return np.sqrt(np.trapz((y - y2)**2, x=x) / e1)


def keep_upto_saturation(data, ind_ss, sat_tol, n_cycles_min=10, extra_pts=5):
    """ Removes indices past the saturation index. """
    # Number of cycles is (num peaks - extra_pts) / 2
    # Extra points may vary from test to test, but hopefully not...
    sat_ind = find_saturation_index(data, sat_tol)
    cycles_to_sat = int(next(i for i, v in enumerate(ind_ss) if v > sat_ind) - extra_pts) // 2
    if cycles_to_sat < n_cycles_min:
        cycles_to_sat = n_cycles_min
        # Ensure minimum number of cycles
        if int(n_cycles_min * 2 + extra_pts) < len(ind_ss):
            sat_ind = ind_ss[int(n_cycles_min * 2 + extra_pts)]
        else:
            sat_ind = ind_ss[-1]
    # Only keep indicies less than saturation
    ind_ss = [i for i in ind_ss if i <= sat_ind]
    print('Kept {0} cycles to reach saturation.'.format(cycles_to_sat))
    return ind_ss


def find_saturation_index(d, sat_tol=0.99):
    """ Returns the index of the first instance that reaches saturation.

    Saturation is defined by sat_tol and must be satisfied in both positive and negative
    loading directions.
    """
    # Check the positive loading direction
    s_max = d['Sigma_true'].max()
    i_sat1 = d[d['Sigma_true'].gt(sat_tol * s_max)].index[0]
    # Check the negative loading direction
    s_min = d['Sigma_true'].min()
    i_sat2 = d[d['Sigma_true'].lt(sat_tol * s_min)].index[0]
    # Take the max of both directions
    i_sat = int(max(i_sat1, i_sat2))
    return i_sat
