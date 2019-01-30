import os
import pandas as pd
import warnings
from rlmtp.readers import DescriptionReader


def construct_description_database(parent_directory):
    """ Builds the database of specimen descriptions from an organized database of campaign and specimen tests.

    :param str parent_directory: Path of the database containing each campaign.
    :return pd.DataFrame: Description database from all the specimens in the database.
    """
    description_reader = DescriptionReader()
    database = pd.DataFrame(dtype=object)
    file_to_find = 'specimen_description.csv'
    # Construct the database
    for root, dirs, files in os.walk(parent_directory):
        # Walk through the subdirectories until we find the specimen_description.csv file
        if file_to_find in files:
            print('Found {0}, adding to database...'.format(os.path.join(root, file_to_find)))
            del dirs[:]  # delete in-place so we don't search the current subdirectories
            # Now we read the data and add it to our database
            file = os.path.join(root, file_to_find)
            database = database.append(description_reader.read(file))
    # TODO: figure out some way to order the columns according to the ordered dict in the description reader
    # Reset the indices
    database = database.reset_index(drop=True)
    # Change the column names that correspond to multiple entries, needs to happen before the single entries
    database = handle_multi_input(database, description_reader.multiple_inputs)
    # Change the column names that correspond to single entries
    database = database.rename(index=str, columns=description_reader.accepted_inputs)
    return database


def handle_multi_input(database, multi_inputs):
    """ Renames or replaces columns that correspond to keyword with multiple values.

    :param pd.DataFrame database: Specimen description database.
    :param list multi_inputs: (str) Keywords with multiple values.
    :return pd.DataFrame: Modified database.

    - The column names in database must be based on the keyword inputs for this function to work correctly.
    """
    for input in multi_inputs:
        # We have to handle each case separately
        if input == 'pid_force':
            column_rename = dict()
            column_rename[input + '_0'] = 'PID Force K_p'
            column_rename[input + '_1'] = 'PID Force T_i'
            column_rename[input + '_2'] = 'PID Force T_d'
            database = database.rename(index=str, columns=column_rename)
        elif input == 'pid_disp':
            column_rename = dict()
            column_rename[input + '_0'] = 'PID Disp. K_p'
            column_rename[input + '_1'] = 'PID Disp. T_i'
            column_rename[input + '_2'] = 'PID Disp. T_d'
            database = database.rename(index=str, columns=column_rename)
        elif input == 'pid_extenso':
            column_rename = dict()
            column_rename[input + '_0'] = 'PID Extenso. K_p'
            column_rename[input + '_1'] = 'PID Extenso. T_i'
            column_rename[input + '_2'] = 'PID Extenso. T_d'
            database = database.rename(index=str, columns=column_rename)
        elif input == 'reduced_dia_m':
            cols = [input + '_' + str(i) for i in range(3)]
            avg = database[cols].mean(axis=1)
            new_name = 'Avg. Red. Dia [mm]'
            database = database.drop(cols, axis=1)
            ind_gage_length = database.columns.get_loc('gage_length_n') + 1  # +1 to insert after
            database.insert(ind_gage_length, new_name, avg)
        else:
            warnings.warn('Could not find the multi-index keyword "{0}" in the database.'.format(input))

    return database


def write_description_database_csv(parent_directory, output_file):
    """ Writes the description database to a .csv file.

    :param str parent_directory: Path of the database containing each campaign.
    :param str output_file: Path of the file to write the database.
    :return:
    """

    database = construct_description_database(parent_directory)
    database.to_csv(output_file, float_format='%g')
    return
