from flask import Flask, render_template, jsonify, request
from jinja2 import StrictUndefined
import json
import data

app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Homepage."""

    return render_template("home.html", brands=get_brands(),
                           top_buy_rate_brand=data.top_buying_brand())


def get_brands():
    brands = data.df["Parent Brand"].unique()
    lst_of_brands = []

    for brand in brands:
        lst_of_brands.append(brand)
    return lst_of_brands


def get_rates():
    lst_of_rates = []
    brand_buy_rate = data.get_buy_rate_values()

    for brand in get_brands():
        lst_of_rates.append(brand_buy_rate[brand])

    return lst_of_rates


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

    brands = data.df["Parent Brand"].unique()
    lst_of_brands = []

    for brand in brands:
        lst_of_brands.append(brand)
    print brands

    brand_buy_rate = data.get_buy_rate_values()
    print brand_buy_rate

    lst_of_rates = []

    for brand in lst_of_brands:
        lst_of_rates.append(brand_buy_rate[brand])

    data_dict = {"labels": lst_of_brands,
                 "datasets": [{"data": lst_of_rates,
                               "label": "Buying Rate ($ Spent / HH)",
                               "backgroundColor": ["#c70039",
                                                   "#ff5733",
                                                   "#ff8d1a",
                                                   "#ffc300"],
                               "hoverBackgroundColor": ["#c70039",
                                                        "#3ff5733",
                                                        "#Fff8d1a",
                                                        "#3ffc300"]}]}

    return jsonify(data_dict)


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    app.run(port=5000, host="0.0.0.0")
