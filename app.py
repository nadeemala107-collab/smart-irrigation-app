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
# SOFT UI STYLE (FIXED + BLAND LOOK)
# -------------------------------
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* CLEAN CONTAINER */
.block-container {
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(6px);
    padding: 20px;
}

/* SOFT CARD */
.card {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 15px;
    color: #f5f5f5;
    text-align: center;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
}

/* TEXT SOFT (NOT HARSH WHITE) */
h1, h2, h3, h4, p, label {
    color: #f1f1f1 !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

/* INPUT CLEAN */
input {
    background: rgba(255,255,255,0.95) !important;
    color: black !important;
    border-radius: 10px !important;
}

/* BUTTON SOFT GREEN */
.stButton>button {
    background: #4CAF50;
    color: white;
    border-radius: 10px;
    padding: 10px 16px;
    font-weight: 500;
}

.stButton>button:hover {
    background: #43a047;
}

/* CENTER LOADER */
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
# HOME PAGE (SOFT FARM LOOK)
# -------------------------------
if st.session_state.page == "home":
    set_bg("https://images.unsplash.com/photo-1461354464878-ad92f492a5a0")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("💧 Smart Precision Irrigation System")
    st.markdown("### 🌱 Smart Farming Made Simple")
    st.info("AI + Weather based irrigation system")

    if st.button("🚀 Start System"):
        st.session_state.page = "input"

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# DATASET PAGE
# -------------------------------
elif st.session_state.page == "dataset":
    set_bg("https://images.unsplash.com/photo-1551288049-bebda4e38f71")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("📊 Dataset Overview")
    st.dataframe(data.head())
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# INPUT PAGE (FIELD + SKY SOFT)
# -------------------------------
elif st.session_state.page == "input":
    set_bg("https://images.unsplash.com/photo-1500595046743-cd271d694d30")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🌿 Farm Conditions Input")

    city = st.text_input("🌍 Enter City", "Delhi")

    if st.button("🌦️ Get Weather"):
        api_key = "YOUR_API_KEY_HERE"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url).json()

            if str(response.get("cod")) != "200":
                st.error("❌ Invalid City")
            else:
                st.session_state["temp"] = response['main']['temp']
                st.session_state["humidity"] = response['main']['humidity']

                st.success(f"🌡 {st.session_state['temp']}°C | 💧 {st.session_state['humidity']}%")

        except:
            st.error("⚠️ Network Error")

    col1, col2, col3 = st.columns(3)
    soil_moisture = col1.number_input("Soil Moisture (%)", 5.0, 60.0, 25.0)
    rainfall = col2.number_input("Rainfall (mm)", 0.0, 50.0, 0.0)
    ph = col3.number_input("Soil pH", 3.0, 9.0, 6.5)

    if st.button("➡️ Get Result"):
        st.session_state.soil_moisture = soil_moisture
        st.session_state.page = "result"

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# RESULT PAGE (CLEAN + VISIBLE)
# -------------------------------
elif st.session_state.page == "result":
    set_bg("https://images.unsplash.com/photo-1501004318641-b39e6451bec6")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🚰 Irrigation Decision Result")

    soil_moisture = st.session_state.get("soil_moisture", 25)
    temp = st.session_state.get("temp", "N/A")
    humidity = st.session_state.get("humidity", "N/A")

    if soil_moisture < 30:
        st.success("💧 Irrigation ON")
    else:
        st.info("🚫 Irrigation OFF")

    st.metric("🌱 Soil Moisture", soil_moisture)
    st.metric("🌡 Temperature", temp)
    st.metric("💧 Humidity", humidity)

    if st.button("🔙 Back"):
        st.session_state.page = "input"

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# FOOTER
# -------------------------------
st.divider()
st.caption("Developed by Ekamdeep Singh, Dheeraj Sharma, Nadeem Alam 🌿")
