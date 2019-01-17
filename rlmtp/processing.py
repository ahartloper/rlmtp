import os
import errno
from rlmtp.readers import import_dion7_data, import_catman_data, read_filter_info
from rlmtp.sync_temperature import sync_temperature
from rlmtp.plotting import stress_strain_plotter, temp_time_plotter
from rlmtp.filtering import clean_data


def dir_maker(directory):
    """ Makes directory if it doesn't exist, else does nothing. """
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return


def load_data_files(input_dir):
    """ Checks if the correct files exists and loads them if they do.

    :param str input_dir: Specimen parent directory.
    :return dict: Contains the Dion7 data, catman data, and filtering data.

    - If any of the data files do not exist, then None is returned in their place.
    """
    excel_path = 'Excel/'
    raw_path = 'rawData/'
    print('Checking files...')
    files_in_excel = os.listdir(input_dir + excel_path)
    files_in_raw = os.listdir(input_dir + raw_path)
    files_in_root = os.listdir(input_dir)
    # Dion7 data file
    try:
        valid_file = [f for f in files_in_excel if f[:8] == 'testData']
        dion7_file = input_dir + excel_path + valid_file[0]
        dion7_data = import_dion7_data(dion7_file)
        valid_dion7_data = True
        print('\t Dion7 data exists.')
    except (FileNotFoundError, IndexError):
        valid_dion7_data = False
        print('\t Dion7 data does NOT exist.')
    # catman data file
    try:
        valid_file = [f for f in files_in_raw if f[:11] == 'Temperature']
        valid_file = [f for f in valid_file if (f[-4:].lower() == 'xlsx' or f[-3:].lower() == 'xls')]
        catman_file = input_dir + raw_path + valid_file[0]
        catman_data = import_catman_data(catman_file)
        valid_catman_data = True
        print('\t catman data exists.')
    except (FileNotFoundError, IndexError):
        valid_catman_data = False
        print('\t catman data does NOT exist.')
    # filtering file
    try:
        valid_file = [f for f in files_in_root if f[:6] == 'filter']
        filter_file = input_dir + valid_file[0]
        filter_data = read_filter_info(filter_file)
        valid_filter_data = True
        print('\t Filtering information exists.')
    except (FileNotFoundError, IndexError):
        valid_filter_data = False
        print('\t Filtering information does NOT exist.')

    # Add all the datafiles to a dict and return it
    data = {}
    if valid_dion7_data:
        data['Dion7'] = dion7_data
    else:
        data['Dion7'] = None
    if valid_catman_data:
        data['catman'] = catman_data
    else:
        data['catman'] = None
    if valid_filter_data:
        data['filtering'] = filter_data
    else:
        data['filtering'] = None
    return data


def generate_output(data, output_dir):
    """ Creates the output files in the specified directory.

    :param pd.DataFrame data: Contains all the data to save to file.
    :param str output_dir: Directory where files will be saved.
    :return:
    """
    # Write the .csv file
    file_name = 'processed_data.csv'
    out_path = os.path.join(output_dir, file_name)
    data.to_csv(out_path, index=False)

    # Write the figures
    stress_strain_plotter(data, output_dir)
    if 'Temperature[C]' in data.columns:
        temp_time_plotter(data, output_dir)
    return


def process_specimen_data(input_path, output_root):
    """ Generates the final .csv output and plots the relevant data.

    :param str input_path: Parent directory of the coupon specimen data.
    :param str output_root: Parent directory to create the output directory in.
    :return pd.DataFrame: Contains all the processed, filtered data collected by the function.

    - The structure of the specimen input directory must follow the specification. The behavior of this function
    depends on the files that exist.
    - The Dion7 data must exist for this function to run, temperature and filtering data are optional.
    - The output directory gets the same name as the input directory.
    - A new directory is created in the output_root if it does not exist already, all the processed files are placed
    in this directory.
    - If the temperature data exists, it is synced with the Dion7 data.
    """
    # Check to see if the correct files exist, and load the data
    all_data = load_data_files(input_path)
    dion7_data = all_data['Dion7']
    if dion7_data is None:
        raise Exception('Dion7 data does not exist (in the correct format), exiting.')
    # Add the temperature to the stress/strain data
    catman_data = all_data['catman']
    if catman_data is not None:
        print('Syncing temperature data with Dion7 data...')
        final_data = sync_temperature(dion7_data, catman_data)
    else:
        final_data = dion7_data.data
    # Do the filtering
    filter_info = all_data['filtering']
    if filter_info is not None:
        print('Filtering the data...')
        final_data = clean_data(final_data, filter_info)

    # Output the required files
    specimen_dir_name = os.path.normpath(input_path).split(os.path.sep)[-1]
    output_dir = os.path.join(output_root, specimen_dir_name)
    dir_maker(output_dir)
    print('Generating the output...')
    generate_output(final_data, output_dir)
    print('Finished processing!')
    return final_data
