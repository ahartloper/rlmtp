"""@package construct_database
Functions to compile specimen description databases.
"""

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
    database_tag = 0
    # Construct the database
    for root, dirs, files in os.walk(parent_directory):
        # Walk through the subdirectories until we find the specimen_description.csv file
        if file_to_find in files:
            print('Found {0}, adding to database...'.format(os.path.join(root, file_to_find)))
            del dirs[:]  # delete in-place so we don't search the current subdirectories
            # Now we read the data and add it to our database
            file = os.path.join(root, file_to_find)
            df = description_reader.read(file)
            df['DB Tag'] = database_tag
            database = database.append(df)
            # Leave a file with the DB tag in the specimen directory to map between, then increment the tag
            write_db_tag_file(root, database_tag)
            database_tag += 1
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


def write_db_tag_file(specimen_dir, db_tag):
    """ Writes a file with the current database tag in the specimen directory. """
    file_name = 'db_tag.txt'
    with open(os.path.join(specimen_dir, file_name), 'w') as f:
        f.write(str(db_tag))
    return


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
            database = handle_diameter_entries(mi, database, description_reader, 'gage_length_n')
        elif mi == 'fractured_dia_top_m':
            prev_tag_1 = description_reader.accepted_inputs['reduced_dia_m'][0]
            prev_tag_2 = description_reader.accepted_inputs['fractured_dia_bot_m'][0]
            if prev_tag_1 in database.columns:
                database = handle_diameter_entries(mi, database, description_reader, prev_tag_1)
            elif prev_tag_2 in database.columns:
                database = handle_diameter_entries(mi, database, description_reader, prev_tag_2)
            else:
                prev_tag = 'gage_length_n'
                database = handle_diameter_entries(mi, database, description_reader, prev_tag)
        elif mi == 'fractured_dia_bot_m':
            prev_tag_1 = description_reader.accepted_inputs['reduced_dia_m'][0]
            prev_tag_2 = description_reader.accepted_inputs['fractured_dia_top_m'][0]
            if prev_tag_1 in database.columns:
                database = handle_diameter_entries(mi, database, description_reader, prev_tag_1)
            elif prev_tag_2 in database.columns:
                database = handle_diameter_entries(mi, database, description_reader, prev_tag_2)
            else:
                prev_tag = 'gage_length_n'
                database = handle_diameter_entries(mi, database, description_reader, prev_tag)
        else:
            warnings.warn('Could not find the multi-index keyword "{0}" in the database.'.format(mi))

    return database


def handle_diameter_entries(mi_tag, db, description_reader, insert_after_tag):
    """ Averages the diameters, adds the entry to db, and removes the old entries. """
    cols = [mi_tag + '_' + str(i) for i in range(3)]
    avg = db[cols].mean(axis=1)
    new_name = description_reader.accepted_inputs[mi_tag][0]
    db = db.drop(cols, axis=1)
    ind_gage_length = db.columns.get_loc(insert_after_tag) + 1  # +1 to insert after
    db.insert(ind_gage_length, new_name, avg)
    return db


def write_description_database_csv(parent_directory, output_file):
    """ Writes the description database to a .csv file.

    :param str parent_directory: Path of the database containing each campaign.
    :param str output_file: Path of the file to write the database.
    :return:
    """

    database = construct_description_database(parent_directory)
    database.to_csv(output_file, float_format='%g')
    return
