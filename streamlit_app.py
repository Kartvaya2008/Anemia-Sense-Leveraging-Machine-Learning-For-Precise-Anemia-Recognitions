# app.py
import streamlit as st
import numpy as np
import pickle
from datetime import datetime

# -------------------------
# Configuration
# -------------------------
MODEL_FILENAME = "model.pkl"
# Order of input features expected by the model
FEATURE_ORDER = ["gender", "hemoglobin", "mch", "mchc", "mcv"]

# -------------------------
# Page setup
# -------------------------
st.set_page_config(page_title="AnemiaSense", page_icon="🩸", layout="centered")

# -------------------------
# Minimal CSS for premium neon + layout
# Uses prefers-color-scheme to adapt to Light/Dark modes
# -------------------------
CSS = """
<style>
:root{
  --neon: #A855FF;
  --neon-2: #C67FFF;
  --muted-light: #6B6B6B;
  --label-neon: #B18BE8;
  --glass-light: rgba(255,255,255,0.7);
  --glass-dark: rgba(255,255,255,0.04);
  --card-bg-light: rgba(255,255,255,0.9);
  --card-bg-dark: rgba(255,255,255,0.02);
  --shadow: 0 10px 30px rgba(11,7,28,0.10);
  --radius: 14px;
}

@media (prefers-color-scheme: light) {
  body { background: linear-gradient(180deg,#EDE7FF 0%, #D4CCFF 100%); }
  .glass-nav { background: rgba(255,255,255,0.65); color:#111; box-shadow: var(--shadow); }
  .input-card { background: var(--card-bg-light); color:#111; border: 1px solid rgba(10,10,10,0.04); }
  .result-card { background: white; color:#111; }
  .nav-link { color:#333; }
}
@media (prefers-color-scheme: dark) {
  body { background: linear-gradient(180deg,#0E061A 0%, #2D1D45 100%); }
  .glass-nav { background: rgba(255,255,255,0.04); color:#eee; backdrop-filter: blur(8px); box-shadow: 0 6px 20px rgba(0,0,0,0.45); }
  .input-card { background: var(--card-bg-dark); color:#eee; border: 1px solid rgba(255,255,255,0.03); }
  .result-card { background: rgba(255,255,255,0.02); color:#fff; }
  .nav-link { color:#ddd; }
}

/* layout container */
.main-container { max-width: 1100px; margin: 22px auto; padding: 18px; }

/* glass nav */
.glass-nav {
  display:flex; align-items:center; justify-content:space-between;
  padding:10px 16px; border-radius:999px; margin-bottom:18px;
}
.nav-left { display:flex; gap:18px; align-items:center; font-size:14px; }
.nav-right { display:flex; gap:12px; align-items:center; }
.start-pill {
  border-radius:999px; padding:6px 14px; font-weight:600; border:1.5px solid rgba(168,85,255,0.85);
  background: transparent;
}

/* hero */
.hero { display:flex; gap:24px; align-items:center; justify-content:space-between; margin-bottom:20px; }
.hero-left { flex:1; min-width:260px; }
.hero-right { width:320px; display:flex; gap:14px; flex-direction:column; align-items:center; }

/* profile ring */
.profile-ring { width:110px; height:110px; border-radius:999px; display:flex; align-items:center; justify-content:center;
  box-shadow: 0 10px 30px rgba(168,85,255,0.12); border: 2px solid rgba(168,85,255,0.08);
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.00));
}

/* title */
.hero-title { font-size:30px; font-weight:700; line-height:1.05; margin-bottom:6px;
  background: linear-gradient(90deg,#A855FF,#FF7AE5); -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  letter-spacing:0.4px;
}
.hero-sub { font-size:15px; color:var(--muted-light); margin-bottom:12px; }

/* features */
.feature-row { display:flex; gap:10px; flex-wrap:wrap; margin-top:10px; }
.feature-badge { padding:8px 12px; border-radius:999px; font-size:13px; display:flex; gap:8px; align-items:center;
  backdrop-filter: blur(6px); border:1px solid rgba(255,255,255,0.04);
  box-shadow: 0 6px 18px rgba(10,10,10,0.06);
}

/* side cards */
.side-card { width:100%; padding:12px; border-radius:12px; text-align:center; box-shadow: 0 8px 26px rgba(11,7,28,0.10); }

/* input area */
.form-area { margin-top:18px; display:flex; flex-direction:column; gap:18px; align-items:center; }
.inputs-grid { display:grid; gap:14px; grid-template-columns: repeat(3,1fr); width:100%; }
.row-2 { display:grid; gap:14px; grid-template-columns: repeat(2,1fr); width:70%; margin: 0 auto; }

/* input card */
.input-card { padding:12px; border-radius:14px; display:flex; flex-direction:column; gap:8px; }
.input-label { font-size:12px; color:var(--label-neon); margin-bottom:6px; }
.input-row { display:flex; align-items:center; gap:8px; }
.input-emoji { font-size:16px; width:22px; text-align:center; }

/* custom input style for number fields to show glow on focus */
.neon-input input[type="number"], .neon-input select {
  width:100%; padding:10px 12px; border-radius:10px; border:1px solid transparent; outline:none;
  background: transparent; color:inherit; font-size:15px;
}
.neon-input input[type="number"]::-webkit-outer-spin-button,
.neon-input input[type="number"]::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }

/* focus */
.neon-input:focus-within { box-shadow: 0 6px 28px rgba(168,85,255,0.14); border-radius:12px; }

/* unit text on right */
.unit-text { font-size:13px; color:inherit; opacity:0.9; }

/* submit button */
.cta-row { margin-top:8px; display:flex; justify-content:center; }
.cta-btn {
  background: linear-gradient(90deg,#9C5CFF,#FF77D4); color:white; padding:12px 28px; border-radius:999px; border:none;
  font-weight:700; box-shadow: 0 12px 36px rgba(183,132,255,0.12); cursor:pointer;
}
.cta-btn:hover { transform: translateY(-2px); box-shadow: 0 18px 46px rgba(183,132,255,0.22); }

/* result card */
.result-card {
  margin-top:12px; padding:14px 18px; border-radius:12px; display:flex; gap:12px; align-items:center; justify-content:center;
  box-shadow: 0 12px 36px rgba(168,85,255,0.08);
}

@media (max-width:900px) {
  .hero { flex-direction:column; align-items:flex-start; gap:14px; }
  .inputs-grid { grid-template-columns: 1fr; width:100%; }
  .row-2 { grid-template-columns: 1fr; width:100%; }
  .hero-title { font-size:24px; }
  .profile-ring { width:88px; height:88px; }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# -------------------------
# Helper: model loader
# -------------------------
def load_model(path):
    try:
        with open(path, "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        return None
    except Exception:
        return None

# -------------------------
# Simple router using session_state
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

def go_main():
    st.session_state.page = "main"

# -------------------------
# Landing Page (premium AIVA)
# -------------------------
def render_landing():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Glass nav
    st.markdown('<div class="glass-nav"><div class="nav-left">'
                '<div style="font-weight:700;">AnemiaSense</div>'
                '<div class="nav-link">Home</div>'
                '<div class="nav-link">About Project</div>'
                '<div class="nav-link">How it works</div>'
                '<div class="nav-link">Model Info</div>'
                '<div class="nav-link">Contact</div>'
                '</div><div class="nav-right">'
                '<div class="start-pill">Start</div>'
                '</div></div>', unsafe_allow_html=True)

    # Hero section
    st.markdown('<div class="hero"><div class="hero-left">', unsafe_allow_html=True)
    st.markdown('<div class="profile-ring"><div style="width:84px;height:84px;border-radius:999px;background:linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));"></div></div>', unsafe_allow_html=True)
    st.markdown('</div><div class="hero-right">', unsafe_allow_html=True)

    # Title and subtitle (right aligned area for visual balance)
    st.markdown('<div style="text-align:left;"><div class="hero-title">Hi, I\'m AnemiaSense — Your AI-Powered Health Assistant</div>'
                '<div class="hero-sub">Check your blood parameters and detect anemia risk instantly — powered by machine learning and modern health analytics.</div>'
                '</div>', unsafe_allow_html=True)

    # Feature badges
    st.markdown('<div class="feature-row">'
                '<div class="feature-badge">⚡&nbsp;<div style="font-size:13px">Fast Detection</div></div>'
                '<div class="feature-badge">🧬&nbsp;<div style="font-size:13px">ML-Based Analysis</div></div>'
                '<div class="feature-badge">📊&nbsp;<div style="font-size:13px">Clear Visualization</div></div>'
                '<div class="feature-badge">🔐&nbsp;<div style="font-size:13px">Secure & Private</div></div>'
                '</div>', unsafe_allow_html=True)

    # CTA
    if st.button("Start Anemia Check", key="landing_cta"):
        go_main()

    st.markdown('</div></div>', unsafe_allow_html=True)  # close hero
    st.markdown('</div>', unsafe_allow_html=True)  # close container

# -------------------------
# Main Page (inputs + predict)
# -------------------------
def render_main():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="margin:6px 0 2px 0;">Anemia Prediction</h2>', unsafe_allow_html=True)
    st.markdown('<div style="color:var(--muted-light); margin-bottom:8px;">Enter the blood parameters below and click Predict Anemia.</div>', unsafe_allow_html=True)

    # Load model once (if present)
    model = load_model(MODEL_FILENAME)
    model_available = model is not None

    # Input grid (3 on top)
    st.markdown('<div class="form-area">', unsafe_allow_html=True)
    st.markdown('<div class="inputs-grid">', unsafe_allow_html=True)

    # Box 1 - Gender
    st.markdown('<div class="input-card input-card" style="min-height:88px;">', unsafe_allow_html=True)
    st.markdown('<div class="input-label">👤 Gender</div>', unsafe_allow_html=True)
    gender = st.selectbox("", options=[0, 1], format_func=lambda x: "Male (0)" if x == 0 else "Female (1)", key="gender_select")
    st.markdown('</div>', unsafe_allow_html=True)

    # Box 2 - Hemoglobin
    st.markdown('<div class="input-card input-card neon-input">', unsafe_allow_html=True)
    st.markdown('<div class="input-label">🩸 Hemoglobin <span style="font-size:12px;color:var(--label-neon)">(g/dL)</span></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([5,1])
    with col1:
        hemoglobin = st.number_input("", min_value=0.0, format="%.2f", value=13.50, key="hemoglobin")
    with col2:
        st.markdown('<div class="unit-text">g/dL</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Box 3 - MCH
    st.markdown('<div class="input-card input-card neon-input">', unsafe_allow_html=True)
    st.markdown('<div class="input-label">🧬 MCH</div>', unsafe_allow_html=True)
    mch = st.number_input("", min_value=0.0, format="%.2f", value=22.70, key="mch")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # end inputs-grid

    # Second row (2 boxes)
    st.markdown('<div class="row-2">', unsafe_allow_html=True)

    # Box 4 - MCHC
    st.markdown('<div class="input-card input-card neon-input">', unsafe_allow_html=True)
    st.markdown('<div class="input-label">⚗️ MCHC</div>', unsafe_allow_html=True)
    mchc = st.number_input("", min_value=0.0, format="%.2f", value=29.10, key="mchc")
    st.markdown('</div>', unsafe_allow_html=True)

    # Box 5 - MCV
    st.markdown('<div class="input-card input-card neon-input">', unsafe_allow_html=True)
    st.markdown('<div class="input-label">📊 MCV</div>', unsafe_allow_html=True)
    mcv = st.number_input("", min_value=0.0, format="%.2f", value=83.70, key="mcv")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # end row-2

    # Submit CTA
    st.markdown('<div class="cta-row">', unsafe_allow_html=True)
    disabled = not model_available
    if disabled:
        st_button = st.button("Predict Anemia", key="predict_btn", disabled=True)
    else:
        st_button = st.button("Predict Anemia", key="predict_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    # Result area placeholder
    result_placeholder = st.empty()

    # Validation & Predict flow
    if st_button:
        errors = []
        # gender validation
        if gender not in (0, 1):
            errors.append("Gender must be 0 (Male) or 1 (Female).")
        # numeric validations
        numeric_fields = {"Hemoglobin": hemoglobin, "MCH": mch, "MCHC": mchc, "MCV": mcv}
        for name, val in numeric_fields.items():
            try:
                v = float(val)
                if v < 0:
                    errors.append(f"{name} must be non-negative.")
            except Exception:
                errors.append(f"{name} must be a number.")
        if errors:
            for e in errors:
                result_placeholder.error(e)
        else:
            # Prepare input vector in FEATURE_ORDER
            mapping = {"gender": gender, "hemoglobin": hemoglobin, "mch": mch, "mchc": mchc, "mcv": mcv}
            try:
                feature_vector = [float(mapping.get(f, 0.0)) for f in FEATURE_ORDER]
            except Exception as ex:
                result_placeholder.error("Failed to prepare features: " + str(ex))
                st.stop()

            arr = np.array(feature_vector, dtype=float).reshape(1, -1)
            # Load model again just before predict (ensures latest)
            model = load_model(MODEL_FILENAME)
            if model is None:
                result_placeholder.error(f"Model file '{MODEL_FILENAME}' not found or failed to load. Place model in project root.")
            else:
                try:
                    pred = model.predict(arr)
                    label = int(pred[0]) if hasattr(pred, "__iter__") else int(pred)
                    prob_text = ""
                    if hasattr(model, "predict_proba"):
                        try:
                            proba = model.predict_proba(arr)
                            if proba.shape[1] > 1:
                                p = float(proba[0][1])
                                prob_text = f" • Risk: {p*100:.1f}%"
                        except Exception:
                            prob_text = ""
                    if label == 0:
                        # No anemia
                        result_placeholder.markdown(
                            f'<div class="result-card" style="border:1px solid rgba(0,255,0,0.06)"><div style="font-size:20px">💡 Result: No Anemia Detected</div><div style="margin-left:8px;color:var(--label-neon);font-size:13px">{prob_text}</div></div>',
                            unsafe_allow_html=True)
                    else:
                        result_placeholder.markdown(
                            f'<div class="result-card" style="border:1px solid rgba(255,100,100,0.06)"><div style="font-size:20px">💜 Result: Anemia Detected</div><div style="margin-left:8px;color:var(--label-neon);font-size:13px">{prob_text}</div></div>',
                            unsafe_allow_html=True)
                except Exception as ex:
                    result_placeholder.error("Prediction failed: " + str(ex))

    # Show model missing notice if disabled
    if not model_available:
        st.warning(f"Model file '{MODEL_FILENAME}' not found in project root. Prediction is disabled until a trained model file with the name is provided.")

    # Footer
    st.markdown('<div style="text-align:center; margin-top:18px; color:var(--label-neon); font-size:13px;">Developed by Kartvaya Raikwar</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # close main container

# -------------------------
# Router
# -------------------------
if st.session_state.page == "landing":
    render_landing()
else:
    render_main()
