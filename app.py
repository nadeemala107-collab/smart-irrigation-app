# IoT-Based Precision Irrigation System
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

# -------------------------------
# 1️⃣ PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Smart Irrigation", layout="wide")
st.title("💧 Smart Precision Irrigation System")

# -------------------------------
# 2️⃣ LOAD DATASET
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("Crop_recommendationV2.csv")

data = load_data()

# -------------------------------
# 3️⃣ SIDEBAR NAVIGATION
# -------------------------------
page = st.sidebar.radio("📌 Navigation", 
                       ["📊 Dataset", "🌿 Input", "🚰 Result"])

# -------------------------------
# 4️⃣ PREPROCESSING (COMMON)
# -------------------------------
cat_cols = ['soil_type', 'sunlight_exposure', 'water_source_type']
for col in cat_cols:
    data[col] = LabelEncoder().fit_transform(data[col].astype(str))

X = data.drop(columns=['label'])

scaler = StandardScaler()
scaler.fit(X)

# -------------------------------
# 📊 PAGE 1: DATASET
# -------------------------------
if page == "📊 Dataset":
    st.header("📊 Dataset Overview")
    st.write(data.head())
    st.divider()
    st.info("This dataset is used to analyze irrigation conditions based on environmental factors.")

# -------------------------------
# 🌿 PAGE 2: INPUT
# -------------------------------
elif page == "🌿 Input":
    st.header("🌿 Enter Environmental Conditions")

    col1, col2, col3 = st.columns(3)
    temperature = col1.number_input("Temperature (°C)", 10.0, 45.0, 28.0)
    humidity = col2.number_input("Humidity (%)", 10.0, 100.0, 60.0)
    soil_moisture = col3.number_input("Soil Moisture (%)", 5.0, 60.0, 25.0)

    col4, col5, col6 = st.columns(3)
    rainfall = col4.number_input("Rainfall (mm)", 0.0, 50.0, 0.0)
    ph = col5.number_input("Soil pH", 3.0, 9.0, 6.5)
    wind_speed = col6.number_input("Wind Speed (km/h)", 0.0, 40.0, 5.0)

    # Save input to session
    st.session_state["soil_moisture"] = soil_moisture

    st.success("✅ Inputs saved! Go to Result page")

# -------------------------------
# 🚰 PAGE 3: RESULT
# -------------------------------
elif page == "🚰 Result":
    st.header("🚰 Irrigation Decision")

    soil_moisture = st.session_state.get("soil_moisture", 25)

    # Simple logic
    if soil_moisture < 30:
        status = "💧 Irrigation ON"
        st.success(status)
    else:
        status = "🚫 Irrigation OFF"
        st.warning(status)

    st.metric("🌱 Soil Moisture", soil_moisture)

    st.divider()
    st.caption("Developed by Ekamdeep Singh, Dheeraj Sharma, Nadeem Alam 🌿")
