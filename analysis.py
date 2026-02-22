def get_order_status_distribution(df):
    return df['order_status'].value_counts().to_dict()


def get_monthly_trend(df):
    monthly = df.groupby(['purchase_year', 'purchase_month']).size()
    monthly = monthly.reset_index(name='order_count')
    return monthly.to_dict(orient="records")