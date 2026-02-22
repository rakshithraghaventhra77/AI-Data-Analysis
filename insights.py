"""
Insights Module
Generates business insight summaries from the analytics data.
"""

import pandas as pd
from metrics import get_all_metrics
from analysis import order_status_distribution


def generate_executive_summary(df: pd.DataFrame) -> dict:
    """
    Generate a comprehensive executive summary with key business insights.
    
    Args:
        df (pd.DataFrame): The preprocessed dataset.
    
    Returns:
        dict: Executive summary with multiple insight sections.
    """
    metrics = get_all_metrics(df)
    status_dist = order_status_distribution(df)
    
    # Generate insight text
    total_orders = metrics['total_orders']
    avg_delivery = metrics['average_delivery_days']
    late_percentage = metrics['late_delivery_percentage']
    revenue = metrics['total_revenue']
    
    insights = {
        "summary_header": "E-Commerce Order Analytics Executive Summary",
        "key_metrics": metrics,
        "order_volume_insight": f"The system has processed {total_orders} orders, generating ${revenue:,.2f} in total revenue.",
        "delivery_insight": f"Average delivery time is {avg_delivery} days, with {late_percentage}% of orders experiencing late delivery.",
        "status_insight": f"Order fulfillment is distributed across {len(status_dist.get('status_counts', {}))} statuses, with {status_dist.get('status_counts', {}).get('delivered', 0)} orders successfully delivered.",
        "performance_insight": generate_performance_insight(metrics),
        "recommendations": generate_recommendations(metrics, status_dist)
    }
    
    return insights


def generate_performance_insight(metrics: dict) -> str:
    """
    Generate a performance-based insight text.
    
    Args:
        metrics (dict): The calculated metrics dictionary.
    
    Returns:
        str: Performance insight text.
    """
    late_percentage = metrics.get('late_delivery_percentage', 0)
    on_time_percentage = metrics.get('on_time_delivery_percentage', 0)
    
    if on_time_percentage >= 90:
        performance = "Excellent delivery performance with strong on-time rates."
    elif on_time_percentage >= 75:
        performance = "Good delivery performance. Some optimization opportunities exist."
    else:
        performance = "Delivery performance needs improvement. Investigate root causes."
    
    insight = f"{performance} Current on-time delivery rate: {on_time_percentage}%."
    
    return insight


def generate_recommendations(metrics: dict, status_dist: dict) -> list:
    """
    Generate actionable business recommendations.
    
    Args:
        metrics (dict): The calculated metrics dictionary.
        status_dist (dict): Order status distribution data.
    
    Returns:
        list: List of recommendation strings.
    """
    recommendations = []
    
    late_percentage = metrics.get('late_delivery_percentage', 0)
    avg_delivery = metrics.get('average_delivery_days', 0)
    
    if late_percentage > 20:
        recommendations.append("Priority: Review logistics partner performance and set stricter SLAs.")
    
    if avg_delivery > 15:
        recommendations.append("Consider optimizing warehouse locations or shipping methods to reduce delivery time.")
    
    status_counts = status_dist.get('status_counts', {})
    if status_counts.get('canceled', 0) > status_counts.get('delivered', 0) * 0.05:
        recommendations.append("Investigate high cancellation rates - may indicate inventory or quality issues.")
    
    if not recommendations:
        recommendations.append("Operations are performing well. Continue current strategy while monitoring metrics.")
    
    return recommendations


def get_insights_summary(df: pd.DataFrame) -> dict:
    """
    Get a complete insights summary suitable for API response.
    
    Args:
        df (pd.DataFrame): The preprocessed dataset.
    
    Returns:
        dict: Dictionary containing all insights and recommendations.
    """
    summary = generate_executive_summary(df)
    
    return summary
