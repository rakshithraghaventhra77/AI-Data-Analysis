def calculate_metrics(df):
    total_orders = int(df.shape[0])

    avg_delivery_raw = df['delivery_days'].mean() if total_orders else 0.0
    avg_delivery = round(avg_delivery_raw, 2)
    if avg_delivery != avg_delivery:
        avg_delivery = 0.0

    late_deliveries = df[
        df['order_delivered_customer_date'] >
        df['order_estimated_delivery_date']
    ].shape[0]

    late_percentage = 0.0
    if total_orders:
        late_percentage = round((late_deliveries / total_orders) * 100, 2)

    return {
        "total_orders": total_orders,
        "average_delivery_days": avg_delivery,
        "late_delivery_percentage": late_percentage
    }
# ==============================
# Shaileshvar - Delivery Breakdown
# ==============================

def delivery_performance_breakdown(df):

    on_time = df[
        df['order_delivered_customer_date'] <=
        df['order_estimated_delivery_date']
    ].shape[0]

    late = df[
        df['order_delivered_customer_date'] >
        df['order_estimated_delivery_date']
    ].shape[0]

    return {
        "on_time_deliveries": on_time,
        "late_deliveries": late
    }
