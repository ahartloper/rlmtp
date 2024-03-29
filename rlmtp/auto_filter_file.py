"""@package auto_filter_file
Function to generate filter files from stress-strain data.
"""
from .find_peaks import find_peaks, find_peaks2
from .yield_properties import yield_properties


def generate_filter_file(d, out_path, remove_ranges=[], last_ind=None, wl1=50, wl2=5, wly=None):
    """ Writes an automatically generated filter file for data.
    :param pd.DataFrame d: Contains stress-strain data.
    :param str out_path: Path to write the output filter file.
    :param list remove_ranges: [int, int] Contains indices of ranges of data to remove.
    :param int last_ind: If not None, then only consider data up to this index.
    :param int wl1: Window length for strain range prior to 2% amplitude.
    :param int wl2: Window length for strain range after 2% amplitude.
    :param int wly: Optional, Window length for the strain range up to the yield stress.

    Notes:
    ======
        - The parameter wly only has an effect if the strain amplitude is less than 2% (e.g., LP4 and LP5)
    """
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
        i_final = [0] + i + [i2, i_fyupper]
    # Remove data past 12.5% and remove after the last specified index
    if len(ilast) > 0 or last_ind is not None:
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
    # Add the removal range indices
    rr_start_ind = []
    rr_diffs = []
    for r_range in remove_ranges:
        rr_start = r_range[0]
        rr_end = r_range[1]
        rr_start_ind.append(rr_start)
        rr_diffs.append(rr_end - rr_start + 1)
        i_final += [rr_start, rr_end]
        # remove any points between start and end
        i_final = [i for i in i_final if not (rr_start < i < rr_end)]
    # Combine the points
    i_final = sorted(list(set(i_final)))

    # Write the filter file
    # Doesn't use any interpolation between points (interp_order = 0)
    if len(remove_ranges) == 0:
        # When don't have removal ranges
        if passes_2prct:
            j = i_final.index(iamp)
            out_str = '{0},0\n'.format(wl1) + ','.join([str(i) for i in i_final[:j]])
            out_str += '\n{0},0\n'.format(wl2) + ','.join([str(i) for i in i_final[j:]]) + '\n'
        else:
            j_ify = i_final.index(i_fyupper) + 1
            out_str = '{0},0\n'.format(wly) + ','.join([str(i) for i in i_final[:j_ify]])
            out_str += '\n{0},0\n'.format(wl1) + ','.join([str(i) for i in i_final[j_ify:]])
    else:
        # Assume that all remove ranges are before the switch to higher strain rate
        # Assume only one removal range
        out_str = '{0},0\n'.format(wl1)
        rr_i = rr_start_ind[0]
        ind_list = []
        just_used_rr = False
        for count, i in enumerate(i_final):
            if i < rr_i:
                ind_list.append(i)
            elif i == rr_i:
                # Start index
                if count == 1:
                    # If it's the second point, add one more before it for the first range
                    ind_list.append(i - 1)
                just_used_rr = True
                out_str += ','.join([str(i) for i in ind_list]) + '\n'
                out_str += '{0},0\n{1},'.format(rr_diffs[0], i)
                ind_list = []
            elif just_used_rr:
                # End index
                just_used_rr = False
                if passes_2prct:
                    if i_final[count + 1] == int(iamp):
                        # If next point is the amplitude limit just add the last point of the remove range
                        out_str += '{0}'.format(i)
                    else:
                        # Else, add the last point of the remove range and start a new series at window length 1
                        out_str += '{0}\n{1},0\n'.format(i, wl1)
                else:
                    # Don't need to worry about the amplitude limit if don't pass 2%
                    out_str += '{0}\n{1},0\n'.format(i, wl1)
            else:
                # Continue as normal
                ind_list.append(i)
        # Finish off the string
        if passes_2prct:
            j = ind_list.index(iamp)
            out_str += ','.join([str(i) for i in ind_list[:j]])
            out_str += '\n{0},0\n'.format(wl2) + ','.join([str(i) for i in ind_list[j:]]) + '\n'
        else:
            out_str += ','.join([str(i) for i in ind_list])
    # Write file
    with open(out_path, 'w') as f:
        f.write(out_str)
    return


def read_points_of_interest(fpath):
    """ Reads the points_of_interest.txt files.
    :param str fpath: Path to the file.
    :return list: [int, list] first value is the buckle index, second is the list of removal range.
    """
    with open(fpath, 'r') as f:
        lines = f.readlines()
    final_ind = None
    remove_range = []
    for l in lines:
        l_split = l.split(',')
        if l_split[0] == 'buckle_ind':
            final_ind = int(l_split[1])
        elif l_split[0] == 'removal_range':
            ls2 = l_split[1].split(':')
            remove_range.append([int(ls2[0]), int(ls2[1])])
    return [final_ind, remove_range]
