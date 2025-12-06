import streamlit as st
import numpy as np
import pickle

# -----------------------------
# Load trained ML model
# -----------------------------
# Make sure file name is exactly "model.pkl" in the repo
model = pickle.load(open("model.pkl", "rb"))

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="AnemiaSense – Anemia Prediction",
    page_icon="🩸",
    layout="centered"
)

# -----------------------------
# UI – left text, right form style (simple)
# -----------------------------
st.markdown("## 🩸 AnemiaSense – Early Anemia Prediction System")
st.write(
    "Enter your basic blood report values below and get an **ML-based anemia risk** "
    "prediction. This is only for **project / demo use**, not real medical advice."
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", options=[0, 1], format_func=lambda x: "Male (0)" if x == 0 else "Female (1)")
    hb = st.number_input("Hemoglobin (g/dL)", min_value=0.0, max_value=25.0, value=13.0, step=0.1)
    pcv = st.number_input("PCV (%)", min_value=0.0, max_value=80.0, value=40.0, step=0.1)

with col2:
    mcv = st.number_input("MCV (fL)", min_value=0.0, max_value=130.0, value=88.0, step=0.1)
    mchc = st.number_input("MCHC (g/dL)", min_value=0.0, max_value=45.0, value=32.0, step=0.1)

st.markdown("")

if st.button("🔍 Predict Anemia Risk"):
    # input shape: [[Gender, Hemoglobin, PCV, MCV, MCHC]]
    input_data = np.array([[gender, hb, pcv, mcv, mchc]])
    pred = model.predict(input_data)[0]

    if pred == 0:
        st.success("✅ Prediction: **You are not anemic (No anemia detected).**")
    else:
        st.error("⚠️ Prediction: **You have anemia (anemic condition detected).**")

    st.caption("Note: This result is only for educational/demo purpose, not a medical diagnosis.")
