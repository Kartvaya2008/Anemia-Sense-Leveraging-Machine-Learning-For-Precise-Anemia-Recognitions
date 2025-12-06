import streamlit as st
import numpy as np
import pickle

st.set_page_config(page_title="AnemiaSense", page_icon="🩸", layout="centered")

# ---------------- CSS FOR CHATGPT-STYLE HEADING ----------------
st.markdown("""
<style>
.big-title {
    font-size: 40px;
    font-weight: 700;
    color: #111;
}
.gradient-text {
    background: linear-gradient(90deg, #8a2be2, #6366f1);
    -webkit-background-clip: text;
    color: transparent;
    font-weight: 700;
}
.subtitle {
    font-size: 22px;
    color: #555;
    margin-top: -15px;
    margin-bottom: 30px;
}
.box {
    background: #ffffff;
    padding: 30px;
    border-radius: 12px;
    border: 1px solid #ededed;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER TEXT (CHATGPT STYLE) ----------------
st.markdown('<p class="big-title">Hi there, <span class="gradient-text">Kartvaya</span></p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">What would you like to check today?</p>', unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
try:
    model = pickle.load(open("model.pkl", "rb"))
    model_loaded = True
except:
    st.error("Model file `model.pkl` not found.")
    model_loaded = False

# ---------------- INPUT FORM BOX ----------------
st.markdown('<div class="box">', unsafe_allow_html=True)

gender = st.selectbox("Gender", [0, 1], format_func=lambda x: "Male" if x == 0 else "Female")
hb = st.number_input("Hemoglobin (g/dL)", value=11.6)
pcv = st.number_input("PCV (%)", value=22.3)
mcv = st.number_input("MCV (fL)", value=30.9)
mchc = st.number_input("MCHC (g/dL)", value=33.0)

if st.button("Predict"):
    if model_loaded:
        data = np.array([[gender, hb, pcv, mcv, mchc]])
        pred = model.predict(data)[0]

        if pred == 0:
            st.success("✔ You do NOT have anemia.")
        else:
            st.error("❗ You have anemia.")

st.markdown("</div>", unsafe_allow_html=True)
