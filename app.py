# IoT-Based Precision Irrigation System
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import requests

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Smart Irrigation", layout="wide")

# 🎨 PAGE BACKGROUND FUNCTION
def set_bg(image_url):
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .block-container {{
        background: rgba(0,0,0,0.55);
        padding: 20px;
        border-radius: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

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
# NAVIGATION
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
    set_bg("https://images.unsplash.com/photo-1500595046743-cd271d694d30")

    st.title("💧 Smart Precision Irrigation System")
    st.markdown("### 🌱 Welcome to Smart Farming System")
    st.info("AI + Weather based irrigation decision system")

    if st.button("🚀 Start"):
        st.session_state.page = "input"

# -------------------------------
# DATASET PAGE
# -------------------------------
elif st.session_state.page == "dataset":
    set_bg("https://images.unsplash.com/photo-1551288049-bebda4e38f71")

    st.header("📊 Dataset Overview")
    st.dataframe(data.head())

# -------------------------------
# INPUT PAGE (FIELD LOOK)
# -------------------------------
elif st.session_state.page == "input":
    set_bg("https://images.unsplash.com/photo-1464226184884-fa280b87c399")

    st.header("🌿 Enter Environmental Conditions")

    city = st.text_input("🌍 Enter City", "Delhi")

    if st.button("🌦️ Get Weather"):
        api_key = "YOUR_API_KEY_HERE"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url).json()

            if str(response.get("cod")) != "200":
                st.error(f"❌ {response.get('message')}")
            else:
                st.session_state["temp"] = response['main']['temp']
                st.session_state["humidity"] = response['main']['humidity']

                st.success(f"🌡 Temp: {st.session_state['temp']}°C | 💧 Humidity: {st.session_state['humidity']}%")

        except:
            st.error("⚠️ Network error")

    col1, col2, col3 = st.columns(3)
    soil_moisture = col1.number_input("Soil Moisture (%)", 5.0, 60.0, 25.0)
    rainfall = col2.number_input("Rainfall (mm)", 0.0, 50.0, 0.0)
    ph = col3.number_input("Soil pH", 3.0, 9.0, 6.5)

    if st.button("➡️ Get Result"):
        st.session_state.soil_moisture = soil_moisture
        st.session_state.page = "result"

# -------------------------------
# RESULT PAGE (IRRIGATION LOOK)
# -------------------------------
elif st.session_state.page == "result":
    set_bg("https://images.unsplash.com/photo-1501004318641-b39e6451bec6")

    st.header("🚰 Irrigation Decision")

    soil_moisture = st.session_state.get("soil_moisture", 25)
    temp = st.session_state.get("temp", "N/A")
    humidity = st.session_state.get("humidity", "N/A")

    irrigation_on = soil_moisture < 30
    status_text = "💧 Irrigation ON" if irrigation_on else "🚫 Irrigation OFF"
    bg_color = "rgba(0,255,0,0.25)" if irrigation_on else "rgba(255,0,0,0.25)"

    st.markdown(f"""
    <div style='
        backdrop-filter: blur(10px);
        background: {bg_color};
        padding:20px;
        border-radius:15px;
        color:white;
        text-align:center;
    '>
        <h2>{status_text}</h2>
        <h4>🌱 Soil Moisture: {soil_moisture}</h4>
        <h4>🌡 Temperature: {temp}</h4>
        <h4>💧 Humidity: {humidity}</h4>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔙 Back"):
        st.session_state.page = "input"

# -------------------------------
# FOOTER
# -------------------------------
st.divider()
st.caption("Developed by Ekamdeep Singh, Dheeraj Sharma, Nadeem Alam 🌿")
