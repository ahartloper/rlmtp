"""
This file automatically creates filter files if none exist.
"""
import pandas as pd
import os
import rlmtp


campaign_dirs = [
    # ADD THE DIRECTORIES HERE
]
campaign_dirs = ['../RESSLab_Material_DB/' + d for d in campaign_dirs]


data_str = 'testData'
for camdir in campaign_dirs:
    lp_dirs = next(os.walk(camdir))[1]
    for lpd in [os.path.join(camdir, d1) for d1 in lp_dirs]:
        spec_dirs = next(os.walk(lpd))[1]
        for specd in [os.path.join(lpd, d2) for d2 in spec_dirs]:
            csv_txt_files = [f for f in os.listdir(specd) if (
                os.path.splitext(f)[1] == '.csv' or os.path.splitext(f)[1] == '.txt')]
            if 'filter_file.csv' not in csv_txt_files:
                print('Generating in dir: {0}'.format(specd))
                df = [f for f in os.listdir(os.path.join(specd, 'Excel')) if f[:len(data_str)] == data_str][0]
                d = pd.read_excel(os.path.join(specd, 'Excel', df), skiprows=6)
                if 'sigma_true' in d.columns:
                    d['Sigma_true'] = d['sigma_true']
                if 'points_of_interest.txt' in csv_txt_files:
                    [final_ind, remove_range] = rlmtp.read_points_of_interest(
                        os.path.join(specd, 'points_of_interest.txt'))
                    if len(remove_range) > 0:
                        print('\tFound removal range = {0}:{1}, final ind = {2}'.format(
                            remove_range[0][0], remove_range[0][1], final_ind))
                    else:
                        print('\tFound removal range = {0}:{1}, final ind = {2}'.format(None, None, final_ind))
                else:
                    final_ind = None
                    remove_range = []
                # Set the window lengths
                if 'LP9' in specd:
                    pre_2_prct_wl = 50
                    post_2_prct_wl = 3
                else:
                    pre_2_prct_wl = 50
                    post_2_prct_wl = 5
                rlmtp.generate_filter_file(d, os.path.join(specd, 'filter_file_auto.csv'), remove_range, final_ind,
                                           wl1=pre_2_prct_wl, wl2=post_2_prct_wl)
