from unittest import TestCase
import os
from rlmtp.processing import process_specimen_data


class TestProcess_specimen_data(TestCase):
    def test_process_specimen_data(self):
        input_dir = '../test_specimen/'
        output_dir = '../output/test_specimen/'

        # Delete if file already exists
        if os.path.isfile('../output/test_specimen/test_specimen_processed_data.csv'):
            os.remove('../output/test_specimen/test_specimen_processed_data.csv')
        if os.path.isfile('../output/test_specimen/test_specimen_stress_strain_plot.pdf'):
            os.remove('../output/test_specimen/test_specimen_stress_strain_plot.pdf')
        if os.path.isfile('../output/test_specimen/test_specimen_temperature_time_plot.pdf'):
            os.remove('../output/test_specimen/test_specimen_temperature_time_plot.pdf')

        process_specimen_data(input_dir, output_dir)

        self.assertTrue(os.path.isfile('../output/test_specimen/test_specimen_processed_data.csv'))
        self.assertTrue(os.path.isfile('../output/test_specimen/test_specimen_stress_strain_plot.pdf'))
        self.assertTrue(os.path.isfile('../output/test_specimen/test_specimen_temperature_time_plot.pdf'))
        return

    def test_with_filtering(self):
        input_dir = '../test_specimen_3/'
        output_dir = '../output/test_specimen_3/'

        # Delete if file already exists
        if os.path.isfile('../output/test_specimen_3/test_specimen_3_processed_data.csv'):
            os.remove('../output/test_specimen_3/test_specimen_3_processed_data.csv')
        if os.path.isfile('../output/test_specimen_3/test_specimen_3_stress_strain_plot.pdf'):
            os.remove('../output/test_specimen_3/test_specimen_3_stress_strain_plot.pdf')

        process_specimen_data(input_dir, output_dir)

        self.assertTrue(os.path.isfile('../output/test_specimen_3/test_specimen_3_processed_data.csv'))
        self.assertTrue(os.path.isfile('../output/test_specimen_3/test_specimen_3_stress_strain_plot.pdf'))
        return

    def test_no_microsecond_data(self):
        input_dir = '../test_specimen_4/'
        output_dir = '../output/test_specimen_4/'

        # Delete if file already exists
        if os.path.isfile('../output/test_specimen_4/test_specimen_4_processed_data.csv'):
            os.remove('../output/test_specimen_4/test_specimen_4_processed_data.csv')
        if os.path.isfile('../output/test_specimen_4/test_specimen_4_stress_strain_plot.pdf'):
            os.remove('../output/test_specimen_4/test_specimen_4_stress_strain_plot.pdf')

        process_specimen_data(input_dir, output_dir)

        self.assertTrue(os.path.isfile('../output/test_specimen_4/test_specimen_4_processed_data.csv'))
        self.assertTrue(os.path.isfile('../output/test_specimen_4/test_specimen_4_stress_strain_plot.pdf'))
        return
