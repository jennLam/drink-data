import unittest
import pandas as pd
import operator as op
import pandas.util.testing as pdt
from data import InfoScoutData


class TestCase(unittest.TestCase):

    # Create instance with test data
    test_isd = InfoScoutData("testing_data.csv")

    def test_search_criteria(self):
        """Test for search_criteria."""

        expected = pd.Series([True, False, False, False, False, False, True,
                             True, False, False, False, False, False, False,
                             False, False, True, True, False, False, False, True,
                             True, False], name='Parent Brand', dtype='bool')
        actual = self.test_isd.search_criteria("Parent Brand", "Monster", op.eq)

        pdt.assert_series_equal(expected, actual)

    def test_get_total_units(self):
        """Test for get_total_units."""

        self.assertEqual(self.test_isd.get_total_units(), 40)
        self.assertEqual(self.test_isd.get_total_units("Monster"), 11)
        self.assertEqual(self.test_isd.get_total_units(retailer="Walmart"), 9)
        self.assertEqual(self.test_isd.get_total_units("Monster", "Walmart"), 5)
        self.assertEqual(self.test_isd.get_total_units("Water"), 0)

    def test_calc_affinity(self):
        """Test for calc_affinity."""

        self.assertEqual(self.test_isd.calc_affinity("Monster", "Walmart"), 2.02)
        self.assertEqual(self.test_isd.calc_affinity("Monster", "Subway"), 0)
        self.assertEqual(self.test_isd.calc_affinity("Water", "Walmart"), 0)
        self.assertEqual(self.test_isd.calc_affinity("Water", "Subway"), 0)

    def test_get_retailer_affinity_values(self):
        """Test for get_retailer_affinity_values."""

        expected_for_monster = {'CVS': 0, 'Costco': 0, 'Kroger': 0.64, 'Publix': 0,
                                'Target': 2.73, 'Walgreens': 0, 'Walmart': 2.02}
        expected_for_water = {'CVS': 0, 'Costco': 0, 'Kroger': 0, 'Publix': 0,
                              'Target': 0, 'Walgreens': 0, 'Walmart': 0}

        self.assertEqual(self.test_isd.get_retailer_affinity_values("Monster"), expected_for_monster)
        self.assertEqual(self.test_isd.get_retailer_affinity_values("Water"), expected_for_water)

    def test_get_dict_max(self):
        """Test for get_dict_max."""

        test_dict1 = {'apple': 5, 'berry': 78, 'cherry': 39, 'durian': 20}
        test_dict2 = {'apple': 5, 'berry': 30, 'cherry': 19, 'durian': 30}

        td2_results = self.test_isd.get_dict_max(test_dict2)
        td2_results.sort()

        self.assertEqual(self.test_isd.get_dict_max(test_dict1), ['berry'])
        self.assertEqual(td2_results, ['berry', 'durian'])

    def test_retailer_affinity(self):
        """Test for retailer_affinity."""

        rockstar_results = self.test_isd.retailer_affinity("Rockstar")
        rockstar_results.sort()

        self.assertEqual(self.test_isd.retailer_affinity("Monster"), ['Target'])
        self.assertEqual(rockstar_results, ['CVS', 'Costco'])
        self.assertEqual(self.test_isd.retailer_affinity("Water"), None)

    def test_count_hhs(self):
        """Test for count_hhs."""

        self.assertEqual(self.test_isd.count_hhs(start_date="1/3/14"), 5)
        self.assertEqual(self.test_isd.count_hhs(start_date="1/3/14", end_date="1/1/15"), 3)
        self.assertEqual(self.test_isd.count_hhs("Monster"), 6)
        self.assertEqual(self.test_isd.count_hhs(retailer="Walmart"), 6)
        self.assertEqual(self.test_isd.count_hhs("Monster", "Walmart"), 2)
        self.assertEqual(self.test_isd.count_hhs("Red Bull", "Kroger", "1/1/14"), 1)
        self.assertEqual(self.test_isd.count_hhs("Water"), 0)

    def test_calc_buy_rate(self):
        """Test for calc_buy_rate."""

        self.assertEqual(self.test_isd.calc_buy_rate("Monster"), 4.5)
        self.assertEqual(self.test_isd.calc_buy_rate("Water"), 0)

    def test_get_buy_rate_values(self):
        """Test for get_buy_rate_values."""

        expected = {'5 Hour Energy': 7.0, 'Monster': 4.5, 'Red Bull': 4.14, 'Rockstar': 24.0}

        self.assertEqual(self.test_isd.get_buy_rate_values(), expected)

    def test_top_buying_brand(self):
        """Test for top_buying_brand."""

        self.assertEqual(self.test_isd.top_buying_brand(), ['Rockstar'])


if __name__ == "__main__":
    unittest.main()
