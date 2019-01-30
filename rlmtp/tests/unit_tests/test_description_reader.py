from unittest import TestCase
import datetime
import warnings
from rlmtp.readers import DescriptionReader


class TestDescription_reader(TestCase):
    def test_description_reader(self):
        file = '../specimen_description_test.csv'
        reader = DescriptionReader(file)
        result = reader.read()

        self.assertTrue(result['pid_force_0'][0] == '[p]')

    def test_real_data(self):
        file = '../test_specimen/specimen_description.csv'
        reader = DescriptionReader(file)
        result = reader.read()

        self.assertTrue(result['pid_force_0'][0] == 0.21)
        self.assertTrue(result['steel_grade'][0] == 'S355')
        self.assertTrue(result['date'][0] == datetime.date(month=1, day=7, year=2019))

    def test_bad_entry(self):
        file = '../specimen_description_bad.csv'
        reader = DescriptionReader(file)
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            reader.read()
            assert issubclass(w[-1].category, UserWarning)
