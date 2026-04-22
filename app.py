# IoT-Based Precision Irrigation System
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import requests

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
# SESSION STATE
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# -------------------------------
# TOP NAV BUTTONS
# -------------------------------
col1, col2, col3 = st.columns([1,1,6])

with col1:
    if st.button("🏠 Home"):
        st.session_state.page = "home"

with col2:
    if st.button("📊 Dataset"):
        st.session_state.page = "dataset"

# -------------------------------
# PREPROCESSING
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
    st.info("AI + Weather based irrigation decision system")

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

    # 🌍 City Input
    city = st.text_input("🌍 Enter City", "Delhi")

    if st.button("🌦️ Get Weather"):
        api_key = "PASTE_YOUR_REAL_API_KEY_HERE"   # 🔑 IMPORTANT
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url).json()

            # Proper error handling
            if str(response.get("cod")) != "200":
                st.error(f"❌ Error: {response.get('message')}")
            else:
                temp = response['main']['temp']
                humidity = response['main']['humidity']

                st.session_state["temp"] = temp
                st.session_state["humidity"] = humidity

                st.success(f"🌡 Temp: {temp}°C | 💧 Humidity: {humidity}%")

        except:
            st.error("⚠️ Network error. Try again.")

    # Manual Inputs
    col1, col2, col3 = st.columns(3)
    soil_moisture = col1.number_input("Soil Moisture (%)", 5.0, 60.0, 25.0)
    rainfall = col2.number_input("Rainfall (mm)", 0.0, 50.0, 0.0)
    ph = col3.number_input("Soil pH", 3.0, 9.0, 6.5)

    if st.button("➡️ Get Result"):
        st.session_state.soil_moisture = soil_moisture
        st.session_state.page = "result"

# -------------------------------
# RESULT PAGE
# -------------------------------
elif st.session_state.page == "result":
    st.header("🚰 Irrigation Decision")

    soil_moisture = st.session_state.get("soil_moisture", 25)
    temp = st.session_state.get("temp", "N/A")
    humidity = st.session_state.get("humidity", "N/A")

    # 🎨 Color Card UI
    if soil_moisture < 30:
        st.markdown(f"""
        <div style='background-color:#d4edda;padding:20px;border-radius:12px'>
            <h2 style='color:green;'>💧 Irrigation ON</h2>
            <p>🌱 Soil Moisture: {soil_moisture}</p>
            <p>🌡 Temperature: {temp}</p>
            <p>💧 Humidity: {humidity}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background-color:#f8d7da;padding:20px;border-radius:12px'>
            <h2 style='color:red;'>🚫 Irrigation OFF</h2>
            <p>🌱 Soil Moisture: {soil_moisture}</p>
            <p>🌡 Temperature: {temp}</p>
            <p>💧 Humidity: {humidity}</p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🔙 Back"):
        st.session_state.page = "input"

# -------------------------------
# FOOTER
# -------------------------------
st.divider()
st.caption("Developed by Ekamdeep Singh, Dheeraj Sharma, Nadeem Alam 🌿")
