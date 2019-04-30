from unittest import TestCase
import numpy as np
import matplotlib.pyplot as plt
from rlmtp.filtering import reduce_data, clean_data
from rlmtp.readers import import_dion7_data


class TestClean_test_data(TestCase):
    def test_reduce_data(self):
        data_path = '../testData_07012018.xlsx'
        dion7_data = import_dion7_data(data_path)
        ind = [1, 777, 1479, 2481, 3835, 5505, 7533, 9872, 12557, 15237, 15398, 15536, 15698, 15861, 16056, 16244,
               16487, 16700, 16940, 17179, 17455, 17719, 18060, 18349]
        ind = [x - 1 for x in ind]
        window = int(np.floor(np.min(np.abs(np.diff(ind)) / 10)))
        print(window)
        print(ind)
        t = np.array(range(0, len(dion7_data.data['e_true'])))
        clean_data = reduce_data(dion7_data.data['e_true'], dion7_data.data['Sigma_true'], t, ind, window)
        print('Length orig = {0}, length new = {1}'.format(len(dion7_data.data['e_true']), len(clean_data[0])))

        # plt.figure()
        # plt.plot(dion7_data.data['e_true'], dion7_data.data['Sigma_true'])
        # plt.plot(clean_data[0], clean_data[1])
        # plt.show()

        self.assertEqual(len(clean_data[0]), 2847)

    def test_clean_data(self):
        data_path = '../testData_07012018.xlsx'
        dion7_data = import_dion7_data(data_path)
        window = [13, 13]
        poly_order = [1, 1]
        inds = [[0, 776, 1478, 2480, 3834, 5504, 7532, 9871, 12556, 15236, 15397, 15535, 15697],
                [15860, 16055, 16243, 16486, 16699, 16939, 17178, 17454, 17718, 18059, 18348]]

        filter_info = {'anchors': inds, 'window': window, 'poly_order': poly_order}
        cleaned_data = clean_data(dion7_data.data, filter_info)

        # plt.figure()
        # plt.plot(dion7_data.data['e_true'], dion7_data.data['Sigma_true'])
        # plt.plot(cleaned_data['e_true'], cleaned_data['Sigma_true'])
        # plt.show()

        self.assertEqual(len(cleaned_data['e_true']), 2847)
