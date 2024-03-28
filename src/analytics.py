import plotly.express as px

def create_roastlevel_analysis_chart(roastlevel_analysis):
    fig = px.bar(roastlevel_analysis, x='Origin', y='AvgMonthlySales',
                title='Average Monthly Sales by Origin',
                labels={'AvgMonthlySales': 'Average Monthly Sales', 'Origin': 'Origin'},
                color='AvgMonthlySales',
                color_continuous_scale=px.colors.sequential.Viridis)

    fig.update_layout(xaxis_title='Origin',
                yaxis_title='Average Monthly Sales',
                coloraxis_showscale=True)
    return fig


# Create the bubble chart
def bubble_chart(final_df):
    fig = px.scatter(final_df, x="Origin", y="RoastLevel",
                size="AvgMonthlySales", color="AvgMonthlySales",
                hover_name="ProductName",  # Showing product name on hover
                size_max=60,  # You can adjust the max bubble size
                color_continuous_scale=px.colors.sequential.Viridis)

    fig.update_layout(title='Sales Performance by Origin and Roast Level (Bubble Chart)',
                xaxis_title='Origin',
                yaxis_title='Roast Level',
                xaxis={'categoryorder':'total descending'})  # This may help order the x-axis based on value

    return fig

# Roast level top 10 products
def roast_top10(roast10_df):
    fig = px.bar(roast10_df, x='ProductName', y='AvgMonthlySales',
                title='Top 10 products by Roast Level',
                labels={'AvgMonthlySales': 'Average Monthly Sales', 'ProductName': 'ProductName'},
                color='AvgMonthlySales',
                color_continuous_scale=px.colors.sequential.Viridis)

    fig.update_layout(xaxis_title='Products',
                yaxis_title='Average Monthly Sales',
                coloraxis_showscale=True)
    return fig
