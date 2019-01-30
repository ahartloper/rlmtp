import pandas as pd
import datetime
import warnings
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

    def __init__(self, start_row=7):
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
        for i, st in enumerate(system_time):
            t_micro_1 = st.microsecond
            if t_micro_1 != 0:
                st2 = system_time[i + 1]
                t_micro_2 = st2.microsecond
                dt = t_micro_2 - t_micro_1  # the timestep is assumed to be constant
                first_micro_index = i
                first_micro_time = st
                break
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
    :return dict: Contains: 'window', 'poly_order', 'anchors'

    - If a poly_order is not provided in file then returns the default of 1
    """
    with open(file, 'r') as f:
        line = f.readline().split(',')
        window = int(line[0])
        try:
            poly_order = int(line[1])
        except ValueError:
            poly_order = 1
        line = f.readline().split(',')
        anchors = [int(x) for x in line]
    return {'window': window, 'poly_order': poly_order, 'anchors': anchors}


class DescriptionReader:
    """ Reads the specimen_description.csv file. """

    def __init__(self, file):
        """ Constructor.

        :param str file: Path to the description file.
        """
        self.file = file
        self.description = pd.DataFrame(dtype=object)

        self.accepted_inputs = ['steel_grade', 'add_spec', 'fy_n', 'fu_n', 'specimen_id', 'specimen_source',
                                'outer_dia_n', 'gage_length_n', 'reduced_dia_m', 'pid_force', 'pid_disp', 'pid_extenso',
                                'date', 'personnel', 'location', 'setup', 'ambient_temp']
        return

    def read(self):
        """ Returns the formatted information from the description file.

        :return pd.DataFrame: Info from the description file.
        """
        with open(self.file, 'r') as f:
            for line in f:
                if line.strip() is not '':
                    line_separated = line.split(',')
                    line_separated = [l.strip() for l in line_separated]  # remove whitespaces at the start and end
                    column = line_separated.pop(0)
                    data = line_separated
                    # Add the data if it's recognized
                    if column in self.accepted_inputs:
                        data_sanitized = self.sanitize_inputs(data)
                        if len(data) == 1:
                            self.handle_single_data(column, data_sanitized)
                        else:
                            self.handle_multi_data(column, data_sanitized)
                    else:
                        warnings.warn(
                            'Description keyword "{0}" not recognized, I''m skipping this entry.'.format(column))

        return self.description

    def handle_single_data(self, column, data):
        """ Add entry to description that has only 1 value. """
        self.description[column] = data
        return

    def handle_multi_data(self, column, data):
        """ Add multiple entries to description from multiple values. """
        for i in range(len(data)):
            new_col = column + '_' + str(i)
            self.description[new_col] = data[i]
        return

    def sanitize_inputs(self, data):
        """ Ensure that the description entries are in the proper format. """
        try:
            # First try converting to a date
            dt = [datetime.datetime.strptime(d, '%d-%m-%Y') for d in data]
            data_san = [datetime.date(day=dti.day, month=dti.month, year=dti.year) for dti in dt]
        except ValueError:
            try:
                # Then try converting to a float
                data_san = [float(d) for d in data]
            except ValueError:
                # OK keep the string
                data_san = data
        return data_san
