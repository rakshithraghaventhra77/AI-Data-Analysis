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