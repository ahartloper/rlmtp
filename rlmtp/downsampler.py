"""@package downsampler
Function to downsample stress-strain data.
"""
import numpy as np
from numpy.lib.polynomial import poly
from scipy.signal import savgol_filter
import polyprox
from .find_peaks import find_peaks, find_peaks2
from .yield_properties import yield_properties


def downsample_data(data, params):
    """ Returns the downsampled data.
    :param data pd.DataFrame: Stress-strain, time, and (optional) temperature data.
    :param params dict: Parameters for `rlmtp_downsampler`.
    :return pd.DataFrame: Downsampled stress-strain, time, and (temperature if provided).
    """
    ind = rlmtp_downsampler(data, **params)
    cols_to_include = ['C_1_Temps[s]', 'e_true', 'Sigma_true']
    temperature_col = 'Temperature[C]'
    if temperature_col in data.columns:
        cols_to_include += [temperature_col]
    return data[cols_to_include].loc[ind]


def rlmtp_downsampler(data, use_local_error=True, downsample_tol=0.001, last_ind=None, removal_ranges=[],
                      n_elastic_region=7, apply_filter=True, wl_base_factor=5, wl_2prct_factor=11,
                      sat_tol=0.99, n_cycles_min=20, f_yn=345.0):
    """ Returns the indices of data to keep.
    :param data pd.DataFrame: Contains the true stress-strain data.
    :param use_local_error bool: If True, then downsample_tol is applied to the local criteria.
                                 If False, then applied to the global criteria.
    :param downsample_tol float: Maximum allowable perpindicular distance between sampled points.
    :param last_ind int: Last index to keep in the data.
    :param removal_ranges list: (list) Each list specifies ranges of indices to remove.
    :param n_elastic_region int: Number of extra points to keep in the initial elastic range.
    :param apply_filter bool: If True, filter the stress data before downsampling.
    :param wl_base_factor int: Windowlength for the stress filter after 2% strain.
    :param wl_2prct_factor int: Windowlength multiplier for the stress filter before 2% strain.
    :param sat_tol float: Proportion of maximum stress to consider saturated under constant amplitude loading.
                          0.0 < sat_tol <= 1.0. Set sat_tol=None to disable cycle cutting.
    :param n_cycles_min int: Minimum number of cycles to use in constant amplitude tests.
                             Only applies if sat_tol is not None.
    :param f_yn float: Nominal yield stress.
    :return list: Indices in data to keep.

    Notes:
    ======
        - Uses two downsampling strategies:
            1. Keep the "peaks" of the stress-strain data
            2. Ramer–Douglas–Peucker (RDP) algorithm to remove points inbetween peaks
        - Can specify where the data should end with last_ind
        - Can specify ranges of indices to remove with removal_ranges as follows:
            - removal_ranges = [[i_0, i_1], [i_2, i_3], ...]
            - Indices i_0, i_1, i_2, i_3, ... are added to the data
            - Any indicies i with i_0 < i < i_1, i_2 < i < i_3, ... will be removed
        - The local criteria uses downsample_tol as the local epsilon.
        - The global criteria iterates the local epsilon until the global criteria on all the sampled
          data and the original data is satisfied.
        - Adds extra data to the initial elastic region to have fidelity in this area
        - If apply_filter=True, a moving average filter is applied to the stress after the
        peaks have been selected, but before the RDP downsampler is applied. Therefore,
        the peaks of the stress-strain data are maintained and the result is somewhat robust to
        noise in the stress data. See rlmtp.downsampler.filter_stress for details on the stresss filter.
        - wl_base_factor and wl_2prct_factor are parameters of the stress filter.
        - Cycle cutting with sat_tol takes cycles up to and including when stress > sat_tol*max(stress)
          and stress < sat_tol*min(stress). This assumes a cyclic hardening behavior and should be
          disabled for cycling softening by using sat_tol=None.
    """
    # Obtain the "peaks" in the stress-strain data
    ind_ss, ind_2prct = stress_strain_peaks(data, last_ind=last_ind, f_yn=f_yn)
    # Remove any duplicates and sort
    ind_ss = sorted(list(set(ind_ss)))

    # Only use cycles up to saturation for constant amplitude tests
    # Constant amplitude if ind_2prct=None and many peaks found
    large_num_cycles = 55
    if ind_2prct is None and len(ind_ss) > large_num_cycles and sat_tol is not None:
        ind_ss = keep_upto_saturation(data, ind_ss, sat_tol=sat_tol, n_cycles_min=n_cycles_min)

    # Run max deviation downsampler
    # Remove noise in the stress with a moving average filter
    d = np.array(data[['e_true', 'Sigma_true']])
    if apply_filter:
        d[:, 1] = filter_stress(d, ind_2prct, wl_base=wl_base_factor, wl_factor=wl_2prct_factor)
    if use_local_error:
        ind_downsampler = apply_downsampler(d, ind_ss[-1], downsample_tol)
    else:
        ind_downsampler = downsample_loop(d, ind_ss[-1], downsample_tol)

    # Combine the points, remove any points that lie between the removal ranges
    ind_final = ind_ss + ind_downsampler
    ind_final = apply_removal_ranges(ind_final, removal_ranges)
    ind_final = sorted(list(set(ind_final)))

    # Keep extra points in initial elastic region
    ind_final += add_to_elastic(d, [ind_ss[0], ind_ss[1]], n_elastic_region)
    # Sort again and return
    ind_final = sorted(list(set(ind_final)))
    return ind_final


