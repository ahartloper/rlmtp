from unittest import TestCase
from timed_data import ExcelDion7Reader
from sync_video import dion7_times_to_video_times


class TestDion7_times_to_video_times(TestCase):
    def test_dion7_times_to_video_times(self):
        reader = ExcelDion7Reader()
        dion_data = reader.read('../LP9_1_181211.xlsx')

        times = dion_data.data['System Date']
        video = 'D:\\D5600_B_245_145701_925.MOV'
        video_times = dion7_times_to_video_times(video, times)
        print(video_times)

        pass

    def test_bad_video_times(self):
        reader = ExcelDion7Reader()
        dion_data = reader.read('../LP9_1_181211.xlsx')

        times = dion_data.data['System Date']
        video = 'D:\\D5600_B_254_132139_589.MOV'
        video_times = dion7_times_to_video_times(video, times)
        # Should raise warning about incompatible times.
        pass
