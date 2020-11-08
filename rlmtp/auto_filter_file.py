"""@package auto_filter_file
Function to generate filter files from stress-strain data.
"""
from .find_peaks import find_peaks, find_peaks2
from .yield_properties import yield_properties


def generate_filter_file(d, out_path):
    """ Writes an automatically generated filter file for data.
    :param pd.DataFrame d: Contains stress-strain data.
    :param str out_path: Path to write the output filter file.
    """
    # Get the moment peaks
    i = find_peaks(d['Sigma_true'])
    # Get the strain peak of the first cycle
    i2 = find_peaks2(d['e_true'], d['Sigma_true'])
    i2 = i2[0]
    # Get the upper yield point
    em, fym = yield_properties(d)
    i3 = abs(d['Sigma_true'] - fym).idxmin()
    ipeak = d['Sigma_true'].loc[:i3].idxmax()
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
        i_final = [0] + i + [i2, int(i3), int(iamp)]
    else:
        passes_2prct = False
        i_final = [0] + i + [i2, int(i3)]
    # Remove data past 12.5%
    if len(ilast) > 0:
        i_ult = ilast.index[0]
        i_final = [i for i in i_final if i < i_ult]
        i_final.append(i_ult)
    # Combine the points
    i_final = list(set(i_final))
    i_final.sort()

    # Write the filter file
    # Window lengths for the two strain ranges
    wl1 = 25
    wl2 = 3
    # Doesn't use any interpolation between points (interp_order = 0)
    if passes_2prct:
        j = i_final.index(iamp)
        out_str = '{0},0\n'.format(wl1) + ','.join([str(i) for i in i_final[:j]])
        out_str += '\n{0},0\n'.format(wl2) + ','.join([str(i) for i in i_final[j:]]) + '\n'
    else:
        out_str = '{0},0\n'.format(wl1) + ','.join([str(i) for i in i_final])
    with open(out_path, 'w') as f:
        f.write(out_str)
    return
