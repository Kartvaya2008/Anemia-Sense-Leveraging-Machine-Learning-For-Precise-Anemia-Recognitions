import streamlit as st
import numpy as np
import pickle

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="AnemiaSense – Prediction App",
    page_icon="🩸",
    layout="centered"
)

# -------------------- Custom CSS (Modern UI) --------------------
st.markdown("""
<style>
/* Center Main Title */
h1 {
    text-align: center;
    color: #B80000;
}

/* Input card style */
.stButton>button {
    background-color: #B80000;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
}
.stButton>button:hover {
    background-color: #8A0000;
}
div[data-testid="stNumberInput"] {
    background:#FFF5F5;
    padding:10px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- Title Section --------------------
st.title("🩸 AnemiaSense – Basic Anemia Prediction")
st.write("Enter the blood parameters below to predict anemia status.")

# -------------------- Load Model --------------------
try:
    model = pickle.load(open("model.pkl", "rb"))
    model_loaded = True
except:
    st.error("⚠ model.pkl not found in project folder.")
    model_loaded = False

# -------------------- Input Form --------------------
st.subheader("🧬 Enter Patient Details")

gender = st.selectbox(
    "Gender",
    options=[0, 1],
    format_func=lambda x: "Male" if x == 0 else "Female"
)

hb = st.number_input("Hemoglobin (g/dL)", 0.0, 25.0, 11.6, 0.1)
pcv = st.number_input("PCV (%)", 0.0, 80.0, 22.3, 0.1)
mcv = st.number_input("MCV (fL)", 0.0, 130.0, 30.9, 0.1)
mchc = st.number_input("MCHC (g/dL)", 0.0, 45.0, 33.0, 0.1)

# -------------------- Prediction Button --------------------
if st.button("Predict Anemia"):
    if model_loaded:
        input_data = np.array([[gender, hb, pcv, mcv, mchc]])
        pred = model.predict(input_data)[0]

        st.subheader("🔍 Prediction Result")
        if pred == 0:
            st.success("✔ You do NOT have anemia.")
        else:
            st.error("❗ You HAVE anemia.")
