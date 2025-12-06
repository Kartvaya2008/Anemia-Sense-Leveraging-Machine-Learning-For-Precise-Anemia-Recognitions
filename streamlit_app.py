# app.py
import streamlit as st
import numpy as np
import pickle

# ========== BASIC PAGE SETTINGS ==========
st.set_page_config(
    page_title="AnemiaSense – Anemia Prediction",
    page_icon="🩸",
    layout="centered"
)

# ========== CUSTOM CSS FOR MODERN UI ==========
/* Remove Streamlit's default top big header box */
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
    col1, col2 = st.columns([2.2, 1])

    with col1:
        c1, c2 = st.columns([1, 3])
        with c1:
            st.markdown('<div class="app-icon">AS</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(
                """
                <div class="form-title">Check Your Anemia Risk</div>
                <div class="form-subtitle">Fill all fields before predicting</div>
                """,
                unsafe_allow_html=True,
            )
    with col2:
        st.markdown(
            """
            <div class="status-chip">
                <span class="status-dot"></span>
                Model Ready
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")  # small space

    # --------- FORM INPUTS ----------
    with st.form("anemia_form"):
        c1, c2 = st.columns(2)

        with c1:
            gender_label = "Gender (0 = Male, 1 = Female)"
            gender = st.selectbox(gender_label, ["0 - Male", "1 - Female"])
            hb = st.number_input("Hemoglobin (g/dL)", min_value=0.0, max_value=25.0, value=13.0, step=0.1)
            pcv = st.number_input("PCV (%)", min_value=0.0, max_value=80.0, value=40.0, step=0.5)

        with c2:
            mcv = st.number_input("MCV (fL)", min_value=40.0, max_value=140.0, value=88.0, step=0.5)
            mchc = st.number_input("MCHC (g/dL)", min_value=20.0, max_value=40.0, value=32.0, step=0.1)

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
            # prediction = model.predict(features)[0]

            # Dummy logic
            score = (hb * 0.4) + (mcv * 0.1) + (mchc * 0.2)
            prediction = 1 if score < 25 else 0

            if prediction == 1:
                st.error("🔴 **High chance of Anemia (model output = 1)**\n\nPlease consult a doctor for proper tests.")
            else:
                st.success("🟢 **Low chance of Anemia (model output = 0)**\n\nValues look okay as per this model.")
        except NameError:
            st.warning(
                "Model file not loaded. Please load your trained model in the code "
                "(section `LOAD MODEL`) and then run again."
            )

st.markdown("</div>", unsafe_allow_html=True)

