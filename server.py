from flask import Flask, render_template, jsonify, request
from jinja2 import StrictUndefined
import data

app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Homepage."""

    return render_template("home.html", brands=get_columns("Parent Brand"),
                           top_buy_rate_brand=data.top_buying_brand(),
                           retailers=get_columns("Retailer"))


def get_columns(column_name):
    items = data.df[column_name].unique()
    lst_of_items = []

    for item in items:
        lst_of_items.append(item)
    return lst_of_items


def get_rates():
    lst_of_rates = []
    brand_buy_rate = data.get_buy_rate_values()

    for brand in get_columns("Parent Brand"):
        lst_of_rates.append(brand_buy_rate[brand])

    return lst_of_rates

@app.route("/search.json")
def get_hh_count():
    brand = request.args.get("brand")
    retailer = request.args.get("retailer")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    hh_count = data.count_hhs(brand=brand, retailer=retailer, start_date=start_date,
                              end_date=end_date)

    return jsonify({"hh_count": hh_count})

@app.route("/affinity.json")
def get_affinity():
    brand = request.args.get("b")

    print brand

    affinity = data.get_retailer_affinity_values(brand)
    top_affinity = data.retailer_affinity(brand)

    return jsonify({"brand": brand, "affinity": affinity, "top_affinity": top_affinity})


@app.route("/buy-rate.json")
def buying_rates():
    """Return data about number of events."""

    # brands = data.df["Parent Brand"].unique()
    # lst_of_brands = []

    # for brand in brands:
    #     lst_of_brands.append(brand)
    # print brands

    # brand_buy_rate = data.get_buy_rate_values()
    # print brand_buy_rate

    # lst_of_rates = []

    # for brand in lst_of_brands:
    #     lst_of_rates.append(brand_buy_rate[brand])

    data_dict = {"labels": get_columns("Parent Brand"),
                 "datasets": [{"data": get_rates(),
                               "label": "Buying Rate ($ Spent / HH)",
                               "backgroundColor": ["#52D1DC",
                                                   "#475B5A",
                                                   "#8D8E8E",
                                                   "#A3A9AA"],
                               "hoverBackgroundColor": ["#52D1DC",
                                                        "#475B5A",
                                                        "#8D8E8E",
                                                        "#A3A9AA"]}]}

    return jsonify(data_dict)


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    app.run(port=5000, host="0.0.0.0")
