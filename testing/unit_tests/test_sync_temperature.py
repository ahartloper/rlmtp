from unittest import TestCase
from timed_data import ExcelDion7Reader, ExcelCatmanReader
from sync_temperature import sync_temperature


class TestSync_temperature(TestCase):
    def test_sync_temperature(self):
        reader = ExcelDion7Reader()
        dion_data = reader.read('../LP9_1_181211.xlsx')
        reader = ExcelCatmanReader()
        catman_data = reader.read('../Temp_LP9_1_181211.XLSX')
        synced_data = sync_temperature(dion_data, catman_data)

        self.fail()
