from unittest import TestCase
import os
from rlmtp.processing import process_specimen_data


class TestProcess_specimen_data(TestCase):
    def test_process_specimen_data(self):
        input_dir = '../test_specimen/'
        output_dir = '../output/'

        # Delete if file already exists
        if os.path.isfile('../output/test_specimen/processed_data.csv'):
            os.remove('../output/test_specimen/processed_data.csv')
        if os.path.isfile('../output/test_specimen/stress_strain_plot.pdf'):
            os.remove('../output/test_specimen/stress_strain_plot.pdf')
        if os.path.isfile('../output/test_specimen/temperature_strain_plot.pdf'):
            os.remove('../output/test_specimen/temperature_strain_plot.pdf')

        process_specimen_data(input_dir, output_dir)

        self.assertTrue(os.path.isfile('../output/test_specimen/processed_data.csv'))
        self.assertTrue(os.path.isfile('../output/test_specimen/stress_strain_plot.pdf'))
        self.assertTrue(os.path.isfile('../output/test_specimen/temperature_strain_plot.pdf'))
        return
