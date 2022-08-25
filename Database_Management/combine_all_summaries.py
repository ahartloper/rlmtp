import os
from datetime import datetime
import pandas as pd


def combine_all_summaries():
    date = datetime.today().strftime('%Y-%m-%d')
    summary_dir = 'Database_Summaries'

    # Load the summary files
    main_file = os.path.join(summary_dir, 'Summarized_Material_DB_' + date + '.csv')
    mech_file = os.path.join(summary_dir, 'Summarized_Mechanical_Props_Individual_' + date + '.csv')
    chem_file = os.path.join(summary_dir, 'Summarized_Chemical_Composition_' + date + '.csv')
    main_summary = pd.read_csv(main_file, index_col=0)
    mechanical_summary = pd.read_csv(mech_file, index_col=0)
    chemical_summary = pd.read_csv(chem_file)

    # Columns to keep in each
    mech_cols = ['citekey', 'Yield Stress [MPa]', 'Elastic Modulus [MPa]', 'Fracture Strain']
    chem_cols = ['C', 'Si', 'Mn', 'P', 'S', 'N', 'Cu', 'Mo', 'Ni',
                 'Cr', 'V', 'Nb', 'Ti', 'Al', 'B', 'Zr', 'Sn', 'Ca', 'H', 'Fe']

    # DB tag to directories to map chemical compositions
    tag_dir_map = pd.read_csv('Clean_Data/db_tag_clean_data_map.csv', header=None, names=['ind', 'cpath'])
    cpath = [os.path.normpath(p) for p in tag_dir_map['cpath']]
    cpath = [os.sep.join(p.split(os.sep)[1:-1]) for p in cpath]
    # Create chem comps list
    chem_comps = {}
    for i, cp in enumerate(cpath):
        for j, chem_row_j in enumerate(chemical_summary['cpath']):
            if cp in chem_row_j:
                chem_comps[tag_dir_map.iloc[i]['ind']] = chemical_summary.iloc[j][chem_cols]
                break
    chem_comp_df = pd.DataFrame.from_dict(chem_comps, orient='index')

    # Combine all the data
    tag_map_2 = tag_dir_map.set_index('ind', drop=True)
    tag_map_2['cpath'] = tag_map_2['cpath'].apply(os.path.normpath)
    main_summary[mech_cols] = mechanical_summary[mech_cols]
    main_summary[chem_cols] = chem_comp_df[chem_cols]
    main_summary['file'] = tag_map_2['cpath']
    # Rename the columns and save to csv
    cols = main_summary.columns
    rename_dict = {}
    for c in cols:
        rename_dict[c] = c.lower().replace('.', '').replace('[', '_').replace(']', '_').replace(' ', '_')
    main_summary = main_summary.rename(rename_dict, axis='columns')
    main_summary.to_csv(os.path.join(summary_dir, 'Overall_Summary_' + date + '.csv'), index_label='hidden_index')


if __name__ == "__main__":
    combine_all_summaries()
