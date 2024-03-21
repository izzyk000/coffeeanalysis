import streamlit as st
from joblib import load
import pandas as pd
import numpy as np
import plotly.express as px  # For interactive charts

# Load your model and encoding dictionaries
model = load('models/your_model.joblib')
origin_means = load('models/origin_means.joblib')
roastlevel_means = load('models/roastlevel_means.joblib')
feature_importance_data = load('models/feature_importance.joblib')  # Loading the feature importance data

st.title('Coffee Product Performance Predictor')

# User inputs
origin_input = st.selectbox('Select Origin', options=list(origin_means.keys()))
roast_level_input = st.selectbox('Select Roast Level', options=list(roastlevel_means.keys()))
price = st.number_input('Price', value=20.0)  # Example default value

# Define the adjustment function
def adjust_prediction_for_price_outliers(prediction, price, high_price_threshold=40, low_price_threshold=10):
    if price > high_price_threshold:
        adjusted_prediction = 'Low'
    elif price < low_price_threshold:
        adjusted_prediction = 'High'
    else:
        adjusted_prediction = prediction
    return adjusted_prediction

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
    
    # Adjust the prediction based on the price outliers
    adjusted_prediction = adjust_prediction_for_price_outliers(raw_prediction[0], price)
    
    st.write(f'Prediction: {adjusted_prediction}')




# Model Performance Metrics
st.subheader('Model Performance Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Accuracy", "94%")
col2.metric("Precision", "90%")
col3.metric("Recall", "92%")

# Interactive Feature Importance Chart
st.subheader('Feature Importance')
# Assuming 'feature_importances_' contains feature importance scores
# and 'features' is a list of feature names
feature_importances_ = feature_importance_data  # Example data
features = ['Origin', 'Roast Level', 'Price']  # Example feature names

fig = px.bar(x=feature_importances_, y=features, labels={'x': 'Importance', 'y': 'Feature'}, orientation='h')
st.plotly_chart(fig, use_container_width=True)

