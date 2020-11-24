"""
Useful for batch renaming directories.
"""

import os

dirs = os.listdir('.')
for d in dirs:
    spec_dir = os.path.join(d, 'Specimen 1')
    old_name = os.path.join(spec_dir, 'Raw Data')
    if os.path.isdir(old_name):
        new_name = os.path.join(spec_dir, 'rawData')
        os.rename(old_name, new_name)
