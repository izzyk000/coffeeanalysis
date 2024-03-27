import streamlit as st
from joblib import load
import pandas as pd
import plotly.express as px  # For interactive charts

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
        prediction_text = '### Prediction: High\n\nThis indicates a strong sales potential for the selected coffee bean characteristics.'
    elif adjusted_prediction == 'Medium':
        prediction_text = '### Prediction: Medium\n\nThis indicates a moderate sales potential. Consider adjusting price or targeting specific markets.'
    else:  # Low
        prediction_text = '### Prediction: Low\n\nThis suggests the sales potential is below average. Review the characteristics and pricing strategy.'

    st.markdown(prediction_text)
