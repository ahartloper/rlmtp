"""@package readers
Readers for various input files.
"""

import pandas as pd
import datetime
import warnings
import collections
from rlmtp.timed_data import TimedData


class Reader:
    """ Base class for the readers for various numerical timed data types. """

    def __init__(self, start_row):
        """ Constructor.

        :param int start_row: Row to start reading the data from, identifies the header.
        """
        self.header_rows = start_row

    def read(self, file):
        """ Returns a properly formatted TimedData object from the specified input file.

        :param str file: Path to the input file to read.
        :return TimedData: Object containing the data in the input file.
        """
        raise Exception('not implemented.')


class ExcelCatmanReader(Reader):
    """ Reader for the Excel output files from catman. """

    def __init__(self, start_row=1):
        Reader.__init__(self, start_row)
        return

    def read(self, file):
        # Import the data and remove the unnecessary rows
        data = pd.read_excel(file, header=self.header_rows)
        col_1 = data.columns[0]
        start_time = datetime.datetime.strptime(data[col_1][2], '%m.%d.%y %H:%M:%S')
        data.drop(range(47), inplace=True)
        data.reset_index(drop=True, inplace=True)
        # Rename the columns to remove the spaces
        col_new_name = ['Time[s]']  # assume that the time associated with temperature is the first column
        rename_dict = dict(zip(data.columns, col_new_name))
        # Find the temperature index
        for col in data.columns:
            if len(col) >= 12:
                if col[:11] == 'Temperature':
                    rename_dict[col] = 'Temperature[C]'
        data = data.rename(index=str, columns=rename_dict)
        time = data['Time[s]']
        sample_rate = int((time[1] - time[0]) * 1000000)
        sample_rate = datetime.timedelta(microseconds=sample_rate)
        # Add the system date column
        system_date = []
        for i in range(len(time)):
            time_diff = i * sample_rate
            system_date.append(start_time + time_diff)
        data['System Date'] = system_date
        temperature_data = TimedData(data, start_time, sample_rate)
        return temperature_data


class ExcelDion7Reader(Reader):
    # this will return a TimedData object properly formatted

    def __init__(self, start_row=8):
        Reader.__init__(self, start_row - 2)
        return

    def read(self, file):
        data = pd.read_excel(file, header=self.header_rows)
        # data.drop('S/No', inplace=True)
        data = data.rename(index=str, columns={"sigma [Mpa]": "Eng_Stress[MPa]", "epsilon": "Eng_Strain[]",
                                               "sigma_true": "Sigma_true"})
        # Deduce and replace the times with microseconds
        system_time = pd.to_datetime(data['System Date'])
        time_with_microseconds = self.deduce_microseconds(system_time)
        first_time = time_with_microseconds[0].to_pydatetime()  # time of first measurement
        sample_rate = time_with_microseconds[1] - time_with_microseconds[0]
        start_time = first_time - sample_rate  # time that the recording started
        data['System Date'] = time_with_microseconds

        # Create the timed data object
        coupon_data = TimedData(data, start_time, sample_rate)
        return coupon_data

    def deduce_microseconds(self, system_time):
        """ Returns a Series of Timestamps with the deduced microseconds from available values. """
        # Find the first entry with microseconds not equal to zero
        set_micro_index = False
        for i, st in enumerate(system_time):
            t_micro_1 = st.microsecond
            if t_micro_1 != 0:
                set_micro_index = True
                st2 = system_time[i + 1]
                t_micro_2 = st2.microsecond
                dt = t_micro_2 - t_micro_1  # the timestep is assumed to be constant
                first_micro_index = i
                first_micro_time = st
                break

        # Exit with original times if no microseconds
        if not set_micro_index:
            warnings.warn('No microseconds in the data, time syncing will not be as accurate.')
            return system_time.copy()

        # Make sure all entries have microseconds
        system_time_micro = system_time.copy()
        # Adjust all the times before the first time with microseconds
        for i in range(first_micro_index):
            micro_second_diff = -(first_micro_index - i) * dt
            system_time_micro[i] = first_micro_time + datetime.timedelta(microseconds=micro_second_diff)
        # Adjust all the times after the first time with microseconds
        count_since_ref = 0
        ref_time = first_micro_time
        for i in range(first_micro_index, len(system_time)):
            if (system_time[i]).microsecond != 0:
                ref_time = system_time[i]
                count_since_ref = 0
            else:
                count_since_ref += 1
                micro_second_diff = count_since_ref * dt
                system_time_micro[i] = ref_time + datetime.timedelta(microseconds=micro_second_diff)
        return system_time_micro


def import_dion7_data(file):
    """ Returns a properly formatted TimedData object from the specified Excel input file.

    :param str file: Path to file in the specified Dion7 format.
    :return TimedData: Object containing the data from the input file.
    """
    reader = ExcelDion7Reader()
    return reader.read(file)


def import_catman_data(file):
    """ Returns a properly formatted TimedData object from the specified Excel input file.

    :param str file: Path to file in the specified catman format.
    :return TimedData: Object containing the data from the input file.
    """
    reader = ExcelCatmanReader()
    return reader.read(file)


