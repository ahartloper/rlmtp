"""
This file creates a table with relavent mechanical properties.
"""
import pandas as pd
import os
import numpy as np
from datetime import datetime
from campaign_reference_map import campaign_reference_map


def gen_mech_props_tab(processed_data_root='Unreduced_Data'):
    # User inputs
    date = datetime.today().strftime('%Y-%m-%d')
    summary_table = 'Database_Summaries/Summarized_Material_DB_' + date + '.csv'
    yield_props_table = os.path.join(processed_data_root, 'yield_stress', 'yield_stress_data.csv')
    db_tag_map = os.path.join(processed_data_root, 'db_tag_clean_data_map.csv')

    # Automatic processing below --------------------------------------------------
    # Set-up the dataframe
    df = pd.read_csv(summary_table, index_col=[0])
    # df = df.loc[:, columns]
    fy_col = 'Yield Stress [MPa]'
    em_col = 'Elastic Modulus [MPa]'
    ref_col = 'citekey'
    df[fy_col] = np.nan
    df[em_col] = np.nan

    # Load and transfer the yield properties
    yield_props = pd.read_csv(yield_props_table)
    ind_to_fpath = pd.read_csv(db_tag_map, names=['ind', 'data_file'])
    # Normalize the paths
    yield_props['data_file'] = yield_props['data_file'].apply(os.path.normpath)
    ind_to_fpath['data_file'] = ind_to_fpath['data_file'].apply(os.path.normpath)
    # Set the indices
    yield_props = yield_props.set_index('data_file')
    ind_to_fpath = ind_to_fpath.set_index('ind')
    for df_ind in df.index:
        if df_ind in ind_to_fpath.index:
            fpath = ind_to_fpath.loc[df_ind]
            df.loc[df_ind, fy_col] = float(yield_props.loc[fpath, 'fy_m'])
            df.loc[df_ind, em_col] = float(yield_props.loc[fpath, 'E_m'])
    # Incorporate the references with the dataframe
    ind_and_refs = construct_reference_map(processed_data_root, ind_to_fpath)
    df = df.join(ind_and_refs)

    # Compute fracture strain for individuals
    cols_to_keep = [
        ref_col, 'Grade', 'Spec.', 'Source', 'LP', fy_col, em_col
    ]
    top_dia = 'Avg. Fractured Dia. Top [mm]'
    bot_dia = 'Avg. Fractured Dia. Bot [mm]'
    df_individual = df[cols_to_keep].copy()
    df_individual['Fracture Strain'] = 2. * np.log(df['Avg. Reduced Dia. [mm]'] / (0.5 * (df[top_dia] + df[bot_dia])))
    # Output the individual specimen table
    df_individual = df_individual.sort_values(by=['citekey', 'Grade', 'Spec.', 'Source', 'LP'])
    df_individual.to_csv('Database_Summaries/Summarized_Mechanical_Props_Individual_' + date + '.csv')

    def coefvar(x):
        """ Returns the coeficient of variation using the sample standard deviation."""
        return np.std(x, ddof=1) / np.mean(x)

    # Output the "by campaign" table
    df_campaign = df[[ref_col, 'Grade', 'Spec.', 'Source', fy_col, em_col]].copy()
    df_campaign['Source'] = df_campaign['Source'].fillna(value='N/A')
    df_campaign['Spec.'] = df_campaign['Spec.'].fillna(value='N/A')
    df_campaign[ref_col] = df_campaign[ref_col].fillna(value='Current')
    df_campaign = df_campaign.sort_values(by=['Grade', 'Spec.', 'Source'])
    df_campaign = df_campaign.groupby([ref_col, 'Grade', 'Spec.', 'Source']).agg(['size', 'count', 'mean', coefvar])
    df_campaign.to_csv('Database_Summaries/Summarized_Mechanical_Props_Campaign_' + date + '.csv')


def construct_reference_map(root_dir, ind_to_fpath):
    # Put all the cite keys and directories in lists
    cite_keys = []
    full_cdirs = []
    for ck, campaign_dirs in campaign_reference_map.items():
        for cdir in campaign_dirs:
            full_cdirs.append(os.path.normpath(os.path.join(root_dir, cdir)))
            cite_keys.append(ck)
    inds = list(ind_to_fpath.index)
    fpaths = ind_to_fpath['data_file']

    # Associate each filepath with a cite key
    all_cks = []
    for fp in fpaths:
        # The default citekey is an empty string
        ck = np.NaN
        # Search through all the cite key directories
        for i, cdir in enumerate(full_cdirs):
            if cdir in fp:
                ck = cite_keys[i]
                break
        all_cks.append(ck)
    # Put results in a DataFrame
    res = pd.DataFrame({'citekey': all_cks}, index=inds)
    return res


if __name__ == "__main__":
    gen_mech_props_tab()
