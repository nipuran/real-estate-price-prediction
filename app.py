import streamlit as st
import pandas as pd
import pickle
import json
import numpy as np

# Load the model
with open('banglore_home_prices_model.pickle', 'rb') as model_file:
    lr_model = pickle.load(model_file)

# Load columns from the JSON file
with open('columns.json', 'r') as json_file:
    columns = json.load(json_file)

locations = columns.get('data_columns')[3:]
X_columns = pd.Index(columns.get('data_columns'))

def predict_price(location, sqft, bath, bhk):
    # Create input array with zeros
    x = np.zeros(len(X_columns))

    # Set features based on user input
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    
    # Check if the location exists in X_columns
    if location in X_columns:
        loc_index = np.where(X_columns == location)[0][0]
        x[loc_index] = 1  # Set the location index to 1
    else:
        st.error("Selected location is not valid.")
        return None  # Return None if location is invalid

    return lr_model.predict([x])[0]

# Title of the app
st.title("Real Estate Price Prediction")

# User inputs
selected_location = st.selectbox("Select Location", options=locations)
total_sqft = st.number_input("Total Square Feet", min_value=0)
bath = st.number_input("Number of Bathrooms", min_value=0)
bhk = st.number_input("Number of Bedrooms (BHK)", min_value=0)

# Prediction button
if st.button("Predict Price"):
    predicted_price = predict_price(selected_location, total_sqft, bath, bhk)
    
    if predicted_price is not None:
        st.success(f"Predicted Price: ₹{predicted_price:,.2f} Lakhs")
