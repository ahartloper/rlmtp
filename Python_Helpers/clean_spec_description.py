"""
This files removes unwanted characters from the specimen_description.csv files.

This can most likely occur after editing the file in Excel.
"""

import os

top = '.'
for root, dirs, files in os.walk(top, topdown=False):
    for name in files:
        if name == 'specimen_description.csv':
            fpath = os.path.join(root, name)
            print('found ' + fpath)
            with open(fpath, 'r+') as f:
                contents = f.read()
                # Remove the following characters: ;, [, ]
                clean_contents = contents.replace(';', '').replace('[', '').replace(']', '')
                # Write back to the file and remove any excess
                f.seek(0)
                f.write(clean_contents)
                f.truncate()
