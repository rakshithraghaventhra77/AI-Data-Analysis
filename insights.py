def generate_insights(df):

    total_orders = df.shape[0]
    most_common_status = df['order_status'].value_counts().idxmax()
    avg_delivery = round(df['delivery_days'].mean(), 2)

    insight_text = f"""
    Total Orders Processed: {total_orders}.
    Most Frequent Order Status: {most_common_status}.
    Average Delivery Time: {avg_delivery} days.
    Delivery system performance evaluated successfully.
    """

    return insight_text