
---

# 🌱 Smart Irrigation System using LSTM | Time-Series Forecasting, Streamlit

### 🔮 Smart Farming Automation Using AI & IoT

This project presents an **AI-powered Smart Irrigation System** that uses **LSTM (Long Short-Term Memory) neural networks** to predict **water usage efficiency** based on environmental conditions. The system recommends whether irrigation should be **ON or OFF**, helping farmers make data-driven decisions, conserve water, and improve crop productivity.

The entire solution is deployed using an interactive **Streamlit dashboard**.

---

## 🚀 Features

* 🤖 **LSTM model** predicts water usage efficiency
* 🌦️ Real-time environmental input through Streamlit UI
* 🚰 Automatic irrigation status (ON/OFF)
* 📊 Model performance metrics (MAE, MSE, RMSE, R²)
* 📈 True vs Predicted visualization
* 🔄 Complete preprocessing pipeline (Label Encoding + Scaling)
* 💧 Supports sustainable and smart agriculture

---

## 🧰 Tech Stack

| Component     | Technology                |
| ------------- | ------------------------- |
| Frontend UI   | Streamlit                 |
| Deep Learning | TensorFlow / Keras (LSTM) |
| ML Processing | Scikit-learn              |
| Data Handling | Pandas, NumPy             |
| Visualization | Matplotlib                |

---

## 📂 Dataset

The project uses **Crop_recommendationV2.csv**, containing:

* Temperature
* Humidity
* Soil Moisture
* Rainfall
* Soil pH
* Soil Type
* Sunlight Exposure
* Water Source Type
* Water Usage Efficiency (Target)

---

## 🧠 LSTM Model Architecture

```
LSTM(128, return_sequences=True)
Dropout(0.3)
LSTM(64)
Dropout(0.3)
Dense(32, activation='relu')
Dense(1, activation='linear')
```

* Loss: **MSE**
* Optimizer: **Adam**
* Epochs: **100**
* Batch Size: **32**

---

## 📊 Model Performance Metrics

* **MAE**
* **MSE**
* **RMSE**
* **R² Score**
* Line graph: True vs Predicted values

These are displayed inside the Streamlit dashboard.

---

## 🖥️ Streamlit Features

* Sidebar: Dataset preview
* User input section for environmental conditions
* Real-time prediction using the trained LSTM model
* Irrigation status displayed clearly
* Visualization & performance metrics

---

## 📁 Project Structure

```
📦 IoT-Precision-Irrigation-LSTM
│── app.py
│── Crop_recommendationV2.csv
│── requirements.txt
│── README.md
└── assets/ (optional)
```

---

## ▶️ How to Run This Project

### 1️⃣ Install required packages

```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Streamlit app

```bash
streamlit run app.py
```

Your dashboard will open automatically in the browser.

---

## 🤝 Contributors

👨‍💻 **Udit Jain & Team**
*IoT | Data Science | Smart Farming Innovation*

---

## 🌿 Vision

To create an intelligent, sensor-driven irrigation system that improves agricultural efficiency, reduces water wastage, and helps farmers adopt **smart & sustainable farming practices** powered by AI.

---
