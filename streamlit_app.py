import streamlit as st
import numpy as np
import pickle

# -------------------- Page Title --------------------
st.title("🩸 AnemiaSense – Basic Anemia Prediction App")
st.write("Enter the required blood parameters below to check anemia status.")

# -------------------- Load Model --------------------
try:
    model = pickle.load(open("model.pkl", "rb"))
    model_loaded = True
except:
    st.error("Model file `model.pkl` not found. Please upload it to the project folder.")
    model_loaded = False

# -------------------- Input Form --------------------
gender = st.selectbox("Gender", options=[0, 1], format_func=lambda x: "Male (0)" if x == 0 else "Female (1)")
hb = st.number_input("Hemoglobin (g/dL)", min_value=0.0, max_value=25.0, value=11.6, step=0.1)
pcv = st.number_input("PCV (%)", min_value=0.0, max_value=80.0, value=22.3, step=0.1)
mcv = st.number_input("MCV (fL)", min_value=0.0, max_value=130.0, value=30.9, step=0.1)
mchc = st.number_input("MCHC (g/dL)", min_value=0.0, max_value=45.0, value=33.0, step=0.1)

# -------------------- Prediction Button --------------------
if st.button("Predict"):
    if model_loaded:
        input_data = np.array([[gender, hb, pcv, mcv, mchc]])
        pred = model.predict(input_data)[0]

        st.subheader("🔍 Prediction Result:")
        if pred == 0:
            st.success("✔ You do NOT have anemia.")
        else:
            st.error("❗ You have anemia.")
