import pandas as pd
import operator as op

location = "trips_gdrive.csv"

df = pd.read_csv(location)

df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")

# remove dollar signs
df["Item Dollars"] = df["Item Dollars"].replace({"\$": ""}, regex=True)

# convert to int
df["Item Dollars"] = pd.to_numeric(df["Item Dollars"])


def search_criteria(column_name, target, operator):
    """Specify search condition for dataframe."""

    result = None

    if target:
        result = operator(df[column_name], target)
    else:
        result = df[column_name] is not None

    return result


def get_total_units(brand=None, retailer=None):
    """Returns the total number of item units for specific retailer and/or brand."""

    condition = df

    if brand or retailer:
        b = search_criteria("Parent Brand", brand, op.eq)
        r = search_criteria("Retailer", retailer, op.eq)

        condition = df[b & r]

    return condition["Item Units"].sum()


def calc_affinity(brand, retailer):
    """Calculate retailer affinity index for brand."""

    # P(A U B) / P(A) * P(B) * 100
    # P(A) is the % of item units of brand purchased
    # P(B) is the % of item units of retailer purchased
    # P(A U B) is the % of item units of brand and retailer purchased

    pab = float(get_total_units(brand, retailer))/get_total_units() * 100
    pa = float(get_total_units(brand=brand))/get_total_units() * 100
    pb = float(get_total_units(retailer=retailer))/get_total_units() * 100

    affinity_index = round(pab/(pa * pb) * 100, 2)

    # If the affinity index is not a number (nan), set affinity index to 0
    if affinity_index != affinity_index:
        affinity_index = 0

    return affinity_index


def get_retailer_affinity_values(brand):
    """Create a dictionary of retailer affinity indices for a brand."""

    retailer_affinity_dict = {}

    for retailer in df["Retailer"].unique():
        retailer_affinity_dict[retailer] = calc_affinity(brand, retailer)

    return retailer_affinity_dict


def get_dict_max(dictionary):
    """Return a list of keys for the max value."""

    max_keys_lst = []

    max_value = max(dictionary.values())

    for key, value in dictionary.items():
        if value == max_value:
            max_keys_lst.append(key)

    return max_keys_lst


def retailer_affinity(focus_brand):
    """Return the strongest retailer affinity for focus brand relative to other brands."""

    retailer_affinity_dict = get_retailer_affinity_values(focus_brand)

    return get_dict_max(retailer_affinity_dict)


def count_hhs(brand=None, retailer=None, start_date=None, end_date=None):
    """Return number of households."""

    condition = df

    if brand or retailer or start_date or end_date:

        b = search_criteria("Parent Brand", brand, op.eq)
        r = search_criteria("Retailer", retailer, op.eq)
        sd = search_criteria("Date", start_date, op.ge)
        ed = search_criteria("Date", end_date, op.le)

        condition = df[b & r & sd & ed]

    # Household determined by User ID
    # Each User ID is a household

    return len(condition["User ID"].unique())


def calc_buy_rate(brand):
    """Return the buying rate for a brand."""

    dollars_spent = df[df["Parent Brand"] == brand]["Item Dollars"].sum()
    household = count_hhs(brand)

    # Buying rate calculated by:
    # Total dollars spent buying brand items / Total household that bought brand items

    return round(float(dollars_spent)/household, 2)


def get_buy_rate_values():
    """Create a dictionary of brands and buying rates."""

    brand_buy_rate_dict = {}

    for brand in df["Parent Brand"].unique():
        brand_buy_rate_dict[brand] = calc_buy_rate(brand)

    return brand_buy_rate_dict


def top_buying_brand():
    """Identify brand with top buying rate."""

    brand_buy_rate_dict = get_buy_rate_values()

    return get_dict_max(brand_buy_rate_dict)
