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
# FARM SOFT UI STYLE (FINAL FIX)
# -------------------------------
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* MAIN CONTAINER */
.block-container {
    background: rgba(255,255,255,0.10) !important;
    backdrop-filter: blur(6px);
    padding: 20px;
    border-radius: 15px;
}

/* FARM CARD */
.card {
    background: rgba(255,255,255,0.18);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: #1b1b1b;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
}

/* HEADINGS */
h1, h2, h3 {
    color: #1b5e20 !important;
}

/* TEXT */
p {
    color: #2d3436 !important;
}

/* ============================= */
/* ✅ FIX INPUT VISIBILITY FULL */
/* ============================= */

label {
    color: #1b5e20 !important;
    font-weight: 600 !important;
}

/* input boxes */
.stTextInput input,
.stNumberInput input {
    background-color: #ffffff !important;
    color: #000000 !important;
    border-radius: 10px !important;
    border: 1px solid #cfd8dc !important;
    padding: 8px !important;
}

/* input container */
.stTextInput, .stNumberInput {
    background: rgba(255,255,255,0.70) !important;
    padding: 6px;
    border-radius: 10px;
}

/* focus effect */
.stTextInput input:focus,
.stNumberInput input:focus {
    border: 2px solid #4caf50 !important;
    outline: none !important;
}

/* BUTTON */
.stButton>button {
    background: #4caf50;
    color: white;
    border-radius: 10px;
    padding: 10px 15px;
    font-weight: 600;
}

.stButton>button:hover {
    background: #388e3c;
}

/* CENTER SPINNER FIX */
div[data-testid="stSpinner"] {
    display: flex;
    justify-content: center;
    align-items: center;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# BACKGROUND FUNCTION
# -------------------------------
def set_bg(image_url):
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{image_url}");
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
# HOME PAGE 🌾
# -------------------------------
if st.session_state.page == "home":
    set_bg("https://images.unsplash.com/photo-1461354464878-ad92f492a5a0")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("🌱 Smart Farming Irrigation System")
    st.markdown("🚜 AI powered water optimization for crops")
    st.info("Helping farmers save water & improve yield 🌾")

    if st.button("🚀 Start Monitoring"):
        st.session_state.page = "input"

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# DATASET PAGE 📊
# -------------------------------
elif st.session_state.page == "dataset":
    set_bg("https://images.unsplash.com/photo-1551288049-bebda4e38f71")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📊 Crop Dataset Overview")
    st.dataframe(data.head())
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# INPUT PAGE 🌿 (FIXED PERFECT)
# -------------------------------
elif st.session_state.page == "input":
    set_bg("https://images.unsplash.com/photo-1500937386664-56d1dfef3854")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.header("🌾 Field Condition Input Panel")

    city = st.text_input("🌍 Enter City", "Delhi")

    if st.button("🌦 Get Weather Data"):
        api_key = "YOUR_API_KEY_HERE"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url).json()

            if str(response.get("cod")) != "200":
                st.error("❌ City not found")
            else:
                st.session_state["temp"] = response['main']['temp']
                st.session_state["humidity"] = response['main']['humidity']

                st.success(f"🌡 {st.session_state['temp']}°C | 💧 {st.session_state['humidity']}%")

        except:
            st.error("⚠ Network Error")

    col1, col2, col3 = st.columns(3)

    soil_moisture = col1.number_input("🌱 Soil Moisture (%)", 5.0, 60.0, 25.0)
    rainfall = col2.number_input("🌧 Rainfall (mm)", 0.0, 50.0, 0.0)
    ph = col3.number_input("⚗ Soil pH", 3.0, 9.0, 6.5)

    if st.button("🚜 Analyze Field"):
        st.session_state.soil_moisture = soil_moisture
        st.session_state.page = "result"

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# RESULT PAGE 🚰 (FINAL CLEAN UI)
# -------------------------------
elif st.session_state.page == "result":
    set_bg("https://images.unsplash.com/photo-1501004318641-b39e6451bec6")

    soil_moisture = st.session_state.get("soil_moisture", 25)
    temp = st.session_state.get("temp", "N/A")
    humidity = st.session_state.get("humidity", "N/A")

    irrigation_on = soil_moisture < 30

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.header("🌾 Smart Farm Irrigation Report")

    # 🌟 UNIQUE OUTPUT UI
    if irrigation_on:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #43cea2, #185a9d);
            padding:20px;
            border-radius:15px;
            color:white;
            text-align:center;">
            <h2>💧 FARM ALERT: WATER NEEDED</h2>
            <p>🌱 Soil moisture is low — irrigation recommended</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #56ccf2, #2f80ed);
            padding:20px;
            border-radius:15px;
            color:white;
            text-align:center;">
            <h2>🌿 FARM STATUS: HEALTHY</h2>
            <p>🚫 No irrigation required currently</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.metric("🌱 Soil Moisture", f"{soil_moisture}%")
    col2.metric("🌡 Temperature", f"{temp}°C")
    col3.metric("💧 Humidity", f"{humidity}%")

    if st.button("🔙 Back to Field"):
        st.session_state.page = "input"

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# FOOTER 🌿
# -------------------------------
st.divider()
st.caption("Developed by Ekamdeep Singh, Dheeraj Sharma, Nadeem Alam 🌿")
