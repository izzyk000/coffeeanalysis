import streamlit as st
from joblib import load
import pandas as pd
import plotly.express as px  # For interactive charts
from analytics import create_roastlevel_analysis_chart, bubble_chart, roast_top10
from data_processing import preprocess_data, preprocess_for_roastlevel_analysis, preprocess_for_roast_top10, load_data


# Load your model and encoding dictionaries
model = load('models/your_model.joblib')
origin_means = load('models/origin_means.joblib')
roastlevel_means = load('models/roastlevel_means.joblib')

# Title and introduction
st.title('Welcome to the Saigon Bean Bazaar Sales Estimator!')
st.markdown("""

Discover the sales potential of new coffee beans with our AI-driven estimator. Leveraging historical sales data from Saigon Bean Bazaar, this tool provides insights into how well new bean varieties might perform in our store. 

Simply input details about the coffee beans you're considering, and let our model predict their sales success. Whether you're evaluating new origins, roast levels, or pricing strategies, our estimator is here to guide your decisions with data-driven confidence.

**Get started** by entering the coffee bean characteristics below and press **Predict** to see the magic happen!
""")


# Sidebar - About description
st.sidebar.header('About Saigon Bean Bazaar Estimator')
st.sidebar.info("""
This predictive tool is designed exclusively for Saigon Bean Bazaar, a leading e-commerce store specializing in premium coffee beans. By analyzing extensive past sales data, our model assesses factors like bean origin, roast level, and pricing to forecast the market appeal of upcoming coffee beans.
""")


# User inputs
origin_input = st.selectbox('Select Origin', options=list(origin_means.keys()), 
                            help='Choose the origin of the coffee bean.')
roast_level_input = st.selectbox('Select Roast Level', options=list(roastlevel_means.keys()), 
                                 help='Choose the roast level.')
price = st.slider('Price ($)', min_value=5.0, max_value=60.0, value=30.0, step=0.5,
                  help='Set the price of the coffee bean.')
    
# Prediction and display results directly
if st.button('Predict'):
    origin_encoded = origin_means[origin_input]
    roast_level_encoded = roastlevel_means[roast_level_input]
    
    # Create a DataFrame with the correct feature names and the input data
    input_data = pd.DataFrame({
        'Origin_TargetEncoded': [origin_encoded],
        'RoastLevel_TargetEncoded': [roast_level_encoded],
        'Price': [price]
    })
    
    # Use the DataFrame for prediction
    raw_prediction = model.predict(input_data)
    
    # Function to adjust the prediction based on price outliers
    def adjust_prediction_for_price_outliers(prediction, price, high_price_threshold=40, low_price_threshold=10):
        if price > high_price_threshold:
            return 'Low'
        elif price < low_price_threshold:
            return 'High'
        else:
            return prediction
    
    # Adjust the prediction based on the price outliers
    adjusted_prediction = adjust_prediction_for_price_outliers(raw_prediction[0], price)

    # Display the result using markdown
    if adjusted_prediction == 'High':
        prediction_text = f"""
            ### Prediction: High\n\n
            This prediction is based on favorable market trends for {origin_input} beans at a roast level of {roast_level_input}. Historically, beans from {origin_input} have shown strong sales when priced correctly. Consider highlighting unique tasting notes and sustainable sourcing practices in your marketing to capitalize on this potential.
        """
        
    elif adjusted_prediction == 'Medium':
        prediction_text = f"""
            ### Prediction: Medium\n\n
            Beans with these characteristics have shown variable market performance. Consider experimenting with limited-time offers or bundle deals to increase appeal. Additionally, engaging storytelling about the bean's origin ({origin_input}) and the roasting process (Roast level: {roast_level_input}) can enhance consumer interest.
        """
    else:  # Low
        prediction_text = f"""
            ### Prediction: Low\n\n
            The prediction suggests there's room to optimize for beans from {origin_input}. Perhaps explore a slight adjustment in price (currently ${price}) or highlight any unique features of the beans. It's also worth researching emerging coffee trends that could influence consumer preferences.
        """

    st.markdown(prediction_text)

    # list of roast level chart
    # coffee_products_df, customers_data_df, sales_data_df = load_data()
    # final_df = preprocess_data(coffee_products_df, sales_data_df)
    # # Generate roastlevel_analysis based on the selected roast level
    # roastlevel_analysis = preprocess_for_roastlevel_analysis(final_df, roast_level_input)
    # fig = create_roastlevel_analysis_chart(roastlevel_analysis)
    # st.plotly_chart(fig)


    # Top 10 roast level product
    # roast10_df = preprocess_for_roast_top10(final_df, roast_level_input)
    # fig1 = roast_top10(roast10_df)
    # st.plotly_chart(fig1)



    # #bubble chart
    # coffee_products_df, customers_data_df, sales_data_df = load_data()
    # final_df = preprocess_data(coffee_products_df, sales_data_df)
    # fig2 = bubble_chart(final_df)
    # st.plotly_chart(fig2)



    # st.markdown("""
    #         ### Interpreting the Bubble Chart: Insights into Coffee Sales Performance

    #         The bubble chart visualizes sales data, making it easier to understand market dynamics at a glance. Here's how to read it:

    #         - **Axes**: The chart is divided by origin (horizontal axis) and roast level (vertical axis), organizing your coffee offerings.
    #         - **Bubbles**: Each represents a coffee product, with its size indicating sales volume—larger bubbles denote higher sales.

    #         #### Insights:
    #         - **Sales Volume**: Larger bubbles highlight the best sellers. This signals strong consumer demand for these origins and roast levels.
    #         - **Market Trends**: Clusters of bubbles in particular areas suggest market preferences, guiding possible marketing and stock strategies.
    #         - **Opportunities**: Smaller bubbles might indicate niche markets with growth potential, deserving targeted marketing efforts.

    #         By analyzing this chart, you can tailor your offerings to meet consumer demand more effectively, optimizing your inventory and marketing strategies for better performance.
    #     """)    

    # Bubble chart section within an expander
    with st.expander("View Bubble Chart Analysis"):
        # Load and preprocess the data
        coffee_products_df, customers_data_df, sales_data_df = load_data()
        final_df = preprocess_data(coffee_products_df, sales_data_df)
        
        # Generate the bubble chart
        fig2 = bubble_chart(final_df)
        st.plotly_chart(fig2)

        # Markdown explanation for the bubble chart
        st.markdown("""
            ### Interpreting the Bubble Chart: Insights into Coffee Sales Performance

            The bubble chart visualizes sales data, making it easier to understand market dynamics at a glance. Here's how to read it:

            - **Axes**: The chart is divided by origin (horizontal axis) and roast level (vertical axis), organizing your coffee offerings.
            - **Bubbles**: Each represents a coffee product, with its size indicating sales volume—larger bubbles denote higher sales.

            #### Insights:
            - **Sales Volume**: Larger bubbles highlight the best sellers. This signals strong consumer demand for these origins and roast levels.
            - **Market Trends**: Clusters of bubbles in particular areas suggest market preferences, guiding possible marketing and stock strategies.
            - **Opportunities**: Smaller bubbles might indicate niche markets with growth potential, deserving targeted marketing efforts.

            By analyzing this chart, you can tailor your offerings to meet consumer demand more effectively, optimizing your inventory and marketing strategies for better performance.
        """)

    # Place any other Streamlit components outside the expander as needed

