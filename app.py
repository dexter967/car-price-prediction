import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("car_price_model.pkl")

st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 Car Price Prediction")
st.write("Enter the car details below to predict its selling price.")

st.divider()

# -----------------------------
# User Inputs
# -----------------------------
year = st.number_input(
    "Manufacturing Year",
    min_value=1990,
    max_value=2026,
    value=2018
)

present_price = st.number_input(
    "Present Price (Lakhs)",
    min_value=0.0,
    value=5.0,
    step=0.1
)

km_driven = st.number_input(
    "Kilometers Driven",
    min_value=0,
    value=30000,
    step=1000
)

fuel_type = st.selectbox(
    "Fuel Type",
    ["Petrol", "Diesel", "CNG"]
)

seller_type = st.selectbox(
    "Seller Type",
    ["Dealer", "Individual"]
)

transmission = st.selectbox(
    "Transmission",
    ["Manual", "Automatic"]
)

owner = st.selectbox(
    "Number of Previous Owners",
    [0, 1, 2, 3]
)

# -----------------------------
# Prediction
# -----------------------------
if st.button("Predict Price"):

    input_df = pd.DataFrame({
        "year": [year],
        "present_price": [present_price],
        "km_driven": [km_driven],
        "fuel_type": [fuel_type],
        "seller_type": [seller_type],
        "transmission": [transmission],
        "owner": [owner]
    })

    prediction = model.predict(input_df)[0]

    st.success(f"Estimated Selling Price: ₹ {prediction:.2f} Lakhs")
