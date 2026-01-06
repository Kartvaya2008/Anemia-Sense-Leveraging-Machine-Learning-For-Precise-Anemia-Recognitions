import streamlit as st
import numpy as np
import pickle

# -------------------------
# Config
# -------------------------
MODEL_FILENAME = "model.pkl"
FEATURE_ORDER = ["gender", "hemoglobin", "mch", "mchc", "mcv"]

st.set_page_config(
    page_title="AnemiaSense",
    page_icon="🩸",
    layout="centered"
)

# -------------------------
# Load Model
# -------------------------
def load_model():
    try:
        with open(MODEL_FILENAME, "rb") as f:
            return pickle.load(f)
    except:
        return None

model = load_model()

# -------------------------
# UI
# -------------------------
st.title("🩸 AnemiaSense")
st.caption("Simple ML-based anemia risk prediction tool")

st.divider()

# -------------------------
# Inputs
# -------------------------
st.subheader("Enter Blood Parameters")

col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox(
        "Gender",
        options=[0, 1],
        format_func=lambda x: "Male" if x == 0 else "Female"
    )
    hemoglobin = st.number_input("Hemoglobin (g/dL)", value=13.5)

with col2:
    mch = st.number_input("MCH", value=22.7)
    mchc = st.number_input("MCHC", value=29.1)
    mcv = st.number_input("MCV", value=83.7)

st.divider()

# -------------------------
# Predict
# -------------------------
if not model:
    st.warning("⚠️ model.pkl not found. Prediction disabled.")
else:
    if st.button("🔍 Predict Anemia"):
        features = np.array(
            [[gender, hemoglobin, mch, mchc, mcv]],
            dtype=float
        )

        try:
            prediction = model.predict(features)[0]

            if prediction == 0:
                st.success("✅ No Anemia Detected")
            else:
                st.error("❗ Anemia Detected")

            if hasattr(model, "predict_proba"):
                prob = model.predict_proba(features)[0][1]
                st.info(f"Anemia Risk Probability: **{prob*100:.1f}%**")

        except Exception as e:
            st.error(f"Prediction failed: {e}")

st.divider()
st.caption("Developed by Kartvaya Raikwar")
