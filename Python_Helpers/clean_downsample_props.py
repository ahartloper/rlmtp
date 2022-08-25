"""
This files modifies the source names in specimen_description.csv files.
"""

import os

top = 'RESSLab_Material_DB/'
for root, dirs, files in os.walk(top, topdown=False):
    for name in files:
        if name == 'downsampler_props.txt':
            fpath = os.path.join(root, name)
            # print('found ' + fpath)
            with open(fpath, 'r') as f:
                contents = f.read()
                if 'wl_base_factor' in contents:
                    print(fpath)
