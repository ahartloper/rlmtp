"""
This files modifies the source names in specimen_description.csv files.
"""

import os

top = 'RESSLab_Material_DB/S355J2_Plates/S355_J2_N_HAZ_12_5_C_s_15mm_plate_SELIMCAN_MASTER_THESIS'
old_name = '15mm plate'
new_name = '15mm plate 12.5 C/s'
for root, dirs, files in os.walk(top, topdown=False):
    for name in files:
        if name == 'specimen_description.csv':
            fpath = os.path.join(root, name)
            print('found ' + fpath)
            with open(fpath, 'r+') as f:
                contents = f.read()
                # Replaces old_name with new_name
                clean_contents = contents.replace(old_name, new_name)

                # Write back to the file and remove any excess
                f.seek(0)
                f.write(clean_contents)
                f.truncate()
