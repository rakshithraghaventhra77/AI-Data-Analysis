"""
Flask Application Module
Main application file for the AI-powered E-Commerce Order Analytics System.
"""

from flask import Flask, jsonify
from pathlib import Path
import json

from data_loader import load_dataset, get_basic_info
from preprocessing import preprocess_pipeline
from analysis import order_status_distribution, monthly_trend_analysis
from metrics import get_all_metrics
from insights import get_insights_summary


# Initialize Flask app
app = Flask(__name__)

# Global variable to store preprocessed data
PROCESSED_DATA = None
DATASET_PATH = "data/orders.csv"  # Update with actual path to your dataset


def initialize_data():
    """
    Initialize the dataset on application startup.
    """
    global PROCESSED_DATA
    
    try:
        if Path(DATASET_PATH).exists():
            raw_data = load_dataset(DATASET_PATH)
            PROCESSED_DATA = preprocess_pipeline(raw_data)
            return True
    except Exception as e:
        return False
    
    return False


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        JSON: Status of the API.
    """
    return jsonify({"status": "healthy", "message": "API is running"}), 200


@app.route('/metrics', methods=['GET'])
def get_metrics():
    """
    GET /metrics endpoint.
    
    Returns key business metrics including total orders, average delivery time,
    and delivery performance percentages.
    
    Returns:
        JSON: Dictionary of calculated metrics.
    """
    if PROCESSED_DATA is None:
        return jsonify({"error": "Dataset not loaded. Please initialize the data."}), 500
    
    try:
        metrics = get_all_metrics(PROCESSED_DATA)
        return jsonify({"success": True, "data": metrics}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/order-status', methods=['GET'])
def get_order_status():
    """
    GET /order-status endpoint.
    
    Returns the distribution of orders by status (delivered, canceled, etc.)
    with both counts and percentages.
    
    Returns:
        JSON: Order status distribution data.
    """
    if PROCESSED_DATA is None:
        return jsonify({"error": "Dataset not loaded. Please initialize the data."}), 500
    
    try:
        status_dist = order_status_distribution(PROCESSED_DATA)
        return jsonify({"success": True, "data": status_dist}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/monthly-trend', methods=['GET'])
def get_monthly_trend():
    """
    GET /monthly-trend endpoint.
    
    Returns monthly trend analysis including order counts, revenue,
    and average order values grouped by year and month.
    
    Returns:
        JSON: Monthly aggregated trend data.
    """
    if PROCESSED_DATA is None:
        return jsonify({"error": "Dataset not loaded. Please initialize the data."}), 500
    
    try:
        monthly_data = monthly_trend_analysis(PROCESSED_DATA)
        result = monthly_data.to_dict('records')
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/insights', methods=['GET'])
def get_insights():
    """
    GET /insights endpoint.
    
    Returns comprehensive business insights including executive summary,
    performance analysis, and actionable recommendations.
    
    Returns:
        JSON: Complete insights and recommendations.
    """
    if PROCESSED_DATA is None:
        return jsonify({"error": "Dataset not loaded. Please initialize the data."}), 500
    
    try:
        insights = get_insights_summary(PROCESSED_DATA)
        return jsonify({"success": True, "data": insights}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/data-info', methods=['GET'])
def get_data_info():
    """
    GET /data-info endpoint.
    
    Returns basic information about the loaded dataset including
    shape, columns, and missing values.
    
    Returns:
        JSON: Dataset information.
    """
    if PROCESSED_DATA is None:
        return jsonify({"error": "Dataset not loaded. Please initialize the data."}), 500
    
    try:
        info = get_basic_info(PROCESSED_DATA)
        return jsonify({"success": True, "data": info}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors.
    
    Returns:
        JSON: Error message.
    """
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors.
    
    Returns:
        JSON: Error message.
    """
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    # Initialize data on startup
    initialize_data()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