def scale_data(d):
    """ Scale the x,y to have unit max length in both axes. """
    d[:, 0] = d[:, 0] / (d[:, 0].max() - d[:, 0].min())
    d[:, 1] = d[:, 1] / (d[:, 1].max() - d[:, 1].min())
    return d


def apply_downsampler(d, last_ind, tol):
    """ Returns the indices to keep in d.
    :param d np.array: x-y data.
    :param last_ind int: Only considers d[0:last_ind+1].
    :param tol float: Threshold to use in the downsampler.
    :return list: Indices to keep.
    """
    d = scale_data(d)
    # Only use the data up to the last index from the stress-strain peaks
    d = d[0:last_ind+1, :]
    # ind_ds = max_deviation_downsampler(d, tol)
    ind_ds = list(polyprox.min_num(d, epsilon=tol, return_index=True))
    return ind_ds


def apply_removal_ranges(ind_final, removal_ranges):
    """ Removes any points contained in any of the removal ranges. """
    for rr in removal_ranges:
        r_start = rr[0]
        r_end = rr[1]
        # Keep the points at the start and end
        ind_final += [r_start, r_end]
        # Remove any points between start and end
        ind_final = [i for i in ind_final if not (r_start < i < r_end)]
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
    small_vall = 1.e-14
    a = y - x
    a2 = np.dot(a, a)
    b = y - z
    b2 = np.dot(b, b)
    c = z - x
    l2 = np.dot(c, c)
    c = l2**0.5
    return (a2 - ((l2 + a2 - b2) / (2 * c + small_vall)) ** 2) ** 0.5


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
    """ Returns the perpindicular distance at the index approx. halfway between n0 and n1. """
    return perp_dist(pos[n0, :], pos[int((n1 + n0) / 2), :], pos[n1, :])


