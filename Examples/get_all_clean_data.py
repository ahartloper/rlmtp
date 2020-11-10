"""
This file generates, sorts, and extracts cleaned stress-strain data from the database.

Additional data that follows the RLMTP storage protocol should be appended to the campaign_dirs_rlmtp list.
Additional data that does not follow the RLMTP storage protocol should be appended to the campaign_dirs_nonrlmtp list.

Run this file from the command line:
>>> python get_all_clean_data.py
"""
import os
import pandas as pd
from shutil import copy2
import errno
import rlmtp
import numpy

# The input_root directory contains the following campaign_dirs
input_root = './RESSLab_Material_DB'
# Data in these directories follow the RLMTP protocol
# The data in these folders are in raw format and need to be filtered/reduced
campaign_dirs_rlmtp = [
    # S355
    # 'S355J2_HEB500/flange',
    # 'S355J2_HEB500/web',
    # 'S355J2_HEM300/flange',
    # 'S355J2_IPE300/flange',
    # 'S355J2_IPE300/web',
    # 'S355J2_IPE400',
    # 'S355J2_HEM320/WP3_HEM320_D_CRM20',
    # 'S355J2_HEM320/WP3_HEM320_C_CRM20',
    # 'S355J2_IPE360/WP3_IPE360_D_CRM8',
    'S355J2_IPE360/WP3_IPE360_C_CRM8_flange',

    # S690
    # 'S690QL/Base metal',
    # 'S690QL/Heat affected zone',
    # 'S690_leftplate',
    # 'S690_middleplate',

    # Fe-SMA
    # 'FE_SMA/FE_SMA_Cyclic-Calib'
]
# Data in these directories do not following the RLMTP protocol
# The data in these folders are already filtered/reduced, just need to copy
campaign_dirs_nonrlmtp = [
    # 'S690QL/25mm',
    # 'S460NL/25mm',
    # 'S355J2_Plates/S355J2_N_25mm',
    # 'S355J2_Plates/S355J2_N_50mm',
    # 'HYP400',
    # 'BCR295',
    # 'BCP325',
    # 'A500',
    # 'A992_Gr50/A992_W14X82_flange',
    # 'A992_Gr50/A992_W14X82_web'
]
# Set the output directory
output_root = './Clean_Data'


# Data processing -------------------------------------------------------------
def get_db_tag(specimen_dir):
    if 'db_tag.txt' in os.listdir(specimen_dir):
        with open(os.path.join(p, 'db_tag.txt'), 'r') as f:
            db_tag = int(f.readlines()[0])
    else:
        print('Generate the database summary!')
        raise ValueError('Missing db_tag.txt in {0}'.format(p))
    return db_tag


db_tag_to_out_dir = dict()
# Process the RLMTP data
for campaign in campaign_dirs_rlmtp:
    print('Processing {0}'.format(campaign))
    cdir = os.path.join(input_root, campaign)
    # next(os.walk(cdir))[1] gets only the directories in cdir
    lps_in_campaign = next(os.walk(cdir))[1]
    for lp in lps_in_campaign:
        specimens = next(os.walk(os.path.join(cdir, lp)))[1]
        for s in specimens:
            output_dir = os.path.join(output_root, campaign)
            p = os.path.join(cdir, lp, s)
            rlmtp.process_specimen_data(p, output_dir, ignore_filter=True)
            # Add the DB tag to the map
            db_tag_to_out_dir[get_db_tag(p)] = output_dir


# Process the non-RLMTP data
def is_valid_data(file):
    """ Returns True file contain stress-strain data, False otherwise. """
    data = pd.read_csv(file, nrows=5)
    if 'e_true' and 'Sigma_true' in data.columns:
        return True
    else:
        return False


def dir_maker(directory):
    """ Makes directory if it doesn't exist, else does nothing. """
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return


for campaign in campaign_dirs_nonrlmtp:
    print('Processing {0}'.format(campaign))
    cdir = os.path.join(input_root, campaign)
    lps_in_campaign = next(os.walk(cdir))[1]
    for lp in lps_in_campaign:
        specimens = next(os.walk(os.path.join(cdir, lp)))[1]
        for s in specimens:
            output_dir = os.path.join(output_root, campaign)
            dir_maker(output_dir)
            raw_data_dir = os.path.join(cdir, lp, s, 'rawData')
            files = os.listdir(raw_data_dir)
            for f in files:
                data_file = os.path.join(raw_data_dir, f)
                if is_valid_data(data_file):
                    copy2(data_file, output_dir)
                    data = pd.read_csv(data_file)
                    rlmtp.stress_strain_plotter(data, output_dir, f[:-4])
                    # Add the DB tag to the map
                    p = os.path.join(cdir, lp, s)
                    db_tag_to_out_dir[get_db_tag(p)] = output_dir
                    break

# Write the DB tag to output dir map
tag_to_outdir_file = os.path.join(output_root, 'db_tag_out_dir_map.csv')
with open(tag_to_outdir_file, 'w') as f:
    for tag, dir_path in db_tag_to_out_dir.items():
        f.write('{0},{1}\n'.format(tag, dir_path))
