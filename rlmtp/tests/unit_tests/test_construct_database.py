from unittest import TestCase
import os
from rlmtp.construct_database import construct_description_database, write_description_database_csv


class TestConstruct_database(TestCase):

    def test_make_database(self):
        dir = '../test_database/'
        database = construct_description_database(dir)
        self.assertTrue('C12' in list(database['ID']))
        self.assertTrue('D2' in list(database['ID']))
        self.assertTrue(database['PID Force T_i'][1] == 0.26)

    def test_write_database(self):
        dir = '../test_database/'
        output = '../output/description_database_test.csv'
        if os.path.isfile(output):
            os.remove(output)
        write_description_database_csv(dir, output)
        self.assertTrue(os.path.isfile(output))
