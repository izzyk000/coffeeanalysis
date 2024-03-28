import pandas as pd

def load_data():
    coffee_products_df = pd.read_excel('data/Coffee_Products.xlsx', engine='openpyxl')
    customers_data_df = pd.read_excel('data/Customers_Data.xlsx', engine='openpyxl')
    sales_data_df = pd.read_excel('data/Sales_Data.xlsx', engine='openpyxl')
    return coffee_products_df, customers_data_df, sales_data_df

def preprocess_data(coffee_products_df, sales_data_df):
    total_sales_per_product = sales_data_df.groupby('ProductID')['Quantity'].sum()
    coffee_products_df['LaunchDate'] = pd.to_datetime(coffee_products_df['LaunchDate'])
    end_date = pd.Timestamp('2023-12-31')
    coffee_products_df['MonthsOnMarket'] = ((end_date.year - coffee_products_df['LaunchDate'].dt.year) * 12 + end_date.month - coffee_products_df['LaunchDate'].dt.month)
    average_monthly_sales = pd.merge(total_sales_per_product.reset_index(), coffee_products_df[['ProductID', 'MonthsOnMarket']], on='ProductID')
    average_monthly_sales['AvgMonthlySales'] = average_monthly_sales['Quantity'] / average_monthly_sales['MonthsOnMarket']
    
    sales_data_df['YearMonth'] = sales_data_df['SaleDate'].dt.to_period('M')
    monthly_total_sales = sales_data_df.groupby('YearMonth')['Quantity'].sum().reset_index(name='TotalMonthlySales')
    sales_data_with_monthly_totals = pd.merge(sales_data_df, monthly_total_sales, on='YearMonth')
    sales_data_with_monthly_totals['SalesShare'] = sales_data_with_monthly_totals['Quantity'] / sales_data_with_monthly_totals['TotalMonthlySales']
    product_sales_share = sales_data_with_monthly_totals.groupby('ProductID')['SalesShare'].mean().reset_index()
    average_monthly_sales_with_share = pd.merge(average_monthly_sales, product_sales_share, on='ProductID')
    average_monthly_sales_with_share['CompositeMetric'] = average_monthly_sales_with_share['AvgMonthlySales'] * average_monthly_sales_with_share['SalesShare']
    # Merging the processed data back with coffee_products_df
    final_df = pd.merge(average_monthly_sales_with_share, coffee_products_df, on='ProductID', how='left')
    
    return final_df


def preprocess_for_roastlevel_analysis(final_df, roast_level):
    roast_df = final_df[final_df['RoastLevel'] == roast_level]

    roastlevel_analysis = (roast_df.groupby('Origin')['AvgMonthlySales']
                           .mean()
                           .sort_values(ascending=False)
                           .reset_index())

    return roastlevel_analysis


def preprocess_for_roast_top10(final_df, roast_level):
    roast10_df = final_df[final_df['RoastLevel'] == roast_level].sort_values(by='AvgMonthlySales', ascending=False)

    return roast10_df

