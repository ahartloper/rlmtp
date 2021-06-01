"""
This file creates a table with relavent mechanical properties.
"""
import pandas as pd
import os
import numpy as np
from datetime import datetime


def gen_mech_props_tab():
    # User inputs
    date = datetime.today().strftime('%Y-%m-%d')
    summary_table = 'Database_Summaries/Summarized_Material_DB_' + date + '.csv'
    yield_props_table = 'Clean_Data/yield_stress/yield_stress_data.csv'
    db_tag_map = 'Clean_Data/db_tag_clean_data_map.csv'

    # Automatic processing below --------------------------------------------------
    # Set-up the dataframe
    df = pd.read_csv(summary_table, index_col=[0])
    # df = df.loc[:, columns]
    fy_col = 'Yield Stress [MPa]'
    em_col = 'Elastic Modulus [MPa]'
    df[fy_col] = np.nan
    df[em_col] = np.nan

    # Load and transfer the yield properties
    yield_props = pd.read_csv(yield_props_table)
    ind_to_fpath = pd.read_csv(db_tag_map, header=0, names=['ind', 'data_file'])
    # Normalize the paths
    yield_props['data_file'] = yield_props['data_file'].apply(os.path.normpath)
    ind_to_fpath['data_file'] = ind_to_fpath['data_file'].apply(os.path.normpath)
    # Set the indices
    yield_props = yield_props.set_index('data_file')
    ind_to_fpath = ind_to_fpath.set_index('ind')
    for df_ind in df.index:
        if df_ind in ind_to_fpath.index:
            df.loc[df_ind, fy_col] = float(yield_props.loc[ind_to_fpath.loc[df_ind], 'fy_m'])
            df.loc[df_ind, em_col] = float(yield_props.loc[ind_to_fpath.loc[df_ind], 'E_m'])

    # Compute fracture strain for individuals
    cols_to_keep = [
        'Grade', 'Spec.', 'Source', 'LP', fy_col, em_col
    ]
    top_dia = 'Avg. Fractured Dia. Top [mm]'
    bot_dia = 'Avg. Fractured Dia. Bot [mm]'
    df_individual = df[cols_to_keep].copy()
    df_individual['Fracture Strain'] = 2. * np.log(df['Avg. Reduced Dia. [mm]'] / (0.5 * (df[top_dia] + df[bot_dia])))
    # Output the individual specimen table
    df_individual = df_individual.sort_values(by=['Grade', 'Spec.', 'Source', 'LP'])
    df_individual.to_csv('Database_Summaries/Summarized_Mechanical_Props_Individual_' + date + '.csv')

    def coefvar(x):
        """ Returns the coeficient of variation using the sample standard deviation."""
        return np.std(x, ddof=1) / np.mean(x)

    # Output the "by campaign" table
    df_campaign = df[['Grade', 'Spec.', 'Source', fy_col, em_col]].sort_values(by=['Grade', 'Spec.', 'Source'])
    df_campaign = df_campaign.groupby(['Grade', 'Spec.', 'Source']).agg(['size', 'count', 'mean', coefvar])
    df_campaign.to_csv('Database_Summaries/Summarized_Mechanical_Props_Campaign_' + date + '.csv')


if __name__ == "__main__":
    gen_mech_props_tab()
