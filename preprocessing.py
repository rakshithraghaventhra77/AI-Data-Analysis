import pandas as pd

def preprocess_data(df):

    date_columns = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]

    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    df['delivery_days'] = (
        df['order_delivered_customer_date'] - df['order_purchase_timestamp']
    ).dt.days

    df['purchase_year'] = df['order_purchase_timestamp'].dt.year
    df['purchase_month'] = df['order_purchase_timestamp'].dt.month

    return df

# ==============================
# Raman - Data Validation Layer
# ==============================

def validate_data(df):

    required_columns = [
        'order_status',
        'order_purchase_timestamp',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]

    missing_cols = [col for col in required_columns if col not in df.columns]

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    return True

# ==============================
# Raman - Data Quality Report
# ==============================

def data_quality_report(df):

    total_rows = df.shape[0]
    total_columns = df.shape[1]
    missing_values = df.isnull().sum().to_dict()

    return {
        "total_rows": total_rows,
        "total_columns": total_columns,
        "missing_values_per_column": missing_values
    }