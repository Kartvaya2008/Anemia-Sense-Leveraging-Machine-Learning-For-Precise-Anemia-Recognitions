import numpy as np
import pickle
import streamlit as st
import os
import time

st.set_page_config(
    page_title="GlucoSense AI | Diabetes Risk Assessment",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:      #050d1a;
    --card:    rgba(255,255,255,0.035);
    --border:  rgba(255,255,255,0.08);
    --teal:    #38bdf8;
    --cyan:    #22d3ee;
    --green:   #34d399;
    --rose:    #fb7185;
    --t1:      #f0f6ff;
    --t2:      #94a3b8;
    --t3:      #4e6280;
    --r-lg:    20px;
    --r-md:    14px;
    --r-sm:    10px;
}

html,body,[data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--t1) !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stAppViewContainer"] > .main { background: var(--bg) !important; }
[data-testid="stHeader"] {
    background: rgba(5,13,26,0.85) !important;
    backdrop-filter: blur(20px) !important;
    border-bottom: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#060f1e 0%,#0a1628 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--t2) !important; font-family:'DM Sans',sans-serif !important; }

.stNumberInput [data-baseweb="input"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    transition: border-color .25s, box-shadow .25s !important;
}
.stNumberInput [data-baseweb="input"]:focus-within {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,.15) !important;
}
.stNumberInput input { color: var(--t1) !important; background: transparent !important; }
.stNumberInput label,.stSlider label {
    color: var(--t2) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

.stButton > button {
    background: linear-gradient(135deg,#0ea5e9 0%,#6366f1 100%) !important;
    color: #fff !important;
    font-family: 'Syne',sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: var(--r-md) !important;
    padding: 14px 32px !important;
    width: 100% !important;
    transition: all .3s cubic-bezier(.34,1.56,.64,1) !important;
    box-shadow: 0 8px 32px rgba(14,165,233,.35) !important;
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 16px 48px rgba(14,165,233,.55) !important;
    filter: brightness(1.1) !important;
}
.stButton > button:active { transform: translateY(0) scale(.98) !important; }

.stProgress > div > div > div > div {
    background: linear-gradient(90deg,var(--teal),var(--cyan)) !important;
    border-radius: 99px !important;
}
.stProgress > div > div > div {
    background: rgba(255,255,255,.06) !important;
    border-radius: 99px !important;
}

hr { border-color: var(--border) !important; margin: 2rem 0 !important; }
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:99px}

@keyframes fadeUp { from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)} }
@keyframes pulseRing {
    0%,100%{box-shadow:0 0 0 3px rgba(14,165,233,.25),0 0 32px rgba(14,165,233,.35)}
    50%{box-shadow:0 0 0 10px rgba(14,165,233,.08),0 0 48px rgba(14,165,233,.5)}
}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
@keyframes resultIn {
    from{opacity:0;transform:translateY(24px)}
    to{opacity:1;transform:translateY(0)}
}

