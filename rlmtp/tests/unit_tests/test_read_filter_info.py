from unittest import TestCase
from rlmtp.readers import read_filter_info


class TestRead_filter_info(TestCase):
    def test_read_filter_info(self):
        filter_file = '../test_specimen/filter_info.csv'
        filter_info = read_filter_info(filter_file)

        self.assertTrue(filter_info['window'], 13)
        self.assertTrue(filter_info['poly_order'], 1)
        self.assertTrue(filter_info['anchors'], [0, 776, 1478, 2480, 3834, 5504, 7532, 9871, 12556, 15236, 15397,
                                                 15535, 15697, 15860, 16055, 16243, 16486, 16699, 16939, 17178, 17454,
                                                 17718, 18059, 18348])
