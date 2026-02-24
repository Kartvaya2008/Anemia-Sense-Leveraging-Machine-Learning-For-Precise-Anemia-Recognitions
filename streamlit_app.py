import numpy as np
import pickle
import streamlit as st
import os
import time

st.set_page_config(
    page_title="AnemiaCheck · Clinical Screening",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&family=DM+Mono:wght@400;500&display=swap');

/* ══ TEAL CLINICAL COLOR SYSTEM ════════════════════════════ */
:root {
    /* Brand teal scale */
    --teal-900:      #063d4f;
    --teal-800:      #09637E;
    --teal-700:      #088395;
    --teal-600:      #0a9aaf;
    --teal-400:      #7AB2B2;
    --teal-200:      #b8d9d9;
    --teal-100:      #d4ecec;
    --teal-50:       #EBF4F6;

    /* Backgrounds */
    --bg-0:          #04151a;
    --bg-1:          #071e26;
    --bg-2:          #0b2a35;
    --bg-3:          #0f3240;
    --bg-4:          #143c4b;

    /* Card surfaces */
    --card-white:    rgba(255,255,255,0.97);
    --card-glass:    rgba(9,99,126,0.18);
    --card-glass-hv: rgba(9,99,126,0.28);
    --card-frost:    rgba(235,244,246,0.06);
    --card-frost-hv: rgba(235,244,246,0.10);

    /* Borders */
    --border-dim:    rgba(122,178,178,0.12);
    --border-mid:    rgba(122,178,178,0.22);
    --border-up:     rgba(122,178,178,0.40);
    --border-strong: rgba(8,131,149,0.65);

    /* Typography */
    --t-white:       #eef6f8;
    --t-silver:      #a8c8cc;
    --t-steel:       #6b9ea4;
    --t-iron:        #3d6870;
    --t-black:       #04151a;
    --t-charcoal:    #0b2a35;

    /* Semantic */
    --ok-text:       #5ecfb0;
    --ok-bg:         rgba(94,207,176,0.10);
    --ok-border:     rgba(94,207,176,0.28);
    --risk-text:     #f4948a;
    --risk-bg:       rgba(244,148,138,0.10);
    --risk-border:   rgba(244,148,138,0.28);

    /* Radii */
    --r-xl:  20px;
    --r-lg:  14px;
    --r-md:  10px;
    --r-sm:  7px;

    /* Shadows */
    --sh-card:  0 1px 3px rgba(0,0,0,0.5), 0 8px 28px rgba(0,0,0,0.45);
    --sh-white: 0 2px 16px rgba(9,99,126,0.18), 0 1px 0 rgba(255,255,255,0.12) inset;
    --sh-hover: 0 4px 8px rgba(0,0,0,0.4), 0 20px 48px rgba(9,99,126,0.25);
    --sh-glow:  0 0 32px rgba(8,131,149,0.22);
}

/* ══ GLOBAL ══════════════════════════════════════════════════ */
html, body, [class*="css"],
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    background: var(--bg-0) !important;
    color: var(--t-white) !important;
    font-family: 'Instrument Sans', -apple-system, sans-serif !important;
}
.stApp {
    background:
        radial-gradient(ellipse 70% 45% at 15% -5%,  rgba(9,99,126,0.22) 0%, transparent 60%),
        radial-gradient(ellipse 55% 35% at 90% 105%, rgba(8,131,149,0.14) 0%, transparent 60%),
        var(--bg-0) !important;
    min-height: 100vh;
}
[data-testid="stHeader"] {
    background: rgba(4,21,26,0.90) !important;
    backdrop-filter: blur(18px) !important;
    border-bottom: 1px solid var(--border-dim) !important;
}
.block-container { padding-top: 2.2rem !important; max-width: 1280px; }
#MainMenu, footer { visibility: hidden; }

