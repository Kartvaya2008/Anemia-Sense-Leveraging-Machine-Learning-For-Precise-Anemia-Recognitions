# app.py
import streamlit as st
import numpy as np
import pickle

# ========== BASIC PAGE SETTINGS ==========
st.set_page_config(
    page_title="AnemiaSense – Anemia Prediction",
    page_icon="🩸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ========== CUSTOM CSS FOR MODERN UI ==========
st.markdown("""
<style>
/* Remove big white rounded header box at top */
header[data-testid="stHeader"] {
    background: transparent !important;
}
header[data-testid="stHeader"] > div {
    background: transparent !important;
    box-shadow: none !important;
}
header[data-testid="stHeader"]::before {
    display: none !important;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #fdf4ff, #e0f2fe);
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Center card */
.block-container {
    max-width: 900px !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

/* Glass card - FIXED */
.glass-card {
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    background: rgba(255, 255, 255, 0.85);
    border-radius: 28px;
    box-shadow:
        0 24px 60px rgba(15, 23, 42, 0.16),
        0 0 0 1px rgba(148, 163, 184, 0.2);
    padding: 32px 36px 32px 36px;
    margin: 20px auto;
    width: 100%;
    box-sizing: border-box;
}

/* Left title area */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 12px;
    background: rgba(56, 189, 248, 0.15);
    color: #0369a1;
    font-weight: 600;
    margin-bottom: 12px;
}

.badge-dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: #22c55e;
    box-shadow: 0 0 0 6px rgba(34, 197, 94, 0.25);
}

.app-title {
    font-size: 32px;
    line-height: 1.1;
    color: #0f172a;
    margin-top: 0;
    margin-bottom: 12px;
    font-weight: 700;
}

.app-title span {
    color: #e11d48;
    background: linear-gradient(135deg, #e11d48, #f97316);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.subtitle {
    font-size: 15px;
    color: #64748b;
    line-height: 1.6;
    margin-bottom: 20px;
}

.pills-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 20px;
}

.pill {
    padding: 8px 16px;
    border-radius: 999px;
    font-size: 13px;
    background: rgba(15, 23, 42, 0.05);
    color: #4b5563;
    border: 1px solid rgba(15, 23, 42, 0.08);
}

/* Right side header */
.app-icon {
    width: 44px;
    height: 44px;
    border-radius: 20px;
    background: radial-gradient(circle at 30% 0, #f97316, #ea580c);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 20px;
    box-shadow: 0 10px 20px rgba(248, 113, 113, 0.45);
    margin-right: 12px;
}

.form-title {
    font-size: 18px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 4px;
}

.form-subtitle {
    font-size: 12px;
    color: #94a3b8;
    margin-bottom: 20px;
}

.status-chip {
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 12px;
    background: rgba(22, 163, 74, 0.12);
    color: #15803d;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    border: 1px solid rgba(22, 163, 74, 0.2);
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: #22c55e;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

/* Form inputs */
.stSelectbox, .stNumberInput {
    margin-bottom: 20px !important;
}

.stSelectbox > div > div {
    border-radius: 14px !important;
    border: 1.5px solid #e2e8f0 !important;
}

.stNumberInput > div > div {
    border-radius: 14px !important;
    border: 1.5px solid #e2e8f0 !important;
}

.stSelectbox label, .stNumberInput label {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #475569 !important;
    margin-bottom: 6px !important;
}

/* Note text */
.note-text {
    font-size: 12px;
    color: #94a3b8;
    text-align: center;
    margin-top: 24px;
    padding-top: 16px;
    border-top: 1px solid #f1f5f9;
}

/* Predict button */
.stButton > button {
    border-radius: 999px;
    background: linear-gradient(135deg, #ec4899, #f97316);
    color: white;
    font-weight: 600;
    font-size: 14px;
    border: none;
    padding: 12px 32px;
    box-shadow: 0 12px 25px rgba(248, 113, 113, 0.4);
    transition: all 0.3s ease;
    width: 100%;
    margin-top: 8px;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 30px rgba(248, 113, 113, 0.5);
}

/* Result messages */
.stAlert {
    border-radius: 16px !important;
    margin-top: 20px !important;
    border: none !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .glass-card {
        padding: 24px;
    }
    .app-title {
        font-size: 28px;
    }
}
</style>
""", unsafe_allow_html=True)

# ========== LOAD MODEL (change path as per your file) ==========
# with open("anemia_model.pkl", "rb") as f:
#     model = pickle.load(f)

# ========== UI LAYOUT ==========

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

# 2 columns: left info, right form
left, right = st.columns([1.2, 1])

with left:
    st.markdown(
        """
        <div class="badge">
            <span class="badge-dot"></span>
            Smart Health Insight
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="app-title">
            AnemiaSense<br>
            <span>Early Anemia</span> Prediction System
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p class="subtitle">
            Enter your basic blood report values and get an instant
            ML-based insight about possible anemia risk.
            <br><b>For project / learning use only.</b>
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="pills-row">
            <div class="pill">⚡ Fast prediction</div>
            <div class="pill">🩸 Uses key CBC parameters</div>
            <div class="pill">🔐 Data stays on device</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    # header of small card
    st.markdown(
        """
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <div class="app-icon">AS</div>
            <div style="flex: 1;">
                <div class="form-title">Check Your Anemia Risk</div>
                <div class="form-subtitle">Fill all fields before predicting</div>
            </div>
            <div class="status-chip">
                <span class="status-dot"></span>
                Model Ready
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------- FORM INPUTS ----------
    with st.form("anemia_form"):
        c1, c2 = st.columns(2)

        with c1:
            gender = st.selectbox("Gender", ["0 - Male", "1 - Female"])
            hb = st.number_input("Hemoglobin (g/dL)", min_value=0.0, max_value=25.0, value=13.0, step=0.1, format="%.1f")
            pcv = st.number_input("PCV (%)", min_value=0.0, max_value=80.0, value=40.0, step=0.5, format="%.1f")

        with c2:
            mcv = st.number_input("MCV (fL)", min_value=40.0, max_value=140.0, value=88.0, step=0.5, format="%.1f")
            mchc = st.number_input("MCHC (g/dL)", min_value=20.0, max_value=40.0, value=32.0, step=0.1, format="%.1f")

        st.markdown(
            '<p class="note-text">⚠️ This app is a demo and does not replace professional medical advice.</p>',
            unsafe_allow_html=True,
        )

        submitted = st.form_submit_button("Predict Now →")

    # --------- PREDICTION LOGIC ----------
    if submitted:
        gender_value = 0 if gender.startswith("0") else 1
        features = np.array([[gender_value, hb, pcv, mcv, mchc]])

        try:
            # Uncomment when you have the model file
            # prediction = model.predict(features)[0]
            
            # Dummy logic for demo
            score = (hb * 0.4) + (mcv * 0.1) + (mchc * 0.2)
            prediction = 1 if score < 25 else 0

            st.markdown("---")
            if prediction == 1:
                st.error("""
                🔴 **High chance of Anemia Detected**
                
                **Model Output:** 1 (Positive)
                
                **Recommendation:** Please consult a healthcare professional for proper diagnosis and treatment.
                """)
            else:
                st.success("""
                🟢 **Low chance of Anemia**
                
                **Model Output:** 0 (Negative)
                
                **Note:** Values appear normal according to this model. Regular checkups are still recommended.
                """)
                
        except NameError:
            st.warning(
                """
                ⚠️ **Model Not Loaded**
                
                Please load your trained model in the code (section `LOAD MODEL`) for accurate predictions.
                
                Currently showing demo results based on simple heuristics.
                """
            )

st.markdown("</div>", unsafe_allow_html=True)
