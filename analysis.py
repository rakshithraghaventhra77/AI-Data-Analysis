def get_order_status_distribution(df):
    return df['order_status'].value_counts().to_dict()


def get_monthly_trend(df):
    monthly = df.groupby(['purchase_year', 'purchase_month']).size()
    monthly = monthly.reset_index(name='order_count')
    return monthly.to_dict(orient="records")

# ==============================
# Balan - Top Performing Months
# ==============================

def get_top_5_months(df):

    monthly = df.groupby(['purchase_year', 'purchase_month']).size()
    monthly = monthly.reset_index(name='order_count')

    top_5 = monthly.sort_values(by='order_count', ascending=False).head(5)

    return top_5.to_dict(orient="records")

# ==============================
# Balan - Yearly Summary
# ==============================

def get_yearly_summary(df):

    yearly = df.groupby('purchase_year').size()
    yearly = yearly.reset_index(name='order_count')

    return yearly.to_dict(orient="records")