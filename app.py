from pathlib import Path

from flask import Flask, jsonify

from data_loader import load_data
from preprocessing import preprocess_data, validate_data
from analysis import get_order_status_distribution, get_monthly_trend
from metrics import calculate_metrics, delivery_performance_breakdown
from insights import generate_insights

app = Flask(__name__)

# Load and preprocess dataset once
DATA_PATH = Path(__file__).resolve().parent / "olist_orders_dataset.csv"
df = load_data(DATA_PATH)
validate_data(df)
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


@app.route("/delivery-breakdown")
def delivery_breakdown():
    return jsonify(delivery_performance_breakdown(df))

@app.route("/data-quality")
def data_quality():
    return jsonify(data_quality_report(df))



# ==============================
# Rakshith - Global Error Handler
# ==============================

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({
        "error": str(e),
        "message": "An internal server error occurred."
    }), 500



# ==============================
# Team - System Metadata
# ==============================

@app.route("/system-info")
def system_info():

    return jsonify({
        "project_name": "AI Powered Order Analytics",
        "backend_framework": "Flask",
        "dataset": "Olist Orders Dataset",
        "total_records": df.shape[0]
    })


if __name__ == "__main__":
    app.run(debug=True)