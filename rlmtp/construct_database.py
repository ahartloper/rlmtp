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
    all_columns = description_reader.get_column_order()
    database = pd.DataFrame(dtype=object, columns=all_columns)
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
    # Order all the columns according to the specified order in the reader
    database = database[all_columns]
    # Reset the indices for all the rows
    database = database.reset_index(drop=True)
    # Change the column names that correspond to multiple entries, assumed to happen before the single entries
    database = handle_multi_input(database, description_reader)
    # Change the column names that correspond to single entries
    rename_single = dict((k, v) for k, v in description_reader.accepted_inputs.items() if type(v) is not list)
    database = database.rename(index=str, columns=rename_single)
    return database


def handle_multi_input(database, description_reader):
    """ Renames or replaces columns that correspond to keyword with multiple values.

    :param pd.DataFrame database: Specimen description database.
    :param DescriptionReader description_reader: Reader for the specimen description files.
    :return pd.DataFrame: Modified database.

    - The column names in database must be based on the keyword inputs for this function to work correctly.
    """
    for mi in description_reader.multiple_inputs:
        # We have to handle the PID and the diameter cases separately
        if mi[:3] == 'pid':
            column_rename = dict()
            new_names = description_reader.accepted_inputs[mi]
            for i, name in enumerate(new_names):
                column_rename[mi + '_' + str(i)] = name
            database = database.rename(index=str, columns=column_rename)
        elif mi == 'reduced_dia_m':
            cols = [mi + '_' + str(i) for i in range(3)]
            avg = database[cols].mean(axis=1)
            new_name = description_reader.accepted_inputs[mi][0]
            database = database.drop(cols, axis=1)
            ind_gage_length = database.columns.get_loc('gage_length_n') + 1  # +1 to insert after
            database.insert(ind_gage_length, new_name, avg)
        else:
            warnings.warn('Could not find the multi-index keyword "{0}" in the database.'.format(mi))

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
