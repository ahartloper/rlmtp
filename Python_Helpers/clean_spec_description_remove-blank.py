"""
This files removes lines that should be blank but have commas from the specimen_description.csv files.

This can most likely occur after editing the file in Excel.
"""

import os

top = 'RESSLab_Material_DB/S355J2_IPE330/S355J2_IPE330_RBS_D_CRM8'
for root, dirs, files in os.walk(top, topdown=False):
    for name in files:
        if name == 'specimen_description.csv':
            lines_to_keep = []
            fpath = os.path.join(root, name)
            print('found ' + fpath)
            with open(fpath, 'r+') as f:
                for line in f:
                    if line[0] != ',':
                        lines_to_keep.append(line)
                # Write back to the file and remove any excess
                f.seek(0)
                f.writelines(lines_to_keep)
                f.truncate()
