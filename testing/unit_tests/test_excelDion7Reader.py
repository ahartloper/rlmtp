from unittest import TestCase
from timed_data import ExcelDion7Reader, ExcelCatmanReader


class TestExcelDion7Reader(TestCase):
    reader = ExcelDion7Reader()
    data = reader.read('../LP9_1_181211.xlsx')
    x = data.data['System Date']

    pass


class TestExcelCatmanReader(TestCase):
    reader = ExcelCatmanReader()
    data = reader.read('../Temp_LP9_1_181211.XLSX')
    x = data.data['System Date']

    pass

