from unittest import TestCase
import os
from rlmtp.readers import ExcelDion7Reader
from rlmtp.sync_video import dion7_times_to_video_times, output_frames_at_times


# These tests will fail if ../D5600_B_254_132139_589.MOV does not exist, however the file is not included because 1 GB
class TestDion7_times_to_video_times(TestCase):
    def test_dion7_times_to_video_times(self):
        reader = ExcelDion7Reader()
        dion_data = reader.read('../testData_07012018.xlsx')

        times = dion_data.data['System Date']
        time_55_strain = [times[18059]]
        video = '../D5600_B_254_132139_589.MOV'
        video_times = dion7_times_to_video_times(video, time_55_strain)

        self.assertLess(abs(video_times[0] - 916.), 1.)
        return

    def test_bad_video_times(self):
        reader = ExcelDion7Reader()
        dion_data = reader.read('../LP9_1_181211.xlsx')

        times = dion_data.data['System Date']
        video = '../D5600_B_254_132139_589.MOV'
        video_times = dion7_times_to_video_times(video, times)
        self.assertFalse(video_times)

    def test_print_frames(self):
        # Delete if file already exists
        if os.path.isfile('../output/s355_web_test_916_394.jpg'):
            os.remove('../output/s355_web_test_916_394.jpg')

        reader = ExcelDion7Reader()
        dion_data = reader.read('../testData_07012018.xlsx')

        time_55_strain = dion_data.get_times_at_increments([18059])
        video = '../D5600_B_254_132139_589.MOV'
        video_times = dion7_times_to_video_times(video, time_55_strain)
        output_frames_at_times(video, video_times, '../output/', 's355_web_test')

        self.assertTrue(os.path.isfile('../output/s355_web_test_916_394.jpg'))
