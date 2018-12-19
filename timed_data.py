import pandas as pd
import datetime


class TimedData:
    """ Time series data, has a column named 'System Date' with the computer time for every entry. """

    def __init__(self, data, start_time, sample_rate_ms):
        """ Constructor.

        :param pd.Dataframe data: Measured data, includes the column 'System Date'.
        :param datetime.datetime start_time: Time that the recording started.
        :param datetime.timedelta sample_rate_ms: Sampling rate in milliseconds.

        - System Date contains pd.Timestamp's with the time to the millisecond of each measurement.
        """
        self.start_time = start_time
        self.data = data
        self.sample_rate_ms = sample_rate_ms


class ExcelCatmanReader:

    def __init__(self, start_row=1):
        self.header_rows = start_row

    def read(self, file):
        # Import the data and remove the unncessary rows
        data = pd.read_excel(file, header=self.header_rows)
        col_1 = data.columns[0]
        start_time = datetime.datetime.strptime(data[col_1][2], '%m.%d.%y %H:%M:%S')
        data.drop(range(47), inplace=True)
        data.reset_index(drop=True, inplace=True)
        # Rename the columns
        col_new_name = ['Time[s]', 'Force[kN]', 'Extenso[mm]', 'Temperature[C]']
        data = data.rename(index=str, columns=dict(zip(data.columns, col_new_name)))
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


class ExcelDion7Reader:
    # this will return a TimedData object properly formatted

    def __init__(self, start_row=7):
        self.header_rows = start_row - 2
        return

    def read(self, file):
        data = pd.read_excel(file, header=self.header_rows)
        # data.drop('S/No', inplace=True)
        data = data.rename(index=str, columns={"sigma [Mpa]": "Eng_Stress[MPa]", "epsilon": "Eng_Strain[]",
                                               "sigma_true": "Sigma_true"})
        # Deduce and replace the times with microseconds
        system_time = data['System Date']
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
