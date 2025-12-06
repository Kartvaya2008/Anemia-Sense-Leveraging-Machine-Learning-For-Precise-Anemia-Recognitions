import streamlit as st
import numpy as np
import pickle

# ------------------- Page config -------------------
st.set_page_config(
    page_title="AnemiaSense – Anemia Prediction",
    page_icon="🩸",
    layout="wide"
)

# ------------------- Custom CSS --------------------
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f7;
    }
    .main {
        padding: 0rem 4rem 4rem 4rem;
    }
    .hero-wrapper {
        padding: 2.5rem 3rem 1.5rem 3rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #f5f5f7 0%, #ffffff 40%, #f3e8ff 100%);
        border: 1px solid #ececec;
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.09);
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 700;
        line-height: 1.15;
        color: #111827;
        margin-bottom: 0.4rem;
    }
    .hero-title span {
        background: linear-gradient(120deg, #a855f7, #6366f1);
        -webkit-background-clip: text;
        color: transparent;
    }
    .hero-subtitle {
        font-size: 0.98rem;
        color: #6b7280;
        max-width: 480px;
        margin-bottom: 1.8rem;
    }
    .pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.25rem 0.8rem;
        border-radius: 999px;
        background-color: rgba(129, 140, 248, 0.08);
        color: #4f46e5;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: .03em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }
    .pill span.icon {
        font-size: 0.9rem;
    }
    .card {
        padding: 1.1rem 1.1rem 1rem 1.1rem;
        border-radius: 18px;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.04);
        height: 100%;
    }
    .card-title {
        font-size: 0.92rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 0.25rem;
    }
    .card-body {
        font-size: 0.8rem;
        color: #6b7280;
    }
    .input-wrapper {
        margin-top: 2.3rem;
        padding: 1.8rem 2.2rem 2rem 2.2rem;
        border-radius: 22px;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        box-shadow: 0 14px 32px rgba(15, 23, 42, 0.08);
    }
    .input-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 0.2rem;
    }
    .input-subtitle {
        font-size: 0.85rem;
        color: #6b7280;
        margin-bottom: 1.2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 999px;
        padding: 0.7rem 1rem;
        font-weight: 600;
        border: none;
        background: linear-gradient(120deg, #6366f1, #a855f7);
        color: white;
        box-shadow: 0 10px 24px rgba(88, 80, 236, 0.45);
    }
    .stButton>button:hover {
        filter: brightness(1.05);
        box-shadow: 0 14px 30px rgba(88, 80, 236, 0.6);
    }
    .result-box {
        padding: 1.2rem 1.4rem;
        border-radius: 18px;
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        margin-top: 0.8rem;
    }
    .result-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #6b7280;
        margin-bottom: 0.25rem;
    }
    .result-text-ok {
        font-size: 0.95rem;
        font-weight: 600;
        color: #059669;
    }
    .result-text-bad {
        font-size: 0.95rem;
        font-weight: 600;
        color: #b91c1c;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------- Load model --------------------
try:
    model = pickle.load(open("model.pkl", "rb"))
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.error("❌ Could not load `model.pkl`. Please check that the file exists in the repo.")
    st.exception(e)

# ------------------- HERO SECTION ------------------
st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)

col_hero_left, col_hero_right = st.columns([2.4, 2])

with col_hero_left:
    st.markdown(
        """
        <div class="pill"><span class="icon">🩸</span>AnemiaSense • ML Powered</div>
        <div class="hero-title">
            Hi there, <span>Kartvaya</span><br/>
            What would you like to check today?
        </div>
        <div class="hero-subtitle">
            Enter a few blood-test values and let AnemiaSense estimate whether anemia
            is likely or not – powered by your trained machine learning model.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_hero_right:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Instant Risk Check</div>
                <div class="card-body">
                    Get a quick anemia risk prediction from your CBC-style values.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Follow-up Support</div>
                <div class="card-body">
                    Re-check values after treatment and compare predicted outcomes.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">ML Transparency</div>
                <div class="card-body">
                    Built on classical ML models you trained & evaluated.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

# ------------------- INPUT + RESULT SECTION --------
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)

left, right = st.columns([1.6, 1.2])

with left:
    st.markdown(
        """
        <div class="input-title">Enter your blood parameters</div>
        <div class="input-subtitle">
            These are example features from your project: gender, hemoglobin,
            PCV, MCV, and MCHC. Use values similar to a normal CBC report.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("anemia_form"):
        c1, c2 = st.columns(2)
        with c1:
            gender = st.selectbox(
                "Gender",
                options=[0, 1],
                format_func=lambda x: "Male (0)" if x == 0 else "Female (1)"
            )
            hb = st.number_input("Hemoglobin (g/dL)", min_value=0.0, max_value=25.0, value=11.6, step=0.1)
            pcv = st.number_input("PCV (%)", min_value=0.0, max_value=80.0, value=22.3, step=0.1)
        with c2:
            mcv = st.number_input("MCV (fL)", min_value=0.0, max_value=130.0, value=30.9, step=0.1)
            mchc = st.number_input("MCHC (g/dL)", min_value=0.0, max_value=45.0, value=74.5, step=0.1)

        submitted = st.form_submit_button("Run Anemia Prediction")

with right:
    st.markdown(
        """
        <div class="input-title">Prediction Panel</div>
        <div class="input-subtitle">
            Once you submit the form, the model's prediction and a short
            interpretation will appear here.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not model_loaded:
        st.info("Waiting for a valid model file (`model.pkl`).")
    else:
        if "last_pred" not in st.session_state:
            st.session_state.last_pred = None

        if 'submitted' in locals() and submitted and model_loaded:
            features = np.array([[gender, hb, pcv, mcv, mchc]])
            pred = model.predict(features)[0]
            st.session_state.last_pred = int(pred)

        if st.session_state.last_pred is not None:
            if st.session_state.last_pred == 0:
                st.markdown(
                    """
                    <div class="result-box">
                        <div class="result-label">Prediction</div>
                        <div class="result-text-ok">
                            ✅ No anemia detected based on the provided values.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <div class="result-box">
                        <div class="result-label">Prediction</div>
                        <div class="result-text-bad">
                            ⚠️ Anemia likely – please consult a healthcare professional.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                """
                <div class="result-box">
                    <div class="result-label">Prediction</div>
                    <div class="result-text-ok">
                        Fill the form on the left and click “Run Anemia Prediction”.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("</div>", unsafe_allow_html=True)
