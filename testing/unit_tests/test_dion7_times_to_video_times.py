from unittest import TestCase
from timed_data import ExcelDion7Reader
from sync_video import dion7_times_to_video_times, output_frames_at_times


class TestDion7_times_to_video_times(TestCase):
    def test_dion7_times_to_video_times(self):
        reader = ExcelDion7Reader()
        dion_data = reader.read('D:\\Cygwin_root\\home\\hartlope\\Documents\\RLMTP\\testing\\testData_07012018.xlsx')

        times = dion_data.data['System Date']
        time_55_strain = [times[18059]]
        video = 'D:\\D5600_B_254_132139_589.MOV'
        video_times = dion7_times_to_video_times(video, time_55_strain)

        self.assertLess(abs(video_times[0] - 916.), 1.)
        return

    def test_bad_video_times(self):
        reader = ExcelDion7Reader()
        dion_data = reader.read('../LP9_1_181211.xlsx')

        times = dion_data.data['System Date']
        video = 'D:\\D5600_B_254_132139_589.MOV'
        video_times = dion7_times_to_video_times(video, times)
        # Should raise warning about incompatible times.
        pass

    def test_print_frames(self):
        reader = ExcelDion7Reader()
        dion_data = reader.read('D:\\Cygwin_root\\home\\hartlope\\Documents\\RLMTP\\testing\\testData_07012018.xlsx')

        time_55_strain = dion_data.get_times_at_increments([18059])
        video = 'D:\\D5600_B_254_132139_589.MOV'
        video_times = dion7_times_to_video_times(video, time_55_strain)
        output_frames_at_times(video, video_times,
                               'D:\\Cygwin_root\\home\\hartlope\\Documents\\RLMTP\\testing\\output\\',
                               's355_web_test')
        return
