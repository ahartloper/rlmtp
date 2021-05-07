"""
This file generates, sorts, and extracts cleaned stress-strain data from the database.

The lists in the 'campaign_directories.py' file specify the data.

Run this file from the command line:
>>> python generate_all_clean_data.py
"""
import os
import pandas as pd
from shutil import copy2
import rlmtp
from campaign_directories import input_root, campaign_dirs_rlmtp, campaign_dirs_nonrlmtp


# Set the output directory
output_root = './Clean_Data'

# Decide whether to ignore the filtering/reduction
# If ignore_filter = False, then DO include the filtering
ignore_filter = False


# Data processing -------------------------------------------------------------
# No need to touch anything below this line
def get_db_tag(specimen_dir):
    if 'db_tag.txt' in os.listdir(specimen_dir):
        with open(os.path.join(p, 'db_tag.txt'), 'r') as f:
            db_tag = int(f.readlines()[0])
    elif 'specimen_description.csv' not in os.listdir(specimen_dir):
        # Not a valid specimen, so don't process
        db_tag = None
    else:
        print('Generate the database summary!')
        raise ValueError('Missing db_tag.txt in {0}'.format(p))
    return db_tag


db_tag_to_clean_file = dict()
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
            db_tag = get_db_tag(p)
            if db_tag is not None:
                rlmtp.process_specimen_data(p, output_dir, ignore_filter=ignore_filter)
                pre_name = rlmtp.processing.get_pre_name(p)
                output_file = rlmtp.processing.processed_file_name(output_dir, pre_name)
                # Add the DB tag to the map
                db_tag_to_clean_file[db_tag] = os.path.join(output_dir, output_file)


# Process the non-RLMTP data
def is_valid_data(file):
    """ Returns True file contain stress-strain data, False otherwise. """
    data = pd.read_csv(file, nrows=5)
    if 'e_true' and 'Sigma_true' in data.columns:
        return True
    else:
        return False


for campaign in campaign_dirs_nonrlmtp:
    print('Processing {0}'.format(campaign))
    cdir = os.path.join(input_root, campaign)
    lps_in_campaign = next(os.walk(cdir))[1]
    for lp in lps_in_campaign:
        specimens = next(os.walk(os.path.join(cdir, lp)))[1]
        for s in specimens:
            output_dir = os.path.join(output_root, campaign)
            rlmtp.dir_maker(output_dir)
            raw_data_dir = os.path.join(cdir, lp, s, 'rawData')
            files = os.listdir(raw_data_dir)
            for f in files:
                data_file = os.path.join(raw_data_dir, f)
                if is_valid_data(data_file):
                    # If the file doesn't exist, don't copy, don't plot
                    final_file_path = os.path.join(output_dir, f)
                    if os.path.isfile(final_file_path):
                        print('The processed data already exists, skipping processing!')
                    else:
                        # Do copy and do plot
                        copy2(data_file, output_dir)
                        data = pd.read_csv(data_file)
                        rlmtp.stress_strain_plotter(data, output_dir, f[:-4])
                    # Add the DB tag to the map
                    p = os.path.join(cdir, lp, s)
                    db_tag_to_clean_file[get_db_tag(p)] = os.path.join(output_dir, f)
                    break

# Write the DB tag to output file map
tag_to_outdir_file = os.path.join(output_root, 'db_tag_clean_data_map.csv')
with open(tag_to_outdir_file, 'w') as f:
    for tag, dir_path in db_tag_to_clean_file.items():
        f.write('{0},{1}\n'.format(tag, dir_path))