.gs-header{display:flex;align-items:center;gap:20px;padding:0 0 2rem 0;animation:fadeUp .5s .05s both}
.gs-logo{width:68px;height:68px;border-radius:50%;background:linear-gradient(135deg,#0ea5e9,#6366f1);display:flex;align-items:center;justify-content:center;font-size:30px;flex-shrink:0;animation:pulseRing 3s ease-in-out infinite}
.gs-h1{font-family:'Syne',sans-serif;font-size:34px;font-weight:800;letter-spacing:-.02em;margin:0 0 4px;line-height:1.1;background:linear-gradient(90deg,#f0f6ff,#38bdf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.gs-sub{font-size:15px;color:var(--t2);margin:0}
.gs-badge{display:inline-flex;align-items:center;gap:6px;padding:4px 12px;border-radius:99px;font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;margin-top:10px;background:rgba(52,211,153,.12);color:var(--green);border:1px solid rgba(52,211,153,.25)}
.gs-badge::before{content:'';width:7px;height:7px;background:var(--green);border-radius:50%;animation:blink 1.4s ease-in-out infinite}

.gs-metric{background:var(--card);border:1px solid var(--border);border-radius:var(--r-md);padding:20px;text-align:center;transition:all .3s ease;animation:fadeUp .5s .2s both}
.gs-metric:hover{background:rgba(255,255,255,.06);border-color:rgba(56,189,248,.25);transform:translateY(-3px);box-shadow:0 12px 32px rgba(0,0,0,.35)}
.gs-m-ico{font-size:26px;margin-bottom:8px}
.gs-m-lbl{font-size:11px;color:var(--t3);letter-spacing:.08em;text-transform:uppercase;font-weight:600}
.gs-m-val{font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:var(--t1);margin:4px 0 2px}

.gs-card{background:var(--card);border:1px solid var(--border);border-radius:var(--r-lg);padding:28px;box-shadow:0 24px 60px rgba(0,0,0,.5),0 0 0 1px rgba(255,255,255,.06);backdrop-filter:blur(12px);transition:border-color .3s,box-shadow .3s;margin-bottom:16px;animation:fadeUp .5s .3s both}
.gs-card:hover{border-color:rgba(56,189,248,.2);box-shadow:0 24px 60px rgba(0,0,0,.5),0 0 0 1px rgba(255,255,255,.06),0 0 40px rgba(56,189,248,.12)}
.gs-card-title{font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:var(--teal);letter-spacing:.12em;text-transform:uppercase;margin-bottom:20px;display:flex;align-items:center;gap:8px}
.gs-card-title::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,var(--border),transparent)}

.gs-grp{font-family:'Syne',sans-serif;font-size:11px;font-weight:700;color:var(--t3);letter-spacing:.1em;text-transform:uppercase;padding:6px 0 12px;border-bottom:1px solid var(--border);margin-bottom:16px;display:flex;align-items:center;gap:8px}
.gs-tip{background:rgba(56,189,248,.06);border:1px solid rgba(56,189,248,.15);border-left:3px solid var(--teal);border-radius:var(--r-sm);padding:12px 16px;font-size:13px;color:var(--t2);line-height:1.6;margin-top:16px}
.gs-sep{height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:28px 0}

.gs-result{border-radius:var(--r-lg);padding:36px;text-align:center;animation:resultIn .6s cubic-bezier(.16,1,.3,1) both}
.gs-result-bad{background:linear-gradient(135deg,rgba(251,113,133,.12),rgba(244,63,94,.06));border:1px solid rgba(251,113,133,.3);box-shadow:0 0 60px rgba(251,113,133,.1),inset 0 1px 0 rgba(255,255,255,.05)}
.gs-result-good{background:linear-gradient(135deg,rgba(52,211,153,.12),rgba(16,185,129,.06));border:1px solid rgba(52,211,153,.3);box-shadow:0 0 60px rgba(52,211,153,.1),inset 0 1px 0 rgba(255,255,255,.05)}
.gs-r-ico{font-size:56px;margin-bottom:14px}
.gs-r-title{font-family:'Syne',sans-serif;font-size:30px;font-weight:800;letter-spacing:-.02em;margin-bottom:8px}
.gs-r-bad{color:var(--rose)}
.gs-r-good{color:var(--green)}
.gs-r-sub{font-size:15px;color:var(--t2);max-width:420px;margin:0 auto;line-height:1.7}
.gs-conf-row{display:flex;justify-content:space-between;font-size:12px;color:var(--t2);font-weight:600;letter-spacing:.06em;margin-bottom:8px;text-transform:uppercase}
.gs-conf-pct{font-family:'Syne',sans-serif;font-size:13px;font-weight:800;color:var(--teal)}

.gs-sum-item{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:14px;text-align:center;margin-bottom:12px;transition:all .25s ease}
.gs-sum-item:hover{background:rgba(255,255,255,.055);border-color:rgba(56,189,248,.2);transform:translateY(-2px)}
.gs-sum-ico{font-size:20px;margin-bottom:4px}
.gs-sum-lbl{font-size:10px;color:#4e6280;text-transform:uppercase;letter-spacing:.08em;font-weight:600}
.gs-sum-val{font-family:'Syne',sans-serif;font-size:16px;font-weight:700;color:#f0f6ff;margin-top:4px}

.gs-footer{text-align:center;padding:32px 0 16px;border-top:1px solid var(--border);margin-top:40px}
.gs-footer-brand{font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:var(--t2)}
.gs-footer-hl{background:linear-gradient(90deg,var(--teal),var(--cyan));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.gs-footer-sub{font-size:12px;color:var(--t3);margin-top:6px}

.sb-logo{display:flex;align-items:center;gap:10px;padding-bottom:20px;border-bottom:1px solid rgba(255,255,255,.06);margin-bottom:24px}
.sb-name{font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:#f0f6ff !important}
.sb-sec{margin-bottom:28px}
.sb-h{font-size:10px !important;letter-spacing:.14em !important;text-transform:uppercase !important;color:rgba(148,163,184,.4) !important;font-weight:700 !important;margin-bottom:10px !important;display:block}
.sb-item{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:10px;margin-bottom:3px;font-size:14px !important;color:#94a3b8 !important;cursor:default;transition:background .2s}
.sb-item:hover{background:rgba(255,255,255,.05)}
.sb-stat{display:flex;justify-content:space-between;align-items:center;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.05);font-size:13px !important;color:#64748b !important}
.sb-sv{font-family:'Syne',sans-serif;font-size:14px;font-weight:700;color:#38bdf8 !important}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------- LOAD MODEL ----------
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
if not os.path.exists(model_path):
    st.error("❌ Model file not found: model.pkl — ensure it is committed to your repository root.")
    st.stop()
with open(model_path, "rb") as f:
    model = pickle.load(f)

# ---------- PREDICTION ----------
def predict_diabetes(data):
    arr = np.asarray(data, dtype=float).reshape(1, -1)
    pred = model.predict(arr)[0]
    try:
        confidence = max(model.predict_proba(arr)[0]) * 100
    except Exception:
        confidence = None
    label = "Diabetic" if pred == 1 else "Not Diabetic"
    return label, confidence

# ══════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class='sb-logo'>
        <span style='font-size:28px'>🩺</span>
        <span class='sb-name'>GlucoSense</span>
    </div>
    <div class='sb-sec'>
        <span class='sb-h'>Navigation</span>
        <div class='sb-item'>📊 &nbsp; Risk Assessment</div>
        <div class='sb-item'>📈 &nbsp; Analytics</div>
        <div class='sb-item'>📋 &nbsp; Reports</div>
        <div class='sb-item'>⚙️ &nbsp; Settings</div>
    </div>
    <div class='sb-sec'>
        <span class='sb-h'>Model Stats</span>
        <div class='sb-stat'><span>Algorithm</span><span class='sb-sv'>SVM / RF</span></div>
        <div class='sb-stat'><span>Dataset</span><span class='sb-sv'>PIMA</span></div>
        <div class='sb-stat'><span>Features</span><span class='sb-sv'>8</span></div>
        <div class='sb-stat'><span>Output</span><span class='sb-sv'>Binary</span></div>
        <div class='sb-stat'><span>Status</span><span class='sb-sv'>● Live</span></div>
    </div>
    <div class='sb-sec'>
        <span class='sb-h'>About</span>
        <p style='font-size:13px;line-height:1.7;color:#475569;'>
            GlucoSense uses a machine learning model trained on the PIMA Indian Diabetes Dataset to estimate Type 2 diabetes risk from 8 clinical measurements.
        </p>
        <p style='font-size:11px;color:#334155;margin-top:10px;line-height:1.6;'>
            ⚠️ Educational use only. Not a substitute for professional medical diagnosis.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════
st.markdown("""
<div class='gs-header'>
    <div class='gs-logo'>🩺</div>
    <div>
        <div class='gs-h1'>GlucoSense AI</div>
        <p class='gs-sub'>Advanced Diabetes Risk Assessment Platform</p>
        <div class='gs-badge'>Model Active</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
#  METRIC STRIP
# ══════════════════════════════════════════
m1, m2, m3, m4 = st.columns(4)
metrics = [
    ("🧬", "Input Features", "8"),
    ("🎯", "Output Classes", "2"),
    ("🗄️", "Training Data", "PIMA"),
    ("⚡", "Inference", "<1ms"),
]
for col, (ico, lbl, val) in zip([m1, m2, m3, m4], metrics):
    with col:
        st.markdown(f"""
        <div class='gs-metric'>
            <div class='gs-m-ico'>{ico}</div>
            <div class='gs-m-lbl'>{lbl}</div>
            <div class='gs-m-val'>{val}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div class='gs-sep'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
#  INPUT FORM
# ══════════════════════════════════════════
left, right = st.columns(2, gap="large")

with left:
    st.markdown("""
    <div class='gs-card'>
        <div class='gs-card-title'>🩸 Physiological Parameters</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='gs-grp'>👶 &nbsp; Reproductive History</div>", unsafe_allow_html=True)
    pregnancies = st.number_input("Number of Pregnancies", min_value=0, max_value=20, value=0, step=1,
                                  help="Total number of pregnancies")

    st.markdown("<div class='gs-grp'>🩸 &nbsp; Blood Markers</div>", unsafe_allow_html=True)
    glucose = st.number_input("Plasma Glucose (mg/dL)", min_value=0, max_value=300, value=100,
                              help="2-hour plasma glucose in OGTT. Normal: 70–140 mg/dL")
    blood_pressure = st.number_input("Diastolic Blood Pressure (mmHg)", min_value=0, max_value=200, value=70,
                                     help="Resting diastolic pressure. Normal: 60–80 mmHg")
    insulin = st.number_input("2-Hour Serum Insulin (μU/mL)", min_value=0, max_value=900, value=80,
                              help="Serum insulin level. Normal: 16–166 μU/mL")

    st.markdown("""<div class='gs-tip'>
        💡 <strong>Tip:</strong> Glucose and insulin values should reflect fasting or post-load readings from recent lab work.
    </div>""", unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class='gs-card'>
        <div class='gs-card-title'>📐 Anthropometric & Genetic Markers</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='gs-grp'>📏 &nbsp; Body Composition</div>", unsafe_allow_html=True)
    skin_thickness = st.number_input("Triceps Skin Fold Thickness (mm)", min_value=0, max_value=100, value=20,
                                     help="Triceps skin fold thickness. Normal: 10–50 mm")
    bmi = st.number_input("Body Mass Index (kg/m²)", min_value=0.0, max_value=70.0, value=25.0, step=0.1,
                          help="Weight / height². Normal: 18.5–24.9")

    st.markdown("<div class='gs-grp'>🧬 &nbsp; Genetic & Demographic</div>", unsafe_allow_html=True)
    pedigree = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.47, step=0.01,
                               help="Hereditary diabetes likelihood (0.08–2.42). Higher = stronger family history")
    age = st.number_input("Age (years)", min_value=1, max_value=120, value=30,
                          help="Patient age in years")

    st.markdown("""<div class='gs-tip'>
        💡 <strong>Tip:</strong> The Diabetes Pedigree Function encodes hereditary influence — higher values indicate stronger family risk.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
#  PREDICT BUTTON
# ══════════════════════════════════════════
st.markdown("<div class='gs-sep'></div>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    clicked = st.button("🔬  Run Diabetes Risk Assessment", use_container_width=True)

# ══════════════════════════════════════════
#  RESULT
# ══════════════════════════════════════════
if clicked:
    data = [pregnancies, glucose, blood_pressure,
            skin_thickness, insulin, bmi, pedigree, age]

    with st.spinner("Analyzing clinical parameters..."):
        time.sleep(0.9)

    result, confidence = predict_diabetes(data)
    is_bad = result == "Diabetic"

    panel_cls  = "gs-result-bad" if is_bad else "gs-result-good"
    title_cls  = "gs-r-bad"      if is_bad else "gs-r-good"
    icon       = "⚠️"            if is_bad else "✅"
    sub_text   = (
        "The model indicates <strong>elevated risk</strong> for Type 2 Diabetes. "
        "Please consult a licensed physician for clinical confirmation and personalised guidance."
        if is_bad else
        "The model indicates <strong>low risk</strong> for Type 2 Diabetes based on the provided values. "
        "Maintain healthy lifestyle habits and schedule regular checkups."
    )
    conf_val   = (confidence / 100.0) if confidence else 0.0
    conf_label = f"{confidence:.1f}%" if confidence else "N/A"
    certainty  = "High" if conf_val > 0.8 else "Moderate" if conf_val > 0.6 else "Low"

    st.markdown("<div class='gs-sep'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='gs-result {panel_cls}'>
        <div class='gs-r-ico'>{icon}</div>
        <div class='gs-r-title {title_cls}'>{result}</div>
        <div class='gs-r-sub'>{sub_text}</div>
    </div>""", unsafe_allow_html=True)

    # Confidence bar
    st.markdown("<br>", unsafe_allow_html=True)
    _, cbar, _ = st.columns([1, 2, 1])
    with cbar:
        st.markdown(f"""
        <div class='gs-conf-row'>
            <span>Model Confidence</span>
            <span class='gs-conf-pct'>{conf_label}</span>
        </div>""", unsafe_allow_html=True)
        st.progress(conf_val)
        st.markdown(f"""
        <div style='text-align:center;font-size:12px;color:var(--t3);margin-top:6px;'>
            PIMA dataset training · {certainty} certainty zone
        </div>""", unsafe_allow_html=True)

    # Input summary grid
    st.markdown("<div class='gs-sep'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:Syne,sans-serif;font-size:11px;font-weight:700;
                color:#38bdf8;letter-spacing:.1em;text-transform:uppercase;margin-bottom:16px;'>
        📋 Input Summary
    </div>""", unsafe_allow_html=True)

    items = [
        ("👶","Pregnancies", str(pregnancies)),
        ("🩸","Glucose",f"{glucose} mg/dL"),
        ("💓","Blood Pressure",f"{blood_pressure} mmHg"),
        ("📏","Skin Thickness",f"{skin_thickness} mm"),
        ("💉","Insulin",f"{insulin} μU/mL"),
        ("⚖️","BMI",f"{bmi:.1f}"),
        ("🧬","Pedigree Fn.",f"{pedigree:.2f}"),
        ("🗓️","Age",f"{age} yrs"),
    ]
    cols = st.columns(4)
    for i, (ico, lbl, val) in enumerate(items):
        with cols[i % 4]:
            st.markdown(f"""
            <div class='gs-sum-item'>
                <div class='gs-sum-ico'>{ico}</div>
                <div class='gs-sum-lbl'>{lbl}</div>
                <div class='gs-sum-val'>{val}</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════
st.markdown("""
<div class='gs-footer'>
    <div class='gs-footer-brand'>
        🩺 &nbsp; <span class='gs-footer-hl'>GlucoSense AI</span>
        &nbsp;·&nbsp; Diabetes Risk Assessment Platform
    </div>
    <div class='gs-footer-sub'>
        Developed by Kartvaya Raikwar &nbsp;·&nbsp; Machine Learning Project &nbsp;·&nbsp;
        For educational purposes only — not a clinical diagnostic tool.
    </div>
</div>
""", unsafe_allow_html=True)
