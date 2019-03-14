from unittest import TestCase
from rlmtp.readers import read_filter_info


class TestRead_filter_info(TestCase):
    def test_read_filter_info(self):
        filter_file = '../test_specimen/filter_info.csv'
        filter_info = read_filter_info(filter_file)

        self.assertEqual(filter_info['window'][0], 13)
        self.assertEqual(filter_info['poly_order'][0], 1)
        self.assertEqual(filter_info['anchors'], [[0, 776, 1478, 2480, 3834, 5504, 7532, 9871, 12556, 15236, 15397,
                                                   15535, 15697, 15860, 16055, 16243, 16486, 16699, 16939, 17178, 17454,
                                                   17718, 18059, 18348]])

    def test_read_filter_info_2_sets(self):
        filter_file = '../test_specimen/two_set_filter_info.csv'
        filter_info = read_filter_info(filter_file)

        self.assertEqual(filter_info['window'][0], 13)
        self.assertEqual(filter_info['window'][1], 50)

        self.assertEqual(filter_info['poly_order'][0], 1)
        self.assertEqual(filter_info['poly_order'][1], 2)

        self.assertEqual(filter_info['anchors'], [[0, 776, 1478, 2480, 3834, 5504, 7532, 9871, 12556, 15236, 15397,
                                                   15535, 15697],
                                                  [15860, 16055, 16243, 16486, 16699, 16939, 17178, 17454,
                                                   17718, 18059, 18348]])