def read_filter_info(file):
    """ Returns the info from the filter file.

    :param str file: Path to the filter file.
    :return dict: Information for filtering.
        list 'window': (int) Window lengths for each set.
        list 'poly_order': (int) Fit each window length with polynomial of order.
        list 'anchors': (list of int) Indices that must be included in the data.

    Notes:
        - If a poly_order is not provided in file then returns the default of 1
        - See protocols/readme.md for the specification on the filter_info.csv file.
    """
    line_mod = 2
    windows = []
    poly_orders = []
    anchors = []
    with open(file, 'r') as f:
        for i, line in enumerate(f):
            l_split = line.strip().split(',')
            if l_split[0] == '':
                # Skip empty lines
                pass
            elif i % line_mod == 0:
                # Even numbered line, so contains window lengths and poly orders
                windows.append(int(l_split[0]))
                try:
                    poly_orders.append(int(l_split[1]))
                except ValueError:
                    poly_orders.append(1)
            else:
                # Odd numbered line, contains anchor points
                anchors.append([int(x) for x in l_split])
    return {'window': windows, 'poly_order': poly_orders, 'anchors': anchors}


class DescriptionReader:
    """ Reads the specimen_description.csv file.

    Notes:
    - Lines with multiple values (e.g., pid_force) are assigned multiple entries starting with 0 to the number of
    values minus 1. Therefore, the line
        pid_force, p, i, d
    is parsed as pid_force_0: p, pid_force_1: i, pid_force_2: d.
    - The read method returns a pd.DataFrame object.
    - Each value is stored in the pd.DataFrame as one of the following types: datetime.date, float, str.
    - Lines starting with "#" will not be read
    """

    def __init__(self):
        """ Constructor, the allowable keywords are set here. """
        # Key = allowable keywords in the specimen description file, value = title of each keyword
        # If multiple values are expected for an entry, then place the value in a list
        self.accepted_inputs = collections.OrderedDict([
            ('steel_grade', 'Grade'),
            ('add_spec', 'Spec.'),
            ('specimen_source', 'Source'),
            ('specimen_id', 'ID'),
            ('load_protocol', 'LP'),
            ('outer_dia_n', 'Size'),
            ('gage_length_n', 'Gage Length [mm]'),
            ('reduced_dia_m', ['Avg. Reduced Dia. [mm]']),
            ('fy_n', 'fy_n [MPa]'),
            ('fu_n', 'fu_n [MPa]'),
            ('ambient_temp', 'T_a [deg C]'),
            ('date', 'Date'),
            ('personnel', 'Investigator'),
            ('location', 'Location'),
            ('setup', 'Machine'),
            ('pid_force', ['PID Force K_p', 'PID Force T_i', 'PID Force T_d']),
            ('pid_disp', ['PID Disp. K_p', 'PID Disp. T_i', 'PID Disp. T_d']),
            ('pid_extenso', ['PID Extenso. K_p', 'PID Extenso. T_i', 'PID Extenso. T_d']),
        ])
        self.multiple_inputs = ['pid_force', 'pid_disp', 'pid_extenso', 'reduced_dia_m']
        return

    def read(self, file):
        """ Returns the formatted information from the description file.

        :param str file: Path to the description file.
        :return pd.DataFrame: Info from the description file.
        """
        description = pd.DataFrame(dtype=object)
        allowable_keywords = self.accepted_inputs.keys()
        with open(file, 'r') as f:
            for line in f:
                if (line.strip() is not '') and (line.strip()[0] is not '#'):
                    # Allow commas (and semi-colons for excel users)
                    line_separated = line.replace(';', ',').split(',')
                    line_separated = [l.strip() for l in line_separated]  # remove whitespaces at the start and end
                    column = line_separated.pop(0)
                    data = line_separated
                    # Add the data if it's recognized
                    if column in allowable_keywords:
                        data_sanitized = self.sanitize_inputs(data)
                        if len(data_sanitized) == 1:
                            self.handle_single_data(description, column, data_sanitized)
                        else:
                            self.handle_multi_data(description, column, data_sanitized)
                    else:
                        warnings.warn(
                            'Description keyword "{0}" not recognized, I''m skipping this entry.'.format(column))

        return description

    def handle_single_data(self, description, column, data):
        """ Add entry to description that has only 1 value. """
        description[column] = data
        return

    def handle_multi_data(self, description, column, data):
        """ Add multiple entries to description from multiple values. """
        for i in range(len(data)):
            new_col = column + '_' + str(i)
            description[new_col] = data[i]
        return

    def sanitize_inputs(self, data):
        """ Ensure that the description entries are in the proper format. """
        try:
            # First try converting to a date
            # Ignore blank data entries
            dt = [datetime.datetime.strptime(d, '%d-%m-%Y') for d in data if d != '']
            data_san = [datetime.date(day=dti.day, month=dti.month, year=dti.year) for dti in dt]
        except ValueError:
            try:
                # Then try converting to a float
                data_san = [float(d) for d in data if d != '']
            except ValueError:
                # OK keep the string, but not emtpy values
                data_san = [d for d in data if d != '']
        return data_san

    def get_column_order(self):
        """ Returns the order of the keywords, including expanded multi-inputs, based on the accepted inputs.

        :return list: (str) Ordered keywords.

        Notes:
        - This function can be used to order the columns of a database.
        - The keywords for multiple inputs are expanded, e.g., pid_force -> pid_force_0, pid_force_1, pid_force_2
        """
        columns = list(self.accepted_inputs.keys())
        # Handle the keywords with multiple input values
        for mi in self.multiple_inputs:
            if mi[:3] == 'pid':
                num_multi = len(self.accepted_inputs[mi])
                if num_multi > 1:
                    i = columns.index(mi)
                    del columns[i]
                    columns[i:i] = [mi + '_' + str(j) for j in range(num_multi)]
            else:
                # This is a bit of a hack for the case where we have 3 diameter measurements and will not work if
                # we have more than three measurements for the diameter...
                num_multi = 3
                if num_multi > 1:
                    i = columns.index(mi)
                    del columns[i]
                    columns[i:i] = [mi + '_' + str(j) for j in range(num_multi)]
        return columns
