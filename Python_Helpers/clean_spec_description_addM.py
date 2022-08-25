"""
This files modifies J2 to J2+M in specimen_description.csv files.
"""

import os

top = 'RESSLab_Material_DB/S355J2_Plates/WP3_PLT15_CRM12'
old_name = 'J2'
new_name = 'J2+N'
for root, dirs, files in os.walk(top, topdown=False):
    for name in files:
        if name == 'specimen_description.csv':
            fpath = os.path.join(root, name)
            print('found ' + fpath)
            with open(fpath, 'r+') as f:
                contents = f.read()
                # Replaces old_name with new_name
                if (old_name in contents) and ~(new_name in contents):
                    clean_contents = contents.replace(old_name, new_name)

                # Write back to the file and remove any excess
                f.seek(0)
                f.write(clean_contents)
                f.truncate()
