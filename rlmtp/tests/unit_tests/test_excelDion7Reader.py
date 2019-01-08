from unittest import TestCase
from rlmtp import ExcelDion7Reader, ExcelCatmanReader


class TestExcelDion7Reader(TestCase):

    def test_sys_time(self):
        reader = ExcelDion7Reader()
        data = reader.read('../LP9_1_181211.xlsx')
        x = data.data['System Date']
        self.assertEqual(x[0].microsecond, 723000)


class TestExcelCatmanReader(TestCase):

    def test_sys_time(self):
        reader = ExcelCatmanReader()
        data = reader.read('../Temp_LP9_1_181211.XLSX')
        x = data.data['System Date']
        self.assertEqual(x[0].microsecond, 0)