/* ══ SIDEBAR ════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--bg-1) !important;
    border-right: 1px solid var(--border-dim) !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 2rem; }
[data-testid="stSidebar"] * { color: var(--t-steel) !important; }

/* ══ INPUTS ══════════════════════════════════════════════════ */
[data-testid="stNumberInput"] [data-baseweb="input"] {
    background: var(--bg-2) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: var(--r-md) !important;
    transition: border-color .2s, box-shadow .2s !important;
}
[data-testid="stNumberInput"] [data-baseweb="input"]:focus-within {
    border-color: var(--teal-700) !important;
    box-shadow: 0 0 0 3px rgba(8,131,149,0.18) !important;
}
[data-testid="stNumberInput"] input {
    color: var(--t-white) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 14px !important;
    background: transparent !important;
}
[data-testid="stNumberInput"] label {
    color: var(--t-steel) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: .04em !important;
}
[data-baseweb="input"] svg { fill: var(--t-iron) !important; }

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: var(--bg-2) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: var(--r-md) !important;
    color: var(--t-white) !important;
}

/* ══ BUTTON ══════════════════════════════════════════════════ */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--teal-800) 0%, var(--teal-700) 100%) !important;
    color: #ffffff !important;
    font-family: 'Instrument Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: .10em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: var(--r-md) !important;
    padding: 0.9rem 2rem !important;
    transition: all .25s cubic-bezier(.34,1.56,.64,1) !important;
    box-shadow: 0 2px 8px rgba(9,99,126,0.45), 0 1px 0 rgba(255,255,255,0.08) inset !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--teal-700) 0%, var(--teal-600) 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(8,131,149,0.55), 0 1px 0 rgba(255,255,255,0.10) inset !important;
    filter: brightness(1.06) !important;
}
.stButton > button:active { transform: scale(.97) translateY(0) !important; }

/* ══ PROGRESS ════════════════════════════════════════════════ */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--teal-700), var(--teal-400)) !important;
    border-radius: 99px !important;
}
.stProgress > div > div > div {
    background: rgba(122,178,178,0.12) !important;
    border-radius: 99px !important;
    height: 8px !important;
}

/* ══ SPINNER ══════════════════════════════════════════════════ */
.stSpinner > div { border-top-color: var(--teal-400) !important; }

