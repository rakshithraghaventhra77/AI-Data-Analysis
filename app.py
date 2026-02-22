from flask import Flask, jsonify

from data_loader import load_data
from preprocessing import preprocess_data
from analysis import get_order_status_distribution, get_monthly_trend
from metrics import calculate_metrics
from insights import generate_insights

app = Flask(__name__)

# Load and preprocess dataset once
df = load_data("olist_orders_dataset.csv")
df = preprocess_data(df)


@app.route("/")
def home():
    return "AI Order Analytics Backend Running"


@app.route("/metrics")
def metrics():
    return jsonify(calculate_metrics(df))


@app.route("/order-status")
def order_status():
    return jsonify(get_order_status_distribution(df))


@app.route("/monthly-trend")
def monthly_trend():
    return jsonify(get_monthly_trend(df))


@app.route("/insights")
def insights():
    return jsonify({"insight": generate_insights(df)})


if __name__ == "__main__":
    app.run(debug=True)