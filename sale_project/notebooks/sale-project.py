import pandas as pd

pd.set_option('display.max_columns', None)

order = pd.read_csv("C:/Users/user/Desktop/sale_project/data/order.csv")
customer = pd.read_csv("C:/Users/user/Desktop/sale_project/data/customer.csv")
product = pd.read_csv("C:/Users/user/Desktop/sale_project/data/products.csv")



merge_df = pd.merge(order, customer, on='customer_id')
merge_df = pd.merge(merge_df, product, on='product_id')



merge_df = merge_df[merge_df['price'].notna()]
merge_df['city'] = merge_df['city'].fillna('Unknown')



print(merge_df["date"].dtype)
merge_df["date"] = pd.to_datetime(merge_df["date"])



merge_df['total_price'] = merge_df["price"] * merge_df["quantity"]
total_product = merge_df.groupby('product_name')['quantity'].sum()


customer_report = merge_df.groupby(['name']).agg(
    total_revenue = ('total_price' , 'sum'),
    total_orders = ('product_name', 'count')
)
customer_report = customer_report.sort_values(by='total_revenue', ascending=False)
customer_report = customer_report.reset_index()
customer_report.to_csv("customer_summary_report.csv")


product_report = merge_df.groupby(['product_name']).agg(
    total_quantity = ('quantity', 'sum'),
    total_revenue = ('total_price', 'sum')
)
product_report['avg_price'] = product_report['total_revenue'] / product_report['total_quantity']
product_report = product_report.sort_values(by='total_quantity', ascending=False)
best_product = product_report['total_quantity'].idxmax()
product_report = product_report.reset_index()

product_report.to_csv("product_summary_report.csv")

revenue_per_city = merge_df.groupby('city')['total_price'].sum()
revenue_per_city = revenue_per_city.sort_values( ascending=False)
revenue_per_city.to_csv("city_summary_report.csv")


sales_over_time = merge_df.groupby('date')['total_price'].sum().reset_index()
sales_over_time = sales_over_time.sort_values(by='date', ascending=True)
sales_over_time.to_csv("sales_over_time_report.csv")

total_revenue = merge_df['total_price'].sum()
best_customer = merge_df.groupby('name')['total_price'].sum()
best_customer = best_customer.idxmax()
top_city = revenue_per_city.idxmax()