from unittest import TestCase
from rlmtp.construct_database import construct_description_database, write_description_database_csv


class TestConstruct_database(TestCase):
    def test_1_entry(self):
        dir = '../test_specimen/'
        database = construct_description_database(dir)
        self.fail()

    def test_make_database(self):
        dir = '../test_database/'
        database = construct_description_database(dir)
        self.fail()

    def test_write_database(self):
        dir = '../test_database/'
        output = '../output/description_database_test.csv'
        write_description_database_csv(dir, output)
