# IoT-Based Precision Irrigation System using LSTM
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# -------------------------------
# 1️⃣ PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="IoT-Based Smart Irrigation", layout="wide")
st.title("💧 IoT-Based Precision Irrigation System using LSTM")

# -------------------------------
# 2️⃣ LOAD DATASET
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Crop_recommendationV2.csv")
    return df

data = load_data()
st.sidebar.header("📊 Dataset Overview")
st.sidebar.write(data.head())

# -------------------------------
# 3️⃣ PREPROCESSING
# -------------------------------
cat_cols = ['soil_type', 'sunlight_exposure', 'water_source_type']
for col in cat_cols:
    data[col] = LabelEncoder().fit_transform(data[col].astype(str))

X = data.drop(columns=['label'])
y = data['water_usage_efficiency']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = np.reshape(X_scaled, (X_scaled.shape[0], 1, X_scaled.shape[1]))

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# -------------------------------
# 4️⃣ MODEL TRAINING (LSTM)
# -------------------------------
@st.cache_resource
def train_model():
    model = Sequential([
        LSTM(128, input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True),
        Dropout(0.3),
        LSTM(64, return_sequences=False),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dense(1, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=0, validation_split=0.2)
    return model

with st.spinner("Training model... ⏳"):
    model = train_model()
st.success("✅ Model trained successfully!")

# -------------------------------
# 5️⃣ USER INPUT SECTION
# -------------------------------
st.header("🌿 Input Environmental Conditions")

col1, col2, col3 = st.columns(3)
temperature = col1.number_input("Temperature (°C)", 10.0, 45.0, 28.0)
humidity = col2.number_input("Humidity (%)", 10.0, 100.0, 60.0)
soil_moisture = col3.number_input("Soil Moisture (%)", 5.0, 60.0, 25.0)

col4, col5, col6 = st.columns(3)
rainfall = col4.number_input("Rainfall (mm)", 0.0, 50.0, 0.0)
ph = col5.number_input("Soil pH", 3.0, 9.0, 6.5)
wind_speed = col6.number_input("Wind Speed (km/h)", 0.0, 40.0, 5.0)

# Create input row
sample_row = data.sample(1).copy()
sample_row['temperature'] = temperature
sample_row['humidity'] = humidity
sample_row['soil_moisture'] = soil_moisture
sample_row['rainfall'] = rainfall
sample_row['ph'] = ph
sample_row['wind_speed'] = wind_speed

# Preprocess input
X_in = scaler.transform(sample_row.drop(columns=['label']))
X_in = np.reshape(X_in, (X_in.shape[0], 1, X_in.shape[1]))

# -------------------------------
# 6️⃣ PREDICTION
# -------------------------------
prediction = model.predict(X_in)[0][0]
threshold = y.mean()
status = "💧 Irrigation ON" if prediction > threshold else "🌤️ Irrigation OFF"

st.subheader("🔮 Predicted Water Requirement")
st.metric(label="Predicted water usage efficiency", value=f"{prediction:.2f}")
st.subheader("🚰 Irrigation Status")
st.success(status if "ON" in status else status)

# -------------------------------
# 7️⃣ MODEL PERFORMANCE
# -------------------------------
y_pred = model.predict(X_test).flatten()

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

st.header("📈 Model Performance Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Mean Absolute Error (MAE)", f"{mae:.3f}")
col2.metric("Mean Squared Error (MSE)", f"{mse:.3f}")
col3.metric("Root Mean Squared Error (RMSE)", f"{rmse:.3f}")
col4.metric("R² Score", f"{r2:.3f}")

# -------------------------------
# 8️⃣ VISUALIZATION
# -------------------------------
st.header("📊 True vs Predicted Water Usage Efficiency")
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(y_test[:100].values, label='True Values', color='blue')
ax.plot(y_pred[:100], label='Predicted', color='red')
ax.legend()
ax.set_xlabel("Samples")
ax.set_ylabel("Efficiency")
st.pyplot(fig)

st.caption("Developed by Udit Jain & Team 🌿 | IoT-based Smart Farming")
