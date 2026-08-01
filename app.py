import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import sklearn
import joblib
import streamlit as st

st.write("scikit-learn:", sklearn.__version__)
st.write("joblib:", joblib.__version__)
# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="🚗 Car Price Predictor",
    page_icon="🚗",
    layout="centered"
)

# -----------------------------
# Load Trained Pipeline Model
# -----------------------------
model = joblib.load("car_price_model.pkl")

# -----------------------------
# Load Dropdown Options
# -----------------------------
with open("options.json", "r") as f:
    options = json.load(f)

# -----------------------------
# Load Car Mapping
# -----------------------------
car_mapping = pd.read_csv("car_mapping.csv")

# -----------------------------
# App Title
# -----------------------------
st.title("🚗 Used Car Price Prediction")

st.markdown("""
Predict the estimated selling price of a used car using a Machine Learning model.

Fill in the vehicle details below and click **Predict Price**.
""")

st.divider()

# -----------------------------
# Car Selection
# -----------------------------
car_name = st.selectbox(
    "Select Car",
    options["car_name"]
)

# Automatically determine Brand and Model
selected = car_mapping[car_mapping["car_name"] == car_name].iloc[0]

brand = selected["brand"]
model_name = selected["model"]

st.info(f"**Brand:** {brand}")

st.info(f"**Model:** {model_name}")

st.divider()
# ======================================================
# User Input Section
# ======================================================

col1, col2 = st.columns(2)

with col1:
    vehicle_age = st.number_input(
        "Vehicle Age (Years)",
        min_value=0,
        max_value=40,
        value=5
    )

    km_driven = st.number_input(
        "Kilometers Driven",
        min_value=0,
        value=30000,
        step=1000
    )

    mileage = st.number_input(
        "Mileage (km/l)",
        min_value=0.0,
        value=18.0,
        step=0.1
    )

    engine = st.number_input(
        "Engine Capacity (CC)",
        min_value=500,
        max_value=7000,
        value=1200,
        step=100
    )

with col2:
    max_power = st.number_input(
        "Max Power (BHP)",
        min_value=10.0,
        max_value=1000.0,
        value=80.0,
        step=1.0
    )

    seats = st.selectbox(
        "Number of Seats",
        options["seats"]
    )

    fuel_type = st.selectbox(
        "Fuel Type",
        options["fuel_type"]
    )

    seller_type = st.selectbox(
        "Seller Type",
        options["seller_type"]
    )

    transmission_type = st.selectbox(
        "Transmission Type",
        options["transmission_type"]
    )

st.divider()

# ======================================================
# Feature Engineering
# ======================================================

if engine == 0:
    power_to_engine_ratio = 0
else:
    power_to_engine_ratio = max_power / engine

km_driven_log = np.log1p(km_driven)

# Preview Inputs
st.subheader("📋 Selected Vehicle")

preview = pd.DataFrame({
    "Feature": [
        "Car Name",
        "Brand",
        "Model",
        "Vehicle Age",
        "KM Driven",
        "Fuel Type",
        "Seller Type",
        "Transmission",
        "Mileage",
        "Engine",
        "Max Power",
        "Seats"
    ],
    "Value": [
        car_name,
        brand,
        model_name,
        vehicle_age,
        km_driven,
        fuel_type,
        seller_type,
        transmission_type,
        mileage,
        engine,
        max_power,
        seats
    ]
})

st.dataframe(preview, use_container_width=True)

st.divider()
# ======================================================
# Prediction
# ======================================================

if st.button("🚗 Predict Price", use_container_width=True):

    # Create input dataframe in the exact order expected by the model
    input_df = pd.DataFrame({
        "car_name": [car_name],
        "brand": [brand],
        "model": [model_name],
        "vehicle_age": [vehicle_age],
        "km_driven": [km_driven],
        "seller_type": [seller_type],
        "fuel_type": [fuel_type],
        "transmission_type": [transmission_type],
        "mileage": [mileage],
        "engine": [engine],
        "max_power": [max_power],
        "seats": [seats],
        "power_to_engine_ratio": [power_to_engine_ratio],
        "km_driven_log": [km_driven_log]
    })

    try:
        prediction = model.predict(input_df)[0]

        st.success("✅ Prediction Completed Successfully!")

        st.metric(
            label="Estimated Selling Price",
            value=f"₹ {prediction:,.2f} Lakhs"
        )

        st.balloons()

        with st.expander("📄 Input Summary"):
            st.dataframe(input_df, use_container_width=True)

    except Exception as e:
        st.error("❌ Prediction Failed!")
        st.exception(e)

# ======================================================
# Footer
# ======================================================

st.divider()

st.markdown(
    """
    ---
    ### 👨‍💻 Developed By

    **Abhijith A Kurup**

    **MUID:** abhijitha-8@mulearn

    Built using **Streamlit**, **Scikit-learn**, and **Python**.
    """
)
