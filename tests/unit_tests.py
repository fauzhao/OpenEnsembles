import os.path
import time
import unittest
import random
import pandas as pd

import openensembles as oe

class TestFunctions(unittest.TestCase):

    def setUp(self):
        fileName = 'data_test.csv'
        df = pd.DataFrame.from_csv(fileName)
        x = [0, 5, 30]
        self.data = oe.data(df, x)

    def test_correct_setup(self):
        self.assertEqual((3,3), self.data.D['parent'].shape)
        self.assertEqual(3, len(self.data.x['parent']))

    def test_incorrect_setup(self):
        fileName = 'data_test.csv'
        df = pd.DataFrame.from_csv(fileName)
        x = [0, 5, 10, 30]
        data = oe.data(df, x)
        self.assertEqual((3,3), data.D['parent'].shape)
        self.assertEqual(3, len(data.x['parent']))

    def test_transform_error_noSource(self):
        self.assertEqual(-1, self.data.transform('parentZ', 'zscore', 'zscore_parentZ'))

    def test_transform_NoNaNs(self):
        self.assertEqual(-3, self.data.transform('parent', 'zscore', 'zscore', Keep_NaN=0))
        self.assertEqual(1, len(self.data.D))

    def test_transform_error_noTxfm(self):
        self.assertEqual(-2, self.data.transform('parent', 'zscoreGobblyGoodk', 'zscore_parent'))

    def test_transform(self):
        #check to see that a new entry in D, x and params are added for every
        #transform available
        TXFM_FCN_DICT = self.data.transforms_available()
        len_expected = 2
        for transform in TXFM_FCN_DICT:
            self.data.transform('parent', transform, transform)
            self.assertEqual(len_expected, len(self.data.D))
            self.assertEqual(len_expected, len(self.data.x))
            self.assertEqual(len_expected, len(self.data.params))
            len_expected += 1

