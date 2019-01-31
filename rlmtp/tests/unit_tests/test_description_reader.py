from unittest import TestCase
import datetime
import warnings
from rlmtp.readers import DescriptionReader


class TestDescription_reader(TestCase):
    def test_description_reader(self):
        file = '../specimen_description_standard.csv'
        reader = DescriptionReader()
        result = reader.read(file)

        self.assertTrue(result['pid_force_0'][0] == '[p]')

    def test_real_data(self):
        file = '../test_specimen/specimen_description.csv'
        reader = DescriptionReader()
        result = reader.read(file)

        self.assertTrue(result['pid_force_0'][0] == 0.21)
        self.assertTrue(result['steel_grade'][0] == 'S355')
        self.assertTrue(result['date'][0] == datetime.date(month=1, day=7, year=2019))

    def test_bad_entry(self):
        file = '../specimen_description_bad.csv'
        reader = DescriptionReader()
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            reader.read(file)
            assert issubclass(w[-1].category, UserWarning)

    def test_get_columns(self):
        reader = DescriptionReader()
        x = reader.get_column_order()
        y = reader.accepted_inputs.keys()
        count = len(y) + 2 * len(reader.multiple_inputs)  # assumes 3 values per multiple input
        self.assertTrue(len(x) == count)
        self.assertTrue(x[0] == 'steel_grade')
        self.assertTrue(x[-1] == 'pid_extenso_2')
