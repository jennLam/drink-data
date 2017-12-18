import pandas as pd
import operator as op


class InfoScoutData(object):

    def __init__(self, location):
        self.location = location
# location = "trips_gdrive.csv"
        self.df = pd.read_csv(location)

        # Format columns in dataframe (convert date to datetime and dollars to int).
        self.df["Date"] = pd.to_datetime(self.df["Date"], format="%m/%d/%Y")
        self.df["Item Dollars"] = self.df["Item Dollars"].replace({"\$": ""}, regex=True)
        self.df["Item Dollars"] = pd.to_numeric(self.df["Item Dollars"])

    def search_criteria(self, column_name, target, operator):
        """Specify search condition for dataframe."""

        if column_name not in list(self.df):
            return

        result = None

        if target:
            result = operator(self.df[column_name], target)
        else:
            result = self.df[column_name] is not None

        return result

    def get_total_units(self, brand=None, retailer=None):
        """Returns the total number of item units for specific retailer and/or brand."""

        condition = self.df

        if brand or retailer:
            b = self.search_criteria("Parent Brand", brand, op.eq)
            r = self.search_criteria("Retailer", retailer, op.eq)

            condition = self.df[b & r]

        return condition["Item Units"].sum()

    def calc_affinity(self, brand, retailer):
        """Calculate retailer affinity index for brand."""

        # P(A U B) / P(A) * P(B) * 100
        # P(A) is the % of item units of brand purchased
        # P(B) is the % of item units of retailer purchased
        # P(A U B) is the % of item units of brand and retailer purchased

        pab = float(self.get_total_units(brand, retailer))/self.get_total_units() * 100
        pa = float(self.get_total_units(brand=brand))/self.get_total_units() * 100
        pb = float(self.get_total_units(retailer=retailer))/self.get_total_units() * 100

        affinity_index = round(pab/(pa * pb) * 100, 2)

        # If the affinity index is not a number (nan), set affinity index to 0
        if affinity_index != affinity_index:
            affinity_index = 0

        return affinity_index

    def get_retailer_affinity_values(self, brand):
        """Create a dictionary of retailer affinity indices for a brand."""

        retailer_affinity_dict = {}

        for retailer in self.df["Retailer"].unique():
            retailer_affinity_dict[retailer] = self.calc_affinity(brand, retailer)

        return retailer_affinity_dict

    def get_dict_max(self, dictionary):
        """Return a list of keys for the max value."""

        max_keys_lst = []

        max_value = max(dictionary.values())

        for key, value in dictionary.items():
            if value == max_value:
                max_keys_lst.append(key)

        return max_keys_lst

    def retailer_affinity(self, focus_brand):
        """Return the strongest retailer affinity for focus brand relative to other brands."""

        if focus_brand not in self.df["Parent Brand"].unique():
            return None

        retailer_affinity_dict = self.get_retailer_affinity_values(focus_brand)

        return self.get_dict_max(retailer_affinity_dict)

    def count_hhs(self, brand=None, retailer=None, start_date=None, end_date=None):
        """Return number of households."""

        condition = self.df

        if brand or retailer or start_date or end_date:

            b = self.search_criteria("Parent Brand", brand, op.eq)
            r = self.search_criteria("Retailer", retailer, op.eq)
            sd = self.search_criteria("Date", start_date, op.ge)
            ed = self.search_criteria("Date", end_date, op.le)

            condition = self.df[b & r & sd & ed]

        # Household determined by User ID
        # Each User ID is a household

        return len(condition["User ID"].unique())

    def calc_buy_rate(self, brand):
        """Return the buying rate for a brand."""

        dollars_spent = self.df[self.df["Parent Brand"] == brand]["Item Dollars"].sum()
        household = self.count_hhs(brand)

        # Buying rate calculated by:
        # Total dollars spent buying brand items / Total household that bought brand items

        return round(float(dollars_spent)/household, 2)

    def get_buy_rate_values(self):
        """Create a dictionary of brands and buying rates."""

        brand_buy_rate_dict = {}

        for brand in self.df["Parent Brand"].unique():
            brand_buy_rate_dict[brand] = self.calc_buy_rate(brand)

        return brand_buy_rate_dict

    def top_buying_brand(self):
        """Identify brand with top buying rate."""

        brand_buy_rate_dict = self.get_buy_rate_values()

        return self.get_dict_max(brand_buy_rate_dict)
