import os
import pandas as pd
import numpy as np
from datetime import datetime
from campaign_directories import campaign_dirs_nonrlmtp, campaign_dirs_rlmtp, input_root
from campaign_reference_map import campaign_reference_map


def gen_chem_comp():

    date = datetime.today().strftime('%Y-%m-%d')

    # Load all the chemical compositions
    all_campaign_dirs = campaign_dirs_nonrlmtp + campaign_dirs_rlmtp
    chem_comp_data = []
    for cdir in all_campaign_dirs:
        cpath = os.path.join(input_root, cdir)
        files = os.listdir(cpath)
        if 'chemical_composition.csv' in files:
            d = pd.read_csv(os.path.join(cpath, 'chemical_composition.csv'))
            d['cpath'] = os.path.normpath(cpath)
        else:
            d = pd.DataFrame()
            d['cpath'] = os.path.normpath(cpath)
        chem_comp_data.append(d)
    df = pd.concat(chem_comp_data, sort=False)
    df = df.set_index('cpath', drop=True)
    df['Grade'] = None
    df['Spec.'] = None
    df['Source'] = None

    # Load DB summary
    db_summary = pd.read_csv('Database_Summaries/Summarized_Material_DB_' + date + '.csv')
    # Load tag map
    db_tag_map = pd.read_csv('Clean_Data/db_tag_clean_data_map.csv', names=['tag', 'path'])
    db_tag_map['path'] = db_tag_map['path'].apply(os.path.normpath)
    db_tag_map = db_tag_map.set_index('path', drop=True)
    all_paths = db_tag_map.index

    # Add grade, specification, source data
    for cpath in df.index:
        rpath = os.path.sep.join(cpath.split(os.path.sep)[1:])
        for p in all_paths:
            if rpath in p:
                ind = db_tag_map.loc[p, 'tag']
                break
        ck = 'Current'
        for citekey, cite_paths in campaign_reference_map.items():
            for cp in cite_paths:
                if cp in cpath:
                    ck = citekey
        df.loc[cpath, ['Grade', 'Spec.', 'Source']] = db_summary.loc[ind, ['Grade', 'Spec.', 'Source']]
        df.loc[cpath, 'citekey'] = ck

    # Save the table to file
    col_order = ['citekey', 'Grade', 'Spec.', 'Source', 'C', 'Si', 'Mn', 'P', 'S', 'N', 'Cu',
                 'Mo', 'Ni', 'Cr', 'V', 'Nb', 'Ti', 'Al', 'B', 'Zr', 'Sn', 'Ca', 'H', 'Fe']
    df = df[col_order]
    df = df.replace('-', np.nan)
    csv_output = 'Database_Summaries/Summarized_Chemical_Composition_' + date + '.csv'
    df.to_csv(csv_output)
