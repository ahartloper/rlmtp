"""
This files removes "desktop.ini" files in any directory.

These files are from google drives and may exist when data is copied from a google drive.
"""

import os

top = '.'
for root, dirs, files in os.walk(top, topdown=False):
    for name in files:
        if name == 'desktop.ini':
            print('found ' + os.path.join(root, name))
            os.remove(os.path.join(root, name))
    for name in dirs:
        if name == 'desktop.ini':
            print('found ' + os.path.join(root, name))
            os.rmdir(os.path.join(root, name))
