"""
This file generates strain rate plots for a sample of the tests.

Run this file from the command line:
>>> python generate_strain_rate_plots.py
"""
import os
import pandas as pd
import rlmtp

# Use the data that has already been filtered/reduced
input_root = 'Clean_Data'
data_dirs = [
    'S235275_Plates/S235275_Plate15'
]

# Set the output directory
output_root = 'Clean_Data/strain_rates'

# Data processing -------------------------------------------------------------
for d in data_dirs:
    files = os.listdir(os.path.join(input_root, d))
    csv_files = [os.path.join(input_root, d, fi) for fi in files if fi[-3:] == 'csv']
    for data_file in csv_files:
        data = pd.read_csv(data_file)
        output_dir = os.path.join(output_root, d)
        rlmtp.dir_maker(output_dir)
        test_name = '_'.join(os.path.basename(data_file).split('_')[:3])
        rlmtp.strain_rate_plotter(data, output_dir, test_name)
