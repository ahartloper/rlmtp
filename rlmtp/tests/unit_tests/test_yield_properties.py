from unittest import TestCase
import pandas as pd
from rlmtp.yield_properties import yield_properties


class TestYieldProperties(TestCase):
    def test_tensile_data(self):
        data = pd.read_csv('../yield_props_examples/example_3.csv')
        res = yield_properties(data)
        self.assertAlmostEqual(res[0], 205900.33785255413, 2)
        self.assertAlmostEqual(res[1], 3.16577548e+02, 2)
        pass

    def test_compression_loading(self):
        data = pd.read_csv('../yield_props_examples/example_3.csv')
        data['e_true'] = -1. * data['e_true']
        data['Sigma_true'] = -1. * data['Sigma_true']
        res = yield_properties(data)
        self.assertAlmostEqual(res[0], 205900.33785255413, 2)
        self.assertAlmostEqual(res[1], 3.16577548e+02, 2)
        pass
