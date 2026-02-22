# AI-Powered E-Commerce Order Analytics System

A professional, modular Flask backend for analyzing Olist e-commerce order data. The system provides comprehensive business analytics through RESTful API endpoints returning JSON responses.

## Project Overview

This backend system processes e-commerce order data and provides analytics on:
- Order metrics (total orders, average delivery time, late delivery percentages)
- Order status distribution (delivered, canceled, pending, etc.)
- Monthly trend analysis (order counts, revenue, average order values)
- Executive business insights and recommendations

## Project Structure

```
project/
│
├── app.py                 # Flask application and API routes
├── data_loader.py         # Dataset loading utilities
├── preprocessing.py       # Data cleaning and feature engineering
├── analysis.py            # Statistical analysis functions
├── metrics.py             # Business metric calculations
├── insights.py            # Business insight generation
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Module Responsibilities

### `data_loader.py`
- **`load_dataset(file_path)`** - Load CSV dataset and return as DataFrame
- **`get_basic_info(df)`** - Return dataset shape, columns, and missing value statistics

### `preprocessing.py`
- **`convert_date_columns(df)`** - Convert date columns to datetime format
- **`create_delivery_days(df)`** - Calculate delivery days from order approval to delivery
- **`create_temporal_features(df)`** - Extract year, month, and date from timestamps
- **`preprocess_pipeline(df)`** - Execute complete preprocessing workflow

### `analysis.py`
- **`order_status_distribution(df)`** - Calculate order counts and percentages by status
- **`monthly_trend_analysis(df)`** - Group orders by month with aggregated metrics
- **`status_by_period(df)`** - Analyze status distribution by year/month
- **`delivery_performance_by_status(df)`** - Calculate delivery metrics by order status

### `metrics.py`
- **`calculate_total_orders(df)`** - Total number of orders
- **`calculate_average_delivery_time(df)`** - Average delivery time in days
- **`calculate_late_delivery_percentage(df)`** - Percentage of late deliveries
- **`calculate_on_time_delivery_percentage(df)`** - Percentage of on-time deliveries
- **`get_all_metrics(df)`** - Comprehensive metric calculation

### `insights.py`
- **`generate_executive_summary(df)`** - Create comprehensive business summary
- **`generate_performance_insight(metrics)`** - Generate performance-based insights
- **`generate_recommendations(metrics, status_dist)`** - Generate actionable recommendations
- **`get_insights_summary(df)`** - Return complete insight summary for API

### `app.py`
Flask application with the following endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | API health check |
| `/metrics` | GET | Key business metrics |
| `/order-status` | GET | Order status distribution |
| `/monthly-trend` | GET | Monthly trend analysis |
| `/insights` | GET | Business insights & recommendations |
| `/data-info` | GET | Dataset information |

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd project
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. **Place your dataset** in the project root or update the path:
   - Default path: `data/orders.csv`
   - Modify `DATASET_PATH` in `app.py` if your file is elsewhere

2. **Required dataset columns:**
   - `order_id` - Order identifier
   - `order_status` - Current status (delivered, canceled, etc.)
   - `order_purchase_timestamp` - Purchase timestamp
   - `order_approved_at` - Approval timestamp
   - `order_delivered_customer_date` - Delivery date
   - `order_total_price` - Order value

## Running the Application

Start the Flask development server:

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### 1. Health Check
```bash
GET http://localhost:5000/health
```
Response:
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

### 2. Get Metrics
```bash
GET http://localhost:5000/metrics
```
Response:
```json
{
  "success": true,
  "data": {
    "total_orders": 99441,
    "average_delivery_days": 12.50,
    "late_delivery_percentage": 15.23,
    "on_time_delivery_percentage": 84.77,
    "total_revenue": 15280150.50,
    "average_order_value": 153.75
  }
}
```

### 3. Get Order Status Distribution
```bash
GET http://localhost:5000/order-status
```
Response:
```json
{
  "success": true,
  "data": {
    "status_counts": {
      "delivered": 84500,
      "canceled": 5000,
      "pending": 10000
    },
    "status_percentages": {
      "delivered": 85.00,
      "canceled": 5.00,
      "pending": 10.00
    },
    "total_orders": 99500
  }
}
```

### 4. Get Monthly Trends
```bash
GET http://localhost:5000/monthly-trend
```
Response:
```json
{
  "success": true,
  "data": [
    {
      "year": 2016,
      "month": 10,
      "order_count": 324,
      "total_revenue": 50000.00,
      "avg_order_value": 154.32
    },
    {
      "year": 2016,
      "month": 11,
      "order_count": 512,
      "total_revenue": 78500.00,
      "avg_order_value": 153.32
    }
  ]
}
```

### 5. Get Business Insights
```bash
GET http://localhost:5000/insights
```
Response:
```json
{
  "success": true,
  "data": {
    "summary_header": "E-Commerce Order Analytics Executive Summary",
    "key_metrics": {...},
    "order_volume_insight": "The system has processed 99,441 orders...",
    "delivery_insight": "Average delivery time is 12.50 days...",
    "status_insight": "Order fulfillment is distributed across...",
    "performance_insight": "Good delivery performance...",
    "recommendations": [
      "Consider optimizing warehouse locations...",
      "Investigate high cancellation rates..."
    ]
  }
}
```

### 6. Get Dataset Info
```bash
GET http://localhost:5000/data-info
```
Response:
```json
{
  "success": true,
  "data": {
    "total_rows": 99441,
    "total_columns": 12,
    "columns": ["order_id", "order_status", ...],
    "missing_values": {...}
  }
}
```

## Architecture Principles

- ✅ **Modular Design** - Each module has a single responsibility
- ✅ **Clean Code** - No print statements, all functions return values
- ✅ **Scalability** - Easy to add new analysis functions and endpoints
- ✅ **Error Handling** - Graceful error responses with meaningful messages
- ✅ **Type Hints** - Functions include parameter and return type annotations
- ✅ **Documentation** - Comprehensive docstrings for all functions

## Dependencies

- **Flask 2.3.3** - Web framework for building REST APIs
- **Pandas 2.0.3** - Data manipulation and analysis

## Extending the System

To add new analysis or metrics:

1. **Add functions to appropriate module** (`analysis.py`, `metrics.py`, etc.)
2. **Import and use in `app.py`**
3. **Create new Flask route** with proper error handling
4. **Update README** with endpoint documentation

Example:
```python
@app.route('/custom-analysis', methods=['GET'])
def get_custom_analysis():
    if PROCESSED_DATA is None:
        return jsonify({"error": "Dataset not loaded"}), 500
    try:
        result = your_analysis_function(PROCESSED_DATA)
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

## Notes

- Ensure your CSV file has datetime columns properly formatted
- The system handles missing values gracefully in calculations
- All metrics are rounded to 2 decimal places for consistency
- The application uses a global variable to cache preprocessed data for performance

## License

This project is provided as-is for educational and development purposes.
