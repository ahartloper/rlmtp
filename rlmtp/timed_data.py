"""@package timed_data
Object to store data that starts at a specific time and has a specific sampling rate.

TimedData objects are generally used to store temperature and stress-strain data.
"""

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

    def get_times_at_increments(self, inc):
        """ Returns the System Date corresponding to the provided time increments.

        :param list inc: Zero-indexed time increments in self.data
        :return list: (datetime.datetime) Corresponding entries in System Date.
        """
        t = []
        for ti in inc:
            t.append(self.data['System Date'][ti])
        return t


