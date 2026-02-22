"""
Preprocessing Module
Handles data cleaning and feature engineering for the dataset.
"""

import pandas as pd


def convert_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert date columns to datetime format.
    
    Args:
        df (pd.DataFrame): The input dataset.
    
    Returns:
        pd.DataFrame: Dataset with converted date columns.
    """
    df = df.copy()
    
    date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
    
    for col in date_columns:
        try:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        except Exception:
            pass
    
    return df


def create_delivery_days(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create delivery_days column as the difference between 
    delivery_date and order_date.
    
    Args:
        df (pd.DataFrame): The input dataset.
    
    Returns:
        pd.DataFrame: Dataset with new delivery_days column.
    """
    df = df.copy()
    
    if 'order_approved_at' in df.columns and 'order_delivered_customer_date' in df.columns:
        df['delivery_days'] = (
            pd.to_datetime(df['order_delivered_customer_date'], errors='coerce') - 
            pd.to_datetime(df['order_approved_at'], errors='coerce')
        ).dt.days
    
    return df


def create_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create purchase_year and purchase_month columns from order_purchase_timestamp.
    
    Args:
        df (pd.DataFrame): The input dataset.
    
    Returns:
        pd.DataFrame: Dataset with new temporal feature columns.
    """
    df = df.copy()
    
    if 'order_purchase_timestamp' in df.columns:
        order_date = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
        df['purchase_year'] = order_date.dt.year
        df['purchase_month'] = order_date.dt.month
        df['purchase_date'] = order_date.dt.date
    
    return df


def preprocess_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Execute the full preprocessing pipeline.
    
    Args:
        df (pd.DataFrame): The input dataset.
    
    Returns:
        pd.DataFrame: Fully preprocessed dataset.
    """
    df = convert_date_columns(df)
    df = create_delivery_days(df)
    df = create_temporal_features(df)
    
    return df
