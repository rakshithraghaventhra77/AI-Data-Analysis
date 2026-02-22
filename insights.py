def generate_insights(df):
    total_orders = int(df.shape[0])
    if total_orders:
        most_common_status = df['order_status'].value_counts().idxmax()
        avg_delivery_raw = df['delivery_days'].mean()
        avg_delivery = round(avg_delivery_raw, 2)
        if avg_delivery != avg_delivery:
            avg_delivery = 0.0
    else:
        most_common_status = "unknown"
        avg_delivery = 0.0

    insight_text = f"""
    Total Orders Processed: {total_orders}.
    Most Frequent Order Status: {most_common_status}.
    Average Delivery Time: {avg_delivery} days.
    Delivery system performance evaluated successfully.
    """

    return insight_text
# ==============================
# Viswakailash - Risk Alert Logic
# ==============================

def risk_alerts(df):

    late_orders = df[
        df['order_delivered_customer_date'] >
        df['order_estimated_delivery_date']
    ].shape[0]

    total_orders = int(df.shape[0])
    if not total_orders:
        return "No orders available to assess delivery risk."

    late_ratio = late_orders / total_orders

    if late_ratio > 0.25:
        return "High risk detected: Late deliveries exceed 25%."
    elif late_ratio > 0.15:
        return "Moderate risk: Delivery delays increasing."
    else:
        return "Delivery performance is stable."
# ==============================
# Viswakailash - Academic Executive Summary
# ==============================

def academic_summary(df):

    total_orders = df.shape[0]
    late_orders = df[
        df['order_delivered_customer_date'] >
        df['order_estimated_delivery_date']
    ].shape[0]

    late_ratio = round((late_orders / total_orders) * 100, 2)

    return (
        f"This dataset contains {total_orders} total orders. "
        f"Late deliveries account for {late_ratio}% of total shipments. "
        "The system successfully analyzed operational efficiency."
    )