/* ══ SCROLLBAR ════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-0); }
::-webkit-scrollbar-thumb { background: var(--bg-4); border-radius: 99px; }
hr { border-color: var(--border-dim) !important; }

/* ══ ANIMATIONS ══════════════════════════════════════════════ */
@keyframes fadeUp {
    from { opacity:0; transform:translateY(14px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes scaleIn {
    from { opacity:0; transform:scale(.93) translateY(8px); }
    to   { opacity:1; transform:scale(1)   translateY(0); }
}
@keyframes pulseDot {
    0%,100% { opacity:1; }
    50%      { opacity:.35; }
}

/* ══════════════════════════════════════════════════════════════
   COMPONENTS
══════════════════════════════════════════════════════════════ */

/* HERO ─────────────────────────────────────────────────────── */
.hero {
    background: var(--card-white);
    border-radius: var(--r-xl);
    padding: 2.4rem 2.8rem;
    margin-bottom: 1.8rem;
    box-shadow: var(--sh-white);
    animation: fadeUp .45s ease both;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content:'';
    position:absolute; top:0; right:0;
    width:340px; height:340px;
    background: radial-gradient(circle at 80% 20%, rgba(9,99,126,0.07) 0%, transparent 65%);
    pointer-events:none;
}
.hero-badge {
    display:inline-flex; align-items:center; gap:7px;
    background: var(--teal-800);
    color: #ffffff;
    border-radius: 99px;
    padding: 5px 16px;
    font-size: 10px; font-weight: 700;
    letter-spacing: .13em; text-transform: uppercase;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 10px rgba(9,99,126,0.35);
}
.hero-dot {
    width:6px; height:6px; border-radius:50%;
    background: var(--ok-text);
    animation: pulseDot 2s ease-in-out infinite;
}
.hero-title {
    font-family: 'Instrument Serif', serif;
    font-size: clamp(30px,4vw,48px);
    font-weight: 400;
    color: var(--t-black);
    line-height: 1.1;
    margin: 0 0 .65rem;
    letter-spacing: -.025em;
}
.hero-title em { font-style:italic; color: var(--teal-800); }
.hero-sub {
    font-size: 15px; color: #4a7a84;
    margin: 0; max-width: 500px; line-height: 1.68;
}

/* METRIC CARD ───────────────────────────────────────────────── */
.mc-wrap {
    background: var(--card-frost);
    border: 1px solid var(--border-dim);
    border-radius: var(--r-lg);
    padding: 1.2rem 1rem;
    text-align: center;
    transition: background .2s, box-shadow .2s, transform .22s, border-color .2s;
    animation: fadeUp .45s .1s ease both;
    cursor: default;
}
.mc-wrap:hover {
    background: var(--card-frost-hv);
    border-color: var(--border-mid);
    transform: translateY(-3px);
    box-shadow: var(--sh-hover);
}
.mc-icon { font-size: 22px; margin-bottom: 6px; opacity: .8; }
.mc-val {
    font-family: 'DM Mono', monospace;
    font-size: 19px; font-weight: 500;
    color: var(--teal-400); display: block;
}
.mc-lbl {
    font-size: 10px; font-weight: 700;
    letter-spacing: .12em; text-transform: uppercase;
    color: var(--t-iron); margin-top: 3px;
}

/* FORM CARD ─────────────────────────────────────────────────── */
.form-card {
    background: var(--card-frost);
    border: 1px solid var(--border-dim);
    border-radius: var(--r-xl);
    padding: 2rem 2rem 1.6rem;
    box-shadow: var(--sh-card);
    animation: fadeUp .45s .15s ease both;
    margin-bottom: 1.2rem;
    transition: border-color .25s, box-shadow .25s;
}
.form-card:hover {
    border-color: var(--border-mid);
    box-shadow: var(--sh-card), var(--sh-glow);
}
.section-head {
    font-size: 10px; font-weight: 700;
    letter-spacing: .18em; text-transform: uppercase;
    color: var(--t-iron);
    margin-bottom: 1.4rem;
    display: flex; align-items: center; gap: 10px;
}
.section-head::after {
    content:''; flex:1; height:1px;
    background: linear-gradient(90deg, var(--border-mid), transparent);
}
.field-lbl {
    font-size: 12px; font-weight: 600;
    color: var(--t-steel); letter-spacing: .04em;
    margin-bottom: 4px;
    display: flex; align-items: center; gap: 5px;
}

/* SUMMARY CARD ──────────────────────────────────────────────── */
.sum-card {
    background: var(--card-frost);
    border: 1px solid var(--border-dim);
    border-radius: var(--r-xl);
    padding: 1.8rem 1.8rem 1.4rem;
    animation: fadeUp .45s .2s ease both;
    margin-bottom: 1.2rem;
    transition: border-color .25s;
}
.sum-card:hover { border-color: var(--border-mid); }
.sum-row {
    display:flex; justify-content:space-between; align-items:center;
    padding: .44rem 0;
    border-bottom: 1px solid rgba(122,178,178,0.07);
}
.sum-row:last-child { border-bottom: none; }
.sum-key { font-size:13px; color: var(--t-steel); }
.sum-val { font-family:'DM Mono',monospace; font-size:13px; color: var(--t-white); }

/* AWAIT BOX ─────────────────────────────────────────────────── */
.await-box {
    background: var(--card-frost);
    border: 1px dashed var(--border-mid);
    border-radius: var(--r-xl);
    padding: 2.8rem 2rem;
    text-align: center;
    animation: fadeUp .45s .25s ease both;
}
.await-icon { font-size:42px; margin-bottom:.9rem; opacity:.4; }
.await-title { font-size:15px; font-weight:600; color:var(--t-steel); margin-bottom:.4rem; }
.await-sub   { font-size:13px; color:var(--t-iron); line-height:1.65; }
.await-cta   { color: var(--teal-400); font-weight:600; }

/* RESULT ────────────────────────────────────────────────────── */
.result-wrap {
    border-radius: var(--r-xl);
    padding: 2.2rem 2rem;
    text-align: center;
    animation: scaleIn .42s cubic-bezier(.34,1.56,.64,1) both;
    margin-bottom: 1rem;
}
.result-risk  { background: var(--risk-bg);  border: 1px solid var(--risk-border); }
.result-clear { background: var(--ok-bg);    border: 1px solid var(--ok-border); }
.result-ico   { font-size:48px; margin-bottom:.75rem; }
.result-lbl   {
    font-family: 'Instrument Serif', serif;
    font-size: 28px; font-weight: 400;
    letter-spacing: -.015em; margin-bottom: .4rem;
}
.result-risk  .result-lbl { color: var(--risk-text); }
.result-clear .result-lbl { color: var(--ok-text); }
.result-desc { font-size:14px; color:var(--t-steel); line-height:1.65; }

/* CONFIDENCE ────────────────────────────────────────────────── */
.conf-card {
    background: var(--card-frost);
    border: 1px solid var(--border-dim);
    border-radius: var(--r-lg);
    padding: 1.4rem 1.6rem;
    animation: fadeUp .35s ease both;
    margin-bottom: .9rem;
}
.conf-head {
    display:flex; justify-content:space-between; align-items:baseline;
    margin-bottom:.75rem;
}
.conf-title {
    font-size:10px; font-weight:700;
    letter-spacing:.16em; text-transform:uppercase;
    color: var(--t-iron);
}
.conf-pct {
    font-family:'DM Mono',monospace;
    font-size:22px; font-weight:500;
    color: var(--teal-400);
}
.conf-badge {
    display:inline-block; font-size:10px; font-weight:700;
    letter-spacing:.08em; text-transform:uppercase;
    border-radius:99px; padding:3px 12px; margin-top:.75rem;
}
.conf-high { color:var(--ok-text);   background:var(--ok-bg);   border:1px solid var(--ok-border); }
.conf-mid  { color:var(--teal-400);  background:rgba(122,178,178,.08); border:1px solid rgba(122,178,178,.22); }
.conf-low  { color:var(--risk-text); background:var(--risk-bg); border:1px solid var(--risk-border); }

/* DISCLAIMER ────────────────────────────────────────────────── */
.disclaimer {
    background: rgba(9,99,126,0.10);
    border: 1px solid var(--border-dim);
    border-left: 3px solid var(--teal-700);
    border-radius: 0 var(--r-md) var(--r-md) 0;
    padding: .85rem 1rem;
    font-size: 11px; color: var(--t-steel); line-height: 1.7;
}

/* SIDEBAR ───────────────────────────────────────────────────── */
.sb-logo {
    font-family: 'Instrument Serif', serif;
    font-size: 22px; font-weight: 400;
    color: var(--teal-400) !important;
    letter-spacing: -.01em; margin-bottom: .2rem;
}
.sb-tag {
    font-size:10px !important; font-weight:700 !important;
    letter-spacing:.14em !important; text-transform:uppercase !important;
    color: var(--t-iron) !important; margin-bottom: 1.6rem;
}
.sb-online {
    display:inline-flex; align-items:center; gap:6px;
    font-size:11px !important; font-weight:700 !important;
    letter-spacing:.08em !important; text-transform:uppercase !important;
    color: var(--ok-text) !important;
}
.sb-pulse {
    width:7px; height:7px; border-radius:50%;
    background: var(--ok-text);
    box-shadow: 0 0 6px var(--ok-text);
    display:inline-block;
    animation: pulseDot 2s ease-in-out infinite;
}
.sb-divider { height:1px; background:var(--border-dim); margin:1.4rem 0; }
.sb-section-h {
    font-size:9px !important; font-weight:700 !important;
    letter-spacing:.18em !important; text-transform:uppercase !important;
    color: var(--t-iron) !important;
    margin-bottom:.9rem !important; display:block;
}
.sb-item {
    display:flex; justify-content:space-between; align-items:center;
    padding:.5rem 0; border-bottom:1px solid var(--border-dim);
    font-size:13px !important;
}
.sb-item:last-child { border-bottom:none; }
.sb-item-k { color:var(--t-steel) !important; }
.sb-item-v {
    font-family:'DM Mono',monospace; font-size:11px !important;
    color: var(--teal-400) !important;
    background: rgba(9,99,126,0.20);
    border: 1px solid var(--border-mid);
    border-radius:5px; padding:2px 8px;
}
.sb-tip {
    background: rgba(9,99,126,0.10);
    border-left: 3px solid var(--teal-700);
    border-radius: 0 var(--r-sm) var(--r-sm) 0;
    padding: .9rem .95rem;
    font-size:12px !important; color:var(--t-iron) !important;
    line-height:1.65 !important; margin-top:.9rem;
}

/* FOOTER ────────────────────────────────────────────────────── */
.footer {
    text-align:center;
    padding: 2.5rem 1rem 1.5rem;
    border-top:1px solid var(--border-dim);
    margin-top:2.5rem;
}
.footer-brand {
    font-family:'Instrument Serif',serif;
    font-size:17px; color:var(--teal-400);
    margin-bottom:.35rem;
}
.footer-sub { font-size:11px; color:var(--t-iron); letter-spacing:.06em; line-height:1.9; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# LOAD MODEL
# ════════════════════════════════════════════════════════════════
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
if not os.path.exists(model_path):
    st.error("❌ Model file `model.pkl` not found. Place it next to this script.")
    st.stop()
with open(model_path, "rb") as f:
    model = pickle.load(f)

# ════════════════════════════════════════════════════════════════
# PREDICTION  (unchanged)
# ════════════════════════════════════════════════════════════════
def predict_anemia(data):
    arr = np.asarray(data, dtype=float).reshape(1, -1)
    pred = model.predict(arr)[0]
    try:
        confidence = max(model.predict_proba(arr)[0]) * 100
    except Exception:
        confidence = None
    label = "Anemic" if pred == 1 else "Not Anemic"
    return label, confidence

# ════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sb-logo">AnemiaCheck</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-tag">Clinical Screening System</div>', unsafe_allow_html=True)
    st.markdown('<span class="sb-online"><span class="sb-pulse"></span> Model Online</span>', unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<span class="sb-section-h">About</span>', unsafe_allow_html=True)
    st.markdown("""
    <p style='font-size:13px;color:#3d6870;line-height:1.75;margin:0'>
    This tool uses a trained ML model to detect anemia risk from routine blood count parameters.
    Built on the <strong style='color:#6b9ea4'>PIMA-style hematology dataset</strong>.
    </p>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<span class="sb-section-h">Model Specs</span>', unsafe_allow_html=True)
    for k, v in [("Algorithm","RFC / SVM"), ("Features","Blood CBC"),
                  ("Output","Binary"), ("Status","Deployed")]:
        st.markdown(f'<div class="sb-item"><span class="sb-item-k">{k}</span><span class="sb-item-v">{v}</span></div>',
                    unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<span class="sb-section-h">Reference Ranges</span>', unsafe_allow_html=True)
    for k, v in [("Hemoglobin ♂","13.5–17.5 g/dL"), ("Hemoglobin ♀","12.0–15.5 g/dL"),
                  ("MCV","80–100 fL"), ("MCH","27–33 pg"), ("MCHC","31.5–35.7 g/dL")]:
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;padding:.45rem 0;
                    border-bottom:1px solid rgba(122,178,178,0.08);font-size:12px'>
            <span style='color:#3d6870'>{k}</span>
            <span style='color:#6b9ea4;font-family:"DM Mono",monospace;font-size:11px'>{v}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-tip">⚠️ Educational use only. Not a substitute for professional clinical diagnosis.</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <p style='font-size:11px;color:#2a4f58;text-align:center;line-height:1.9'>
        Built by <strong style='color:#3d6870'>Kartvaya Raikwar</strong><br>
        Machine Learning · Healthcare AI
    </p>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# HERO
# ════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-badge">
        <span class="hero-dot"></span>
        Clinical Screening System
    </div>
    <div class="hero-title">Anemia Risk <em>Assessment</em></div>
    <p class="hero-sub">Enter complete blood count (CBC) parameters to receive an AI-assisted anemia risk classification with model confidence scoring.</p>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# METRIC STRIP
# ════════════════════════════════════════════════════════════════
c1, c2, c3, c4 = st.columns(4)
for col, (ico, val, lbl) in zip([c1,c2,c3,c4], [
    ("🧬","CBC",     "Input Type"),
    ("⚡","< 1s",    "Response Time"),
    ("🎯","Binary",  "Output Class"),
    ("📋","~85%",    "Model Accuracy"),
]):
    col.markdown(f"""
    <div class="mc-wrap">
        <div class="mc-icon">{ico}</div>
        <span class="mc-val">{val}</span>
        <div class="mc-lbl">{lbl}</div>
    </div>""", unsafe_allow_html=True)

st.write("")

# ════════════════════════════════════════════════════════════════
# INPUTS
# ════════════════════════════════════════════════════════════════
left, right = st.columns([3, 2], gap="large")

with left:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-head">🔴 &nbsp; Red Blood Cell Indices</div>', unsafe_allow_html=True)

    fa, fb = st.columns(2)
    with fa:
        st.markdown('<div class="field-lbl">Hemoglobin (g/dL)</div>', unsafe_allow_html=True)
        hemoglobin = st.number_input("Hemoglobin", min_value=0.0, max_value=25.0, value=0.0,
                                     step=0.1, format="%.1f", label_visibility="collapsed",
                                     help="Blood hemoglobin concentration. Normal ♂: 13.5–17.5, ♀: 12.0–15.5 g/dL")
    with fb:
        st.markdown('<div class="field-lbl">MCH (pg)</div>', unsafe_allow_html=True)
        mch = st.number_input("MCH", min_value=0.0, max_value=50.0, value=27.0,
                              step=0.1, format="%.1f", label_visibility="collapsed",
                              help="Mean Corpuscular Hemoglobin. Normal: 27–33 pg")

    fc, fd = st.columns(2)
    with fc:
        st.markdown('<div class="field-lbl">MCHC (g/dL)</div>', unsafe_allow_html=True)
        mchc = st.number_input("MCHC", min_value=0.0, max_value=45.0, value=31.5,
                               step=0.1, format="%.1f", label_visibility="collapsed",
                               help="Mean Corpuscular Hemoglobin Concentration. Normal: 31.5–35.7 g/dL")
    with fd:
        st.markdown('<div class="field-lbl">MCV (fL)</div>', unsafe_allow_html=True)
        mcv = st.number_input("MCV", min_value=0.0, max_value=130.0, value=80.0,
                              step=0.1, format="%.1f", label_visibility="collapsed",
                              help="Mean Corpuscular Volume. Normal: 80–100 fL")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-head">⚪ &nbsp; Patient Demographics</div>', unsafe_allow_html=True)

    fg, fh = st.columns(2)
    with fg:
        st.markdown('<div class="field-lbl">Gender</div>', unsafe_allow_html=True)
        gender_label = st.selectbox("Gender", ["Female", "Male"], label_visibility="collapsed")
        gender = 0 if gender_label == "Female" else 1
    with fh:
        st.markdown('<div class="field-lbl">Age (years)</div>', unsafe_allow_html=True)
        age = st.number_input("Age", min_value=1, max_value=120, value=25,
                              label_visibility="collapsed", help="Patient age in years")
    st.markdown('</div>', unsafe_allow_html=True)

    predict_clicked = st.button("Run Anemia Screening", use_container_width=True)

# ════════════════════════════════════════════════════════════════
# RIGHT COLUMN
# ════════════════════════════════════════════════════════════════
with right:
    st.markdown('<div class="sum-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-head" style="margin-bottom:1.1rem">📋 &nbsp; Parameter Summary</div>',
                unsafe_allow_html=True)

    for name, val, unit in [
        ("Gender",     gender_label,        ""),
        ("Hemoglobin", f"{hemoglobin:.1f}", "g/dL"),
        ("MCH",        f"{mch:.1f}",        "pg"),
        ("MCHC",       f"{mchc:.1f}",       "g/dL"),
        ("MCV",        f"{mcv:.1f}",        "fL"),
    ]:
        u = f'<span style="font-size:10px;color:#2a4f58;margin-left:3px">{unit}</span>' if unit else ""
        st.markdown(f"""
        <div class="sum-row">
            <span class="sum-key">{name}</span>
            <span class="sum-val">{val}{u}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if predict_clicked:
        # Feature order must match training: Gender, Hemoglobin, MCH, MCHC, MCV
        data_in = [gender, hemoglobin, mch, mchc, mcv]

        with st.spinner("Analyzing CBC parameters…"):
            time.sleep(0.85)
            result, confidence = predict_anemia(data_in)

        st.write("")
        is_anemic = result == "Anemic"

        if is_anemic:
            st.markdown("""
            <div class="result-wrap result-risk">
                <div class="result-ico">⚠️</div>
                <div class="result-lbl">Anemia Detected</div>
                <div class="result-desc">Biomarkers indicate anemia risk.<br>Clinical follow-up is recommended.</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-wrap result-clear">
                <div class="result-ico">✅</div>
                <div class="result-lbl">Not Anemic</div>
                <div class="result-desc">Parameters within acceptable range.<br>Continue routine health monitoring.</div>
            </div>""", unsafe_allow_html=True)

        if confidence is not None:
            conf_v = confidence / 100.0
            if confidence >= 80:
                bc, bt = "conf-high", "High Confidence"
            elif confidence >= 60:
                bc, bt = "conf-mid",  "Moderate Confidence"
            else:
                bc, bt = "conf-low",  "Low Confidence"

            st.markdown(f"""
            <div class="conf-card">
                <div class="conf-head">
                    <span class="conf-title">Model Confidence</span>
                    <span class="conf-pct">{confidence:.1f}%</span>
                </div>""", unsafe_allow_html=True)
            st.progress(conf_v)
            st.markdown(f"""
                <div style="display:flex;justify-content:flex-end;margin-top:.7rem">
                    <span class="conf-badge {bc}">{bt}</span>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="disclaimer">
            <strong style="color:#6b9ea4">Disclaimer:</strong>
            This result is generated by a machine learning model for educational purposes only.
            It does not constitute a medical diagnosis.
            Consult a licensed haematologist or physician.
        </div>""", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="await-box">
            <div class="await-icon">🔬</div>
            <div class="await-title">Awaiting Analysis</div>
            <div class="await-sub">
                Enter CBC parameters and click<br>
                <span class="await-cta">Run Anemia Screening</span>
            </div>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
    <div class="footer-brand">AnemiaCheck · Clinical Screening System</div>
    <div class="footer-sub">
        Developed by <strong style="color:#6b9ea4">Kartvaya Raikwar</strong>
        &nbsp;·&nbsp; Machine Learning · Healthcare AI
        &nbsp;·&nbsp; For educational purposes only &nbsp;·&nbsp; © 2025
    </div>
</div>
""", unsafe_allow_html=True)
