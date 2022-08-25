"""
This file computes the measured yield stress and elastic modulus for each material.

Run this file from the command line:
>>> python generate_yield_properties.py

Notes:
    - All the processed data needs to be generated first.
    - By default this uses the unreduced data to have more datapoints in the yield plateau.
    - The link between the database entry and the file can be found through the
        'db_tag_clean_data_map.csv' file.
"""
import os
import pandas as pd
import numpy as np
import rlmtp
from campaign_directories import campaign_dirs_rlmtp, campaign_dirs_nonrlmtp


def gen_yield_props(processed_data_root='Unreduced_Data'):
    """ Generates the measured yield stress and elastic modulus for all tests.
    :param str processed_data_root: Directory containing the processed stress-strain data.
    """
    # Specify the directories with the stress-strain data
    data_dirs = campaign_dirs_rlmtp + campaign_dirs_nonrlmtp
    # Set the output directory
    output_root = os.path.join(processed_data_root, 'yield_stress')
    rlmtp.dir_maker(output_root)

    # Data processing -------------------------------------------------------------
    yield_data = []
    for d in data_dirs:
        files = os.listdir(os.path.join(processed_data_root, d))
        csv_files = [os.path.join(processed_data_root, d, fi) for fi in files if fi[-3:] == 'csv']
        for data_file in csv_files:
            data = pd.read_csv(data_file)
            try:
                fyn = get_nominal_fy(data_file)
                yield_props = rlmtp.yield_properties(data, f_yn=fyn)
            except IndexError:
                try:
                    # Poor data in elastic region, extend the range
                    # Boost the yield stress so that a*f_yn = f_yn, a is fixed as 0.66
                    fyn = fyn / 0.66
                    yield_props = rlmtp.yield_properties(data, f_yn=fyn)
                except IndexError:
                    # Insufficient data in elastic region
                    yield_props = [np.nan, np.nan]
            # If the elastic data is "bad quality" then the elastic modulus may be low
            # In this case we want to reject the fitting
            e_mod_min_acceptable, e_mod_max_acceptable = get_acceptable_e_range(data_file)
            if not (e_mod_min_acceptable <= yield_props[0] <= e_mod_max_acceptable):
                # Reject the found properties
                yield_props = [np.nan, np.nan]
            yield_data.append([data_file, yield_props[0], yield_props[1]])

    # Store in a dataframe and save
    df = pd.DataFrame(yield_data, columns=['data_file', 'E_m', 'fy_m'])
    df.to_csv(os.path.join(output_root, 'yield_stress_data.csv'), index=False)


def get_acceptable_e_range(fpath):
    """ Returns the min and max acceptable elastic modulus values. """
    e_mod_nominal = 2.e5
    if ('Welded_metal' in fpath) or ('HAZ' in fpath):
        # Allow a larger tolerance for these tests
        e_mod_min_acceptable = 0.6 * e_mod_nominal
        e_mod_max_acceptable = 1.4 * e_mod_nominal
    else:
        e_mod_min_acceptable = 0.75 * e_mod_nominal
        e_mod_max_acceptable = 1.25 * e_mod_nominal
    return e_mod_min_acceptable, e_mod_max_acceptable


def get_nominal_fy(fpath):
    """ Return the nominal fy for the material. """
    fyn_map = {
        'S690': 690., 'S460': 460., 'S355': 355., 'A992': 345., 'A500': 315.,
        'BCP325': 325., 'BCR295': 295., 'HYP400': 400., 'S235275': 235., 'SM490': 325., 'SN490': 325.
    }
    f_yn = 0.
    for grade, fy in fyn_map.items():
        if grade in fpath:
            f_yn = fy
            break
    if f_yn == 0.:
        # Default to 355 MPa (S355)
        f_yn = 355.
    return f_yn


if __name__ == "__main__":
    gen_yield_props()