def max_deviation_downsampler(pos, thresh=0.001, use_midpoint_method=False):
    """ Downsamples pos by removing points within a perpindicular distance of the last point.
    :param pos np.array: (n, 2) Set of 2-dimensional points.
    :param thresh float: Maximum allowable perpindicular distance between sampled points.
    :param ues_midpoint_method bool: If True, use the midpoint distance instead of max distance.
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
    # Metric to use in the deviation distance
    if use_midpoint_method:
        dist_fun = mid_dist
    else:
        dist_fun = max_dist

    adaptive_ind = [0]
    last_n = 0
    for n in range(1, pos.shape[0]):
        if dist_fun(pos, last_n, n) > thresh:
            adaptive_ind.append(n - 1)
            last_n = n - 1
    return adaptive_ind


def stress_strain_peaks(d, last_ind=None, f_yn=345.0):
    """ Returns the indicies of the initial elastic region and stress-strain peaks.
    :param d pd.DataFrame: Stress-strain data.
    :param last_ind int: Only consider the data d[:last_ind+1].
    :param f_yn float: Nominal yield stress.
    :return list: [i_final, i_2prct]:
        - i_final is a list of the indices
        - i_2prct is an int for the index at which crosses to 2% strain, or None if it doesn't cross

    Notes:
    ======
        - Extracted from rlmtp.auto_filter_file.py.
        - Contains the starting point also.
    """
    # Get the stress peaks
    i = find_peaks(d['Sigma_true'])
    # Get the strain peak of the first cycle
    i2 = find_peaks2(d['e_true'], d['Sigma_true'])
    i2 = i2[0]
    # Get the upper yield point -> maximum stress up-to 0.2% offset point
    em, fym = yield_properties(d, f_yn=f_yn)
    fy_limit = 0.2 / 100. + fym / em
    i_plateau = d[d['e_true'].gt(fy_limit)].index[0]
    i_fyupper = int(d['Sigma_true'].loc[:i_plateau].idxmax())
    # Locate the points crossing 2% strain amplitude
    # Use a bit extra past the point
    amp_limit = 0.02 * 1.025
    i_2prct = d[d['e_true'].gt(amp_limit)]
    # Find the point before 12.5%
    amp_limit = 0.125 / 1.02
    ilast = d[d['e_true'].gt(amp_limit)]
    if len(i_2prct) > 0:
        i_2prct = i_2prct.index[0]
        i_final = [0] + i + [i2, i_fyupper, int(i_2prct)]
    else:
        i_2prct = None
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
    return i_final, i_2prct


def downsample_error(d, ind, removal_ranges=[]):
    """ Returns the accumulated relative energy error between the original and downsampled data. """
    # Remove any data in removal ranges so compute correct error
    if len(removal_ranges) > 0:
        remove_ind = []
        remove_ind = [remove_ind + range(r[0]+1, r[1]) for r in removal_ranges]
        d = np.delete(d, remove_ind, axis=0)
    # Compute error
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
    ind_ss = sorted([i for i in ind_ss if i <= sat_ind])
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


def read_downsample_props(fpath):
    """ Parses downsampler_props.txt files.
    :param str fpath: Path to the file.
    :return dict: Parsed properties.
    """
    # To sanitize inputs
    type_map = {'use_local_error': bool, 'downsample_tol': float,
                'last_ind': int, 'removal_range': int, 'n_elastic_region': int,
                'apply_filter': bool, 'wl_base_factor': int, 'wl_2prct_factor': int,
                'sat_tol': float, 'f_yn': float}
    # Deprecated parameters for the old downsampling method
    old_parameters = ['max_dev_tol', 'use_midpoint_method']

    def sani(x, p):
        if x == 'None':
            # Some parameters use None or their type
            return None
        if p in type_map:
            return type_map[p](x)
        else:
            raise ValueError('Unrecognized entry "{0}" in the downsample_props.txt file.'.format(p))

    with open(fpath, 'r') as f:
        lines = f.readlines()
    properties = dict()
    rr = []
    for l in lines:
        ls = l.split(',')
        p = ls[0].strip()
        if p == 'removal_range':
            # Put all the remove ranges together
            ls2 = ls[1].split(':')
            rr.append([sani(ls2[0], p), sani(ls2[1], p)])
        elif p in old_parameters:
            print('Deprecated downsample parameter "{0}"; neglecting this parameter.'.format(p))
        else:
            properties[p] = sani(ls[1].strip(), p)
        properties['removal_ranges'] = rr
    return properties


def downsample_loop(d, last_ind, global_tol, local_tol_0=0.1, max_its=10, removal_ranges=[]):
    """ Runs downsampler until a global tolerance is reached. """
    d = scale_data(d)
    # Only use the data up to the last index from the stress-strain peaks
    d = d[0:last_ind+1, :]
    ds_tol = local_tol_0
    e = 10 * global_tol
    it = 0
    convergence_factor = 1.05
    while e > global_tol and it < max_its:
        ind = polyprox.min_num(d, epsilon=ds_tol, return_index=True)
        e = downsample_error(d, ind, removal_ranges)
        print('Current error = {0:0.1%}, # points = {1}, current tol = {2:0.3e}'.format(e, len(ind), ds_tol))
        # 1.05 below to force a continued reduction near global_tol = e
        ds_tol *= (global_tol / e / convergence_factor)
        it += 1

    return list(ind)
