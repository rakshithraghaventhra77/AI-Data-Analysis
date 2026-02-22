"""
Metrics Module
Calculates key business metrics for the order analytics system.
"""

import pandas as pd


def calculate_total_orders(df: pd.DataFrame) -> int:
    """
    Calculate the total number of orders in the dataset.
    
    Args:
        df (pd.DataFrame): The dataset.
    
    Returns:
        int: Total number of orders.
    """
    return len(df)


def calculate_average_delivery_time(df: pd.DataFrame) -> float:
    """
    Calculate the average delivery time in days.
    
    Args:
        df (pd.DataFrame): The dataset with delivery_days column.
    
    Returns:
        float: Average delivery time in days, rounded to 2 decimal places.
    """
    if 'delivery_days' not in df.columns:
        return 0.0
    
    avg_delivery = df['delivery_days'].mean()
    
    return round(avg_delivery, 2) if pd.notna(avg_delivery) else 0.0


def calculate_late_delivery_percentage(df: pd.DataFrame, threshold_days: int = 0) -> float:
    """
    Calculate the percentage of late deliveries.
    
    A delivery is considered late if delivery_days > threshold_days.
    
    Args:
        df (pd.DataFrame): The dataset with delivery_days column.
        threshold_days (int): Number of days to consider as on-time (default: 0).
    
    Returns:
        float: Percentage of late deliveries, rounded to 2 decimal places.
    """
    if 'delivery_days' not in df.columns or len(df) == 0:
        return 0.0
    
    late_deliveries = (df['delivery_days'] > threshold_days).sum()
    late_percentage = (late_deliveries / len(df)) * 100
    
    return round(late_percentage, 2)


def calculate_on_time_delivery_percentage(df: pd.DataFrame, threshold_days: int = 0) -> float:
    """
    Calculate the percentage of on-time deliveries.
    
    Args:
        df (pd.DataFrame): The dataset with delivery_days column.
        threshold_days (int): Number of days to consider as on-time (default: 0).
    
    Returns:
        float: Percentage of on-time deliveries, rounded to 2 decimal places.
    """
    on_time_percentage = 100 - calculate_late_delivery_percentage(df, threshold_days)
    
    return round(on_time_percentage, 2)


def get_all_metrics(df: pd.DataFrame) -> dict:
    """
    Calculate all key business metrics.
    
    Args:
        df (pd.DataFrame): The preprocessed dataset.
    
    Returns:
        dict: Dictionary containing all calculated metrics.
    """
    metrics = {
        "total_orders": calculate_total_orders(df),
        "average_delivery_days": calculate_average_delivery_time(df),
        "late_delivery_percentage": calculate_late_delivery_percentage(df),
        "on_time_delivery_percentage": calculate_on_time_delivery_percentage(df),
        "total_revenue": round(df['order_total_price'].sum(), 2) if 'order_total_price' in df.columns else 0.0,
        "average_order_value": round(df['order_total_price'].mean(), 2) if 'order_total_price' in df.columns else 0.0
    }
    
    return metrics
