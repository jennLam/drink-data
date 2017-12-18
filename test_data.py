import unittest
import pandas as pd
import operator as op
import pandas.util.testing as pdt
from data import InfoScoutData


class TestCase(unittest.TestCase):

    test_isd = InfoScoutData("test.csv")

    def test_search_criteria(self):
        expected = pd.Series([True, False, False, False], name='Parent Brand', dtype='bool')

        actual = self.test_isd.search_criteria("Parent Brand", "Monster", op.eq)

        pdt.assert_series_equal(expected, actual)

if __name__ == "__main__":
    unittest.main()



