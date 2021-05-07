"""
This file computes the average measured yield stress for each material.

Run this file from the command line:
>>> python generate_yield_properties.py

Notes:
    - All the clean data needs to be generated first.
    - The link between the database entry and the file can be found through the
        'db_tag_out_dir_map.csv' file.
"""
import os
import pandas as pd
import numpy as np
import rlmtp
from campaign_directories import campaign_dirs_rlmtp, campaign_dirs_nonrlmtp

# Use clean data
clean_data_root = 'Clean_Data'
data_dirs = campaign_dirs_rlmtp + campaign_dirs_nonrlmtp

# Set the output directory
output_root = './Clean_Data/yield_stress'
rlmtp.dir_maker(output_root)

# Data processing -------------------------------------------------------------
# If the elastic data is "bad quality" then the elastic modulus may be low
# In this case we want to reject the fitting
e_mod_nominal = 2.e5
e_mod_min_acceptable = 0.8 * e_mod_nominal
e_mod_max_acceptable = 1.2 * e_mod_nominal
yield_data = []
for d in data_dirs:
    files = os.listdir(os.path.join(clean_data_root, d))
    csv_files = [os.path.join(clean_data_root, d, fi) for fi in files if fi[-3:] == 'csv']
    for data_file in csv_files:
        data = pd.read_csv(data_file)
        try:
            yield_props = rlmtp.yield_properties(data)
        except IndexError:
            try:
                # Poor data in elastic region, extend the range
                # Boost the yield stress so that a*f_yn = 345
                yield_props = rlmtp.yield_properties(data, f_yn=523.)
            except IndexError:
                # Insufficient data in elastic region
                yield_props = [np.nan, np.nan]
        if not (e_mod_min_acceptable <= yield_props[0] <= e_mod_max_acceptable):
            # Reject the found properties
            yield_props = [np.nan, np.nan]
        yield_data.append([data_file, yield_props[0], yield_props[1]])

# Store in a dataframe and save
df = pd.DataFrame(yield_data, columns=['data_file', 'E_m', 'fy_m'])
df.to_csv(os.path.join(output_root, 'yield_stress_data.csv'), index=False)
