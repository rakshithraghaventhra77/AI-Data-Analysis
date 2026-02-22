"""
Analysis Module
Performs order analytics including status distribution and monthly trends.
"""

import pandas as pd


def order_status_distribution(df: pd.DataFrame) -> dict:
    """
    Calculate the distribution of order statuses.
    
    Args:
        df (pd.DataFrame): The preprocessed dataset.
    
    Returns:
        dict: Order status counts and percentages.
    """
    if 'order_status' not in df.columns:
        return {}
    
    status_counts = df['order_status'].value_counts()
    status_percentages = (status_counts / len(df) * 100).round(2)
    
    result = {
        "status_counts": status_counts.to_dict(),
        "status_percentages": status_percentages.to_dict(),
        "total_orders": int(len(df))
    }
    
    return result


def monthly_trend_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group orders by month and analyze trends.
    
    Args:
        df (pd.DataFrame): The preprocessed dataset with purchase_year and purchase_month.
    
    Returns:
        pd.DataFrame: Monthly aggregated data with order counts and metrics.
    """
    if 'purchase_year' not in df.columns or 'purchase_month' not in df.columns:
        return pd.DataFrame()
    
    monthly_data = df.groupby(['purchase_year', 'purchase_month']).agg({
        'order_id': 'count',
        'order_total_price': ['sum', 'mean'] if 'order_total_price' in df.columns else []
    }).reset_index()
    
    monthly_data.columns = ['year', 'month', 'order_count', 'total_revenue', 'avg_order_value']
    monthly_data = monthly_data.dropna()
    
    return monthly_data


def status_by_period(df: pd.DataFrame) -> dict:
    """
    Analyze order status distribution by time period (year and month).
    
    Args:
        df (pd.DataFrame): The preprocessed dataset.
    
    Returns:
        dict: Status distribution broken down by year and month.
    """
    if 'purchase_year' not in df.columns or 'order_status' not in df.columns:
        return {}
    
    period_status = df.groupby(['purchase_year', 'purchase_month', 'order_status']).size().reset_index(name='count')
    
    result = period_status.to_dict('records')
    
    return result


def delivery_performance_by_status(df: pd.DataFrame) -> dict:
    """
    Analyze delivery performance metrics grouped by order status.
    
    Args:
        df (pd.DataFrame): The preprocessed dataset with delivery_days.
    
    Returns:
        dict: Delivery metrics by status.
    """
    if 'delivery_days' not in df.columns or 'order_status' not in df.columns:
        return {}
    
    delivery_stats = df.groupby('order_status')['delivery_days'].agg([
        'count', 'mean', 'median', 'min', 'max'
    ]).round(2)
    
    result = delivery_stats.to_dict('index')
    
    return result
