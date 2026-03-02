from pathlib import Path
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from flask import Flask, jsonify, render_template, send_file, request
import pandas as pd

from data_loader import load_data
from preprocessing import preprocess_data, validate_data, data_quality_report
from analysis import get_order_status_distribution, get_monthly_trend
from metrics import calculate_metrics, delivery_performance_breakdown
from insights import generate_insights
from ml_engine import get_all_ml_insights, predict_future_orders, anomaly_detection, clustering_analysis
from report_generator import generate_pdf_report, get_report_downloads
from chatbot import analyze_data_with_ai, initialize_gemini

app = Flask(__name__)

# ===== GEMINI API SETUP =====
# To use Google Gemini API for the chatbot:
# 1. Get your API key from: https://aistudio.google.com/app/apikey
# 2. Set the environment variable (Windows PowerShell):
#    $env:GEMINI_API_KEY = "your-api-key-here"
# 3. Or set it permanently in your system environment variables

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    print("✅ Gemini API key detected - AI chatbot will use Google Gemini")
    initialize_gemini()
else:
    print("⚠️  No GEMINI_API_KEY found - chatbot will use fallback analysis")
    print("   To enable Gemini: set environment variable GEMINI_API_KEY=your-key")
    print("   See GEMINI_SETUP.md for detailed instructions")

# Load and preprocess dataset once
DATA_PATH = Path(__file__).resolve().parent / "olist_orders_dataset.csv"
df = load_data(DATA_PATH)
validate_data(df)
df = preprocess_data(df)

def get_active_df():
    """Get the active dataframe"""
    return df


@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# Chatbot Features (Gemini Integration)
# ==============================

@app.route("/chatbot", methods=['POST'])
def chatbot():
    """AI Chatbot endpoint powered by Google Gemini API"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({"error": "Please provide a question"}), 400
        
        active_df = get_active_df()
        
        # Use Gemini AI to analyze the data and answer the question
        response = analyze_data_with_ai(active_df, question)
        
        return jsonify({
            "question": question,
            "answer": response,
            "rows": len(active_df)
        })
    
    except Exception as e:
        return jsonify({"error": f"Chatbot error: {str(e)}"}), 500


@app.route("/metrics")
def metrics():
    try:
        return jsonify(calculate_metrics(get_active_df()))
    except Exception as e:
        return jsonify({"error": f"Metrics calculation failed: {str(e)}", "total_orders": 0, "average_delivery_days": 0})


@app.route("/order-status")
def order_status():
    try:
        active_df = get_active_df()
        # Try to get order status distribution
        if 'order_status' in active_df.columns:
            return jsonify(active_df['order_status'].value_counts().to_dict())
        else:
            # Return empty dict if column doesn't exist
            return jsonify({})
    except Exception as e:
        return jsonify({})


@app.route("/monthly-trend")
def monthly_trend():
    try:
        active_df = get_active_df()
        # Check if required columns exist
        if 'purchase_year' not in active_df.columns or 'purchase_month' not in active_df.columns:
            # Try to create from date column if available
            date_cols = [col for col in active_df.columns if 'date' in col.lower() or 'time' in col.lower()]
            if date_cols:
                temp_df = active_df.copy()
                date_col = date_cols[0]
                temp_df[date_col] = pd.to_datetime(temp_df[date_col], errors='coerce')
                temp_df['purchase_year'] = temp_df[date_col].dt.year
                temp_df['purchase_month'] = temp_df[date_col].dt.month
                monthly = temp_df.groupby(['purchase_year', 'purchase_month']).size()
                monthly = monthly.reset_index(name='order_count')
                return jsonify(monthly.to_dict(orient="records"))
            return jsonify([])
        
        monthly = active_df.groupby(['purchase_year', 'purchase_month']).size()
        monthly = monthly.reset_index(name='order_count')
        return jsonify(monthly.to_dict(orient="records"))
    except Exception as e:
        return jsonify([])


@app.route("/insights")
def insights():
    try:
        insight = generate_insights(get_active_df())
        return jsonify({"insight": insight})
    except Exception as e:
        return jsonify({"insight": f"Dataset loaded. Ask the AI chatbot for insights about your data!"})


@app.route("/delivery-breakdown")
def delivery_breakdown():
    try:
        return jsonify(delivery_performance_breakdown(get_active_df()))
    except Exception as e:
        return jsonify({})

@app.route("/data-quality")
def data_quality():
    try:
        return jsonify(data_quality_report(get_active_df()))
    except Exception as e:
        return jsonify({"error": str(e)})


# ==============================
# ML & Advanced Analytics Endpoints
# ==============================

@app.route("/predict")
def predict():
    """Machine Learning predictions for future orders."""
    try:
        return jsonify(predict_future_orders(get_active_df(), months_ahead=6))
    except Exception as e:
        return jsonify({"message": "Predictions require specific data columns"})


@app.route("/anomalies")
def anomalies():
    """Detect anomalies in delivery performance."""
    try:
        return jsonify(anomaly_detection(get_active_df()))
    except Exception as e:
        return jsonify({"message": "Anomaly detection requires numeric columns"})


@app.route("/clustering")
def clustering():
    """Perform clustering analysis on delivery data."""
    try:
        return jsonify(clustering_analysis(get_active_df()))
    except Exception as e:
        return jsonify({"message": "Clustering requires numeric data"})


@app.route("/ml-insights")
def ml_insights():
    """Get comprehensive ML-based insights."""
    try:
        return jsonify(get_all_ml_insights(get_active_df()))
    except Exception as e:
        return jsonify({"message": "ML insights not available for this dataset"})


@app.route("/report")
def report():
    """Download PDF report."""
    try:
        active_df = get_active_df()
        metrics = calculate_metrics(active_df)
        status_dist = get_order_status_distribution(active_df)
        trends = get_monthly_trend(active_df)
        insights_text = generate_insights(active_df)
        
        pdf_buffer = generate_pdf_report(active_df, metrics, status_dist, trends, insights_text)
        
        if pdf_buffer is None:
            return jsonify({"error": "PDF generation requires reportlab. Install with: pip install reportlab"}), 400
        
        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"order-analytics-report-{pd.Timestamp.now().strftime('%Y%m%d')}.pdf"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/report-formats")
def report_formats():
    """Get available report download formats."""
    active_df = get_active_df()
    return jsonify(get_report_downloads(active_df, {}, {}, {}, ""))


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
    active_df = get_active_df()
    return jsonify({
        "project_name": "AI Powered Order Analytics",
        "backend_framework": "Flask",
        "dataset": current_dataset['filename'],
        "total_records": len(active_df),
        "version": "2.1.0",
        "features": [
            "Advanced Analytics",
            "Machine Learning Predictions",
            "Anomaly Detection",
            "Clustering Analysis",
            "PDF Report Generation",
            "Real-time Dashboard",
            "CSV Upload",
            "AI Chatbot"
        ]
    })


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "message": "API is running",
        "timestamp": pd.Timestamp.now().isoformat()
    })


if __name__ == "__main__":
    app.run(debug=True)