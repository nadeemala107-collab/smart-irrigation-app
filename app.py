# IoT-Based Precision Irrigation System
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Smart Irrigation", layout="wide")

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("Crop_recommendationV2.csv")

data = load_data()

# -------------------------------
# SESSION STATE (for page control)
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# -------------------------------
# TOP BUTTONS (Navigation)
# -------------------------------
col1, col2, col3 = st.columns([1,1,6])

with col1:
    if st.button("🏠 Home"):
        st.session_state.page = "home"

with col2:
    if st.button("📊 Dataset"):
        st.session_state.page = "dataset"

# -------------------------------
# PREPROCESSING (COMMON)
# -------------------------------
cat_cols = ['soil_type', 'sunlight_exposure', 'water_source_type']
for col in cat_cols:
    data[col] = LabelEncoder().fit_transform(data[col].astype(str))

X = data.drop(columns=['label'])
scaler = StandardScaler()
scaler.fit(X)

# -------------------------------
# HOME PAGE
# -------------------------------
if st.session_state.page == "home":
    st.title("💧 Smart Precision Irrigation System")

    st.markdown("### 🌱 Welcome to Smart Farming System")
    st.info("This system helps farmers decide when to irrigate based on soil conditions.")

    if st.button("🚀 Start"):
        st.session_state.page = "input"

# -------------------------------
# DATASET PAGE
# -------------------------------
elif st.session_state.page == "dataset":
    st.header("📊 Dataset Overview")
    st.write(data.head())

# -------------------------------
# INPUT PAGE
# -------------------------------
elif st.session_state.page == "input":
    st.header("🌿 Enter Environmental Conditions")

    col1, col2, col3 = st.columns(3)
    temperature = col1.number_input("Temperature (°C)", 10.0, 45.0, 28.0)
    humidity = col2.number_input("Humidity (%)", 10.0, 100.0, 60.0)
    soil_moisture = col3.number_input("Soil Moisture (%)", 5.0, 60.0, 25.0)

    col4, col5, col6 = st.columns(3)
    rainfall = col4.number_input("Rainfall (mm)", 0.0, 50.0, 0.0)
    ph = col5.number_input("Soil pH", 3.0, 9.0, 6.5)
    wind_speed = col6.number_input("Wind Speed (km/h)", 0.0, 40.0, 5.0)

    if st.button("➡️ Get Result"):
        st.session_state.soil_moisture = soil_moisture
        st.session_state.page = "result"

# -------------------------------
# RESULT PAGE
# -------------------------------
elif st.session_state.page == "result":
    st.header("🚰 Irrigation Result")

    soil_moisture = st.session_state.get("soil_moisture", 25)

    if soil_moisture < 30:
        st.success("💧 Irrigation ON")
    else:
        st.warning("🚫 Irrigation OFF")

    st.metric("🌱 Soil Moisture", soil_moisture)

    if st.button("🔙 Back"):
        st.session_state.page = "input"

# -------------------------------
# FOOTER
# -------------------------------
st.divider()
st.caption("Developed by Ekamdeep Singh, Dheeraj Sharma, Nadeem Alam 🌿")
