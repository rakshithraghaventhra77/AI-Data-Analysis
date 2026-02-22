def calculate_metrics(df):

    total_orders = df.shape[0]

    avg_delivery = round(df['delivery_days'].mean(), 2)

    late_deliveries = df[
        df['order_delivered_customer_date'] >
        df['order_estimated_delivery_date']
    ].shape[0]

    late_percentage = round((late_deliveries / total_orders) * 100, 2)

    return {
        "total_orders": total_orders,
        "average_delivery_days": avg_delivery,
        "late_delivery_percentage": late_percentage
    }