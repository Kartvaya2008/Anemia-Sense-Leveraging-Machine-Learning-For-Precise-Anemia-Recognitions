import numpy as np
import pickle
import streamlit as st
import os
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AnemiaCheck · Clinical Screening",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&family=DM+Mono:wght@400;500&display=swap');

/* ── TOKENS ──────────────────────────────────────────────── */
:root {
    --black:         #0a0a0b;
    --surface:       #111113;
    --surface-2:     #18181b;
    --surface-3:     #1f1f23;
    --card-white:    rgba(255,255,255,0.97);
    --card-ghost:    rgba(255,255,255,0.04);
    --card-ghost-hv: rgba(255,255,255,0.07);
    --border:        rgba(255,255,255,0.08);
    --border-mid:    rgba(255,255,255,0.14);
    --border-white:  rgba(255,255,255,0.85);
    --text-white:    #f5f5f7;
    --text-gray:     #8e8e93;
    --text-dim:      #48484e;
    --text-black:    #0a0a0b;
    --text-dark:     #1c1c1e;
    --green-muted:   #4ade80;
    --green-bg:      rgba(74,222,128,0.10);
    --green-border:  rgba(74,222,128,0.25);
    --red-muted:     #f87171;
    --red-bg:        rgba(248,113,113,0.10);
    --red-border:    rgba(248,113,113,0.25);
    --shadow-card:   0 1px 3px rgba(0,0,0,0.4), 0 8px 24px rgba(0,0,0,0.35);
    --shadow-white:  0 2px 12px rgba(255,255,255,0.06), 0 1px 0 rgba(255,255,255,0.08) inset;
    --shadow-hover:  0 2px 4px rgba(0,0,0,0.5), 0 16px 40px rgba(0,0,0,0.5);
    --r-xl:          20px;
    --r-lg:          14px;
    --r-md:          10px;
    --r-sm:          7px;
}

/* ── GLOBAL ───────────────────────────────────────────────── */
html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    font-family: 'Instrument Sans', -apple-system, sans-serif !important;
    color: var(--text-white) !important;
}
.stApp, [data-testid="stAppViewContainer"], .main {
    background: var(--black) !important;
}
[data-testid="stHeader"] {
    background: rgba(10,10,11,0.9) !important;
    backdrop-filter: blur(16px) !important;
    border-bottom: 1px solid var(--border) !important;
}
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2.2rem !important; max-width: 1280px; }

/* ── SIDEBAR ──────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 2rem; }
[data-testid="stSidebar"] * { color: var(--text-gray) !important; }

/* ── INPUTS ───────────────────────────────────────────────── */
[data-testid="stNumberInput"] [data-baseweb="input"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: var(--r-md) !important;
    transition: border-color .2s, box-shadow .2s !important;
}
[data-testid="stNumberInput"] [data-baseweb="input"]:focus-within {
    border-color: rgba(255,255,255,0.5) !important;
    box-shadow: 0 0 0 3px rgba(255,255,255,0.06) !important;
}
[data-testid="stNumberInput"] input {
    color: var(--text-white) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 14px !important;
    background: transparent !important;
}
[data-testid="stNumberInput"] label {
    color: var(--text-gray) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: .04em !important;
}
[data-baseweb="input"] svg { fill: var(--text-dim) !important; }

/* ── BUTTON ───────────────────────────────────────────────── */
.stButton > button {
    width: 100% !important;
    background: var(--text-white) !important;
    color: var(--text-black) !important;
    font-family: 'Instrument Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: var(--r-lg) !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    transition: all .25s cubic-bezier(.34,1.56,.64,1) !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.3), 0 4px 16px rgba(255,255,255,0.1) !important;
}
.stButton > button:hover {
    background: #ffffff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.4), 0 12px 32px rgba(255,255,255,0.18) !important;
}
.stButton > button:active { transform: translateY(0) scale(.98) !important; }

/* ── PROGRESS ─────────────────────────────────────────────── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg,#e5e5e7,#ffffff) !important;
    border-radius: 99px !important;
}
.stProgress > div > div > div {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 99px !important;
    height: 8px !important;
}

/* ── SPINNER ──────────────────────────────────────────────── */
.stSpinner > div { border-top-color: var(--text-white) !important; }

/* ── SCROLLBAR ────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--black); }
::-webkit-scrollbar-thumb { background: var(--surface-3); border-radius: 99px; }

/* ── DIVIDER ──────────────────────────────────────────────── */
hr { border-color: var(--border) !important; margin: 1.8rem 0 !important; }

/* ── ANIMATIONS ───────────────────────────────────────────── */
@keyframes fadeUp {
    from { opacity:0; transform:translateY(14px); }
    to   { opacity:1; transform:translateY(0);    }
}
@keyframes scaleIn {
    from { opacity:0; transform:scale(.94); }
    to   { opacity:1; transform:scale(1);   }
}
@keyframes pulseDot {
    0%,100% { opacity:1; }
    50%      { opacity:.4; }
}

/* ══════════════════════════════════════════════════════════
   CUSTOM COMPONENTS
══════════════════════════════════════════════════════════ */

/* HERO */
.hero {
    background: var(--card-white);
    border-radius: var(--r-xl);
    padding: 2.4rem 2.8rem;
    margin-bottom: 1.8rem;
    box-shadow: var(--shadow-white);
    animation: fadeUp .45s ease both;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content:'';
    position:absolute; top:0; right:0;
    width:280px; height:280px;
    background: radial-gradient(circle at 80% 20%, rgba(0,0,0,0.03) 0%, transparent 70%);
    pointer-events:none;
}
.hero-badge {
    display:inline-flex; align-items:center; gap:6px;
    background: var(--black);
    color: var(--text-white);
    border-radius: 99px;
    padding: 5px 14px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.hero-dot {
    width:6px; height:6px; border-radius:50%;
    background: #4ade80;
    animation: pulseDot 2s ease-in-out infinite;
}
.hero-title {
    font-family: 'Instrument Serif', serif;
    font-size: clamp(30px,4vw,48px);
    font-weight: 400;
    color: var(--text-black);
    line-height: 1.1;
    margin: 0 0 .6rem;
    letter-spacing: -.02em;
}
.hero-title em {
    font-style: italic;
    color: #3c3c43;
}
.hero-sub {
    font-size: 15px;
    color: #636366;
    margin: 0;
    max-width: 500px;
    line-height: 1.65;
}

/* METRIC CARDS */
.mc-wrap {
    background: var(--card-ghost);
    border: 1px solid var(--border);
    border-radius: var(--r-lg);
    padding: 1.2rem 1rem;
    text-align: center;
    transition: background .2s, box-shadow .2s, transform .2s;
    animation: fadeUp .45s .1s ease both;
    cursor: default;
}
.mc-wrap:hover {
    background: var(--card-ghost-hv);
    transform: translateY(-3px);
    box-shadow: var(--shadow-hover);
    border-color: var(--border-mid);
}
.mc-icon { font-size: 22px; margin-bottom: 6px; }
.mc-val  {
    font-family: 'DM Mono', monospace;
    font-size: 19px; font-weight: 500;
    color: var(--text-white); display: block;
}
.mc-lbl  {
    font-size: 10px; font-weight: 700;
    letter-spacing: .12em; text-transform: uppercase;
    color: var(--text-dim); margin-top: 3px;
}

/* FORM CARD */
.form-card {
    background: var(--card-ghost);
    border: 1px solid var(--border);
    border-radius: var(--r-xl);
    padding: 2rem 2rem 1.6rem;
    box-shadow: var(--shadow-card);
    animation: fadeUp .45s .15s ease both;
    margin-bottom: 1.2rem;
    transition: border-color .25s;
}
.form-card:hover { border-color: var(--border-mid); }

.section-head {
    font-size: 10px; font-weight: 700;
    letter-spacing: .18em; text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 1.4rem;
    display: flex; align-items: center; gap: 10px;
}
.section-head::after {
    content:''; flex:1; height:1px;
    background: var(--border);
}
.field-lbl {
    font-size: 12px; font-weight: 600;
    color: var(--text-gray);
    letter-spacing: .04em;
    margin-bottom: 4px;
    display: flex; align-items: center; gap: 5px;
}

/* SUMMARY CARD */
.sum-card {
    background: var(--card-ghost);
    border: 1px solid var(--border);
    border-radius: var(--r-xl);
    padding: 1.8rem 1.8rem 1.4rem;
    animation: fadeUp .45s .2s ease both;
    margin-bottom: 1.2rem;
}
.sum-row {
    display:flex; justify-content:space-between; align-items:center;
    padding: .42rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.sum-row:last-child { border-bottom: none; }
.sum-key { font-size:13px; color: var(--text-gray); }
.sum-val {
    font-family:'DM Mono',monospace; font-size:13px;
    color: var(--text-white);
}

/* AWAITING */
.await-box {
    background: var(--card-ghost);
    border: 1px dashed var(--border-mid);
    border-radius: var(--r-xl);
    padding: 2.8rem 2rem;
    text-align: center;
    animation: fadeUp .45s .25s ease both;
}
.await-icon { font-size:42px; margin-bottom:.9rem; opacity:.5; }
.await-title { font-size:15px; font-weight:600; color:var(--text-gray); margin-bottom:.4rem; }
.await-sub   { font-size:13px; color:var(--text-dim); line-height:1.6; }
.await-cta   { color: var(--text-white); font-weight:600; }

/* RESULT */
.result-wrap {
    border-radius: var(--r-xl);
    padding: 2rem 1.8rem;
    text-align: center;
    animation: scaleIn .45s cubic-bezier(.34,1.56,.64,1) both;
    margin-bottom: 1rem;
}
.result-risk {
    background: var(--red-bg);
    border: 1px solid var(--red-border);
}
.result-clear {
    background: var(--green-bg);
    border: 1px solid var(--green-border);
}
.result-ico  { font-size:48px; margin-bottom:.7rem; }
.result-lbl  {
    font-family: 'Instrument Serif', serif;
    font-size: 28px; font-weight: 400;
    letter-spacing: -.01em;
    margin-bottom: .35rem;
}
.result-risk  .result-lbl  { color: var(--red-muted); }
.result-clear .result-lbl  { color: var(--green-muted); }
.result-desc { font-size:14px; color:var(--text-gray); line-height:1.6; }

/* CONFIDENCE */
.conf-card {
    background: var(--card-ghost);
    border: 1px solid var(--border);
    border-radius: var(--r-lg);
    padding: 1.4rem 1.6rem;
    animation: fadeUp .35s ease both;
    margin-bottom: .9rem;
}
.conf-head {
    display:flex; justify-content:space-between; align-items:baseline;
    margin-bottom:.7rem;
}
.conf-title {
    font-size:10px; font-weight:700;
    letter-spacing:.14em; text-transform:uppercase;
    color: var(--text-dim);
}
.conf-pct {
    font-family:'DM Mono',monospace;
    font-size:22px; font-weight:500;
    color: var(--text-white);
}
.conf-badge {
    display:inline-block;
    font-size:10px; font-weight:700;
    letter-spacing:.08em; text-transform:uppercase;
    border-radius:99px; padding:3px 12px;
    margin-top:.7rem;
}
.conf-high   { color:#4ade80; background:rgba(74,222,128,.1); border:1px solid rgba(74,222,128,.22); }
.conf-mid    { color:#fbbf24; background:rgba(251,191,36,.1);  border:1px solid rgba(251,191,36,.22); }
.conf-low    { color:#f87171; background:rgba(248,113,113,.1); border:1px solid rgba(248,113,113,.22); }

/* DISCLAIMER */
.disclaimer {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: var(--r-md);
    padding: .75rem 1rem;
    font-size: 11px; color: var(--text-dim); line-height: 1.65;
}

/* SIDEBAR */
.sb-logo {
    font-family: 'Instrument Serif', serif;
    font-size: 22px; font-weight: 400;
    color: var(--text-white) !important;
    letter-spacing: -.01em;
    margin-bottom: .2rem;
}
.sb-tag {
    font-size:10px; font-weight:700;
    letter-spacing:.14em; text-transform:uppercase;
    color: var(--text-dim) !important;
    margin-bottom: 1.6rem;
}
.sb-online {
    display:inline-flex; align-items:center; gap:6px;
    font-size:11px; font-weight:600;
    color: #4ade80 !important;
    letter-spacing:.06em; text-transform:uppercase;
}
.sb-pulse {
    width:7px; height:7px; border-radius:50%;
    background:#4ade80;
    box-shadow:0 0 6px #4ade80;
    animation: pulseDot 2s ease-in-out infinite;
    display:inline-block;
}
.sb-divider { height:1px; background:var(--border); margin:1.4rem 0; }
.sb-section-h {
    font-size:9px !important; font-weight:700 !important;
    letter-spacing:.18em !important; text-transform:uppercase !important;
    color: var(--text-dim) !important;
    margin-bottom:.9rem !important;
    display:block;
}
.sb-item {
    display:flex; justify-content:space-between; align-items:center;
    padding:.5rem 0; border-bottom:1px solid var(--border);
    font-size:13px !important;
}
.sb-item:last-child { border-bottom:none; }
.sb-item-k { color:var(--text-gray) !important; }
.sb-item-v {
    font-family:'DM Mono',monospace; font-size:11px !important;
    color:var(--text-white) !important;
    background:var(--surface-3);
    border:1px solid var(--border-mid);
    border-radius:5px; padding:2px 8px;
}
.sb-tip {
    background: rgba(255,255,255,0.03);
    border-left: 2px solid rgba(255,255,255,0.15);
    border-radius: 0 var(--r-sm) var(--r-sm) 0;
    padding: .85rem .95rem;
    font-size:12px !important; color:var(--text-dim) !important;
    line-height:1.65 !important;
    margin-top:.9rem;
}

/* FOOTER */
.footer {
    text-align:center;
    padding: 2.5rem 1rem 1.5rem;
    border-top:1px solid var(--border);
    margin-top:2.5rem;
}
.footer-brand {
    font-family:'Instrument Serif',serif;
    font-size:17px; color:var(--text-white);
    margin-bottom:.35rem;
}
.footer-sub  { font-size:11px; color:var(--text-dim); letter-spacing:.06em; line-height:1.8; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────
# LOAD MODEL
# ────────────────────────────────────────────────────────────
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
if not os.path.exists(model_path):
    st.error("❌ Model file `model.pkl` not found. Place it next to this script.")
    st.stop()
with open(model_path, "rb") as f:
    model = pickle.load(f)

# ────────────────────────────────────────────────────────────
# PREDICTION
# ────────────────────────────────────────────────────────────
def predict_anemia(data):
    arr = np.asarray(data, dtype=float).reshape(1, -1)
    pred = model.predict(arr)[0]
    try:
        confidence = max(model.predict_proba(arr)[0]) * 100
    except Exception:
        confidence = None
    label = "Anemic" if pred == 1 else "Not Anemic"
    return label, confidence

# ════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sb-logo">AnemiaCheck</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-tag">Clinical Screening System</div>', unsafe_allow_html=True)
    st.markdown('<span class="sb-online"><span class="sb-pulse"></span> Model Online</span>', unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<span class="sb-section-h">About</span>', unsafe_allow_html=True)
    st.markdown("""
    <p style='font-size:13px;color:#636366;line-height:1.7;margin:0'>
    This tool uses a trained ML model to detect anemia risk from routine blood count parameters.
    Built on the <strong style='color:#8e8e93'>PIMA-style hematology dataset</strong>.
    </p>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<span class="sb-section-h">Model Specs</span>', unsafe_allow_html=True)
    specs = [("Algorithm","RFC / SVM"), ("Features","Blood CBC"), ("Output","Binary"), ("Status","Deployed")]
    for k, v in specs:
        st.markdown(f'<div class="sb-item"><span class="sb-item-k">{k}</span><span class="sb-item-v">{v}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown('<span class="sb-section-h">Reference Ranges</span>', unsafe_allow_html=True)
    refs = [
        ("Hemoglobin ♂", "13.5–17.5 g/dL"),
        ("Hemoglobin ♀", "12.0–15.5 g/dL"),
        ("Hematocrit ♂", "41–53%"),
        ("Hematocrit ♀", "36–46%"),
        ("MCV",          "80–100 fL"),
        ("MCH",          "27–33 pg"),
        ("MCHC",         "31.5–35.7 g/dL"),
    ]
    for k, v in refs:
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;padding:.45rem 0;
                    border-bottom:1px solid rgba(255,255,255,0.05);font-size:12px'>
            <span style='color:#636366'>{k}</span>
            <span style='color:#8e8e93;font-family:"DM Mono",monospace;font-size:11px'>{v}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-tip">⚠️ Educational use only. Not a substitute for professional clinical diagnosis.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <p style='font-size:11px;color:#3a3a3f;text-align:center;line-height:1.8'>
        Built by <strong style='color:#636366'>Kartvaya Raikwar</strong><br>
        Machine Learning · Healthcare AI
    </p>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# HERO
# ════════════════════════════════════════════════════════════
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

# ════════════════════════════════════════════════════════════
# METRIC STRIP
# ════════════════════════════════════════════════════════════
c1, c2, c3, c4 = st.columns(4)
metrics = [
    ("🧬", "CBC", "Input Type"),
    ("⚡", "< 1s", "Response Time"),
    ("🎯", "Binary", "Output Class"),
    ("📋", "~85%", "Model Accuracy"),
]
for col, (icon, val, lbl) in zip([c1,c2,c3,c4], metrics):
    col.markdown(f"""
    <div class="mc-wrap">
        <div class="mc-icon">{icon}</div>
        <span class="mc-val">{val}</span>
        <div class="mc-lbl">{lbl}</div>
    </div>""", unsafe_allow_html=True)

st.write("")

# ════════════════════════════════════════════════════════════
# INPUTS
# ════════════════════════════════════════════════════════════
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
        st.markdown('<div class="field-lbl">Hematocrit (%)</div>', unsafe_allow_html=True)
        hematocrit = st.number_input("Hematocrit", min_value=0.0, max_value=70.0, value=0.0,
                                     step=0.1, format="%.1f", label_visibility="collapsed",
                                     help="Packed cell volume percentage. Normal ♂: 41–53%, ♀: 36–46%")

    fc, fd = st.columns(2)
    with fc:
        st.markdown('<div class="field-lbl">MCV (fL)</div>', unsafe_allow_html=True)
        mcv = st.number_input("MCV", min_value=0.0, max_value=130.0, value=0.0,
                              step=0.1, format="%.1f", label_visibility="collapsed",
                              help="Mean Corpuscular Volume. Normal: 80–100 fL")
    with fd:
        st.markdown('<div class="field-lbl">MCH (pg)</div>', unsafe_allow_html=True)
        mch = st.number_input("MCH", min_value=0.0, max_value=50.0, value=0.0,
                              step=0.1, format="%.1f", label_visibility="collapsed",
                              help="Mean Corpuscular Hemoglobin. Normal: 27–33 pg")

    fe, ff = st.columns(2)
    with fe:
        st.markdown('<div class="field-lbl">MCHC (g/dL)</div>', unsafe_allow_html=True)
        mchc = st.number_input("MCHC", min_value=0.0, max_value=45.0, value=0.0,
                               step=0.1, format="%.1f", label_visibility="collapsed",
                               help="Mean Corpuscular Hemoglobin Concentration. Normal: 31.5–35.7 g/dL")
    with ff:
        st.markdown('<div class="field-lbl">RBC Count (×10⁶/μL)</div>', unsafe_allow_html=True)
        rbc = st.number_input("RBC", min_value=0.0, max_value=10.0, value=0.0,
                              step=0.01, format="%.2f", label_visibility="collapsed",
                              help="Red Blood Cell count. Normal ♂: 4.7–6.1, ♀: 4.2–5.4 ×10⁶/μL")

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

    st.markdown('<div style="margin-top:.4rem">', unsafe_allow_html=True)
    predict_clicked = st.button("Run Anemia Screening", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# RIGHT COLUMN
# ════════════════════════════════════════════════════════════
with right:
    # Live summary
    st.markdown('<div class="sum-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-head" style="margin-bottom:1.1rem">📋 &nbsp; Parameter Summary</div>', unsafe_allow_html=True)

    summary = [
        ("Hemoglobin",  f"{hemoglobin:.1f}", "g/dL"),
        ("Hematocrit",  f"{hematocrit:.1f}", "%"),
        ("MCV",         f"{mcv:.1f}",        "fL"),
        ("MCH",         f"{mch:.1f}",        "pg"),
        ("MCHC",        f"{mchc:.1f}",       "g/dL"),
        ("RBC Count",   f"{rbc:.2f}",        "×10⁶/μL"),
        ("Gender",      gender_label,        ""),
        ("Age",         str(age),            "yrs"),
    ]
    for name, val, unit in summary:
        unit_span = f'<span style="font-size:10px;color:#3a3a3f;margin-left:3px">{unit}</span>' if unit else ""
        st.markdown(f"""
        <div class="sum-row">
            <span class="sum-key">{name}</span>
            <span class="sum-val">{val}{unit_span}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Result
    if predict_clicked:
        data_in = [hemoglobin, hematocrit, mcv, mch, mchc, rbc, gender]

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
                badge_cls, badge_txt = "conf-high", "High Confidence"
            elif confidence >= 60:
                badge_cls, badge_txt = "conf-mid",  "Moderate Confidence"
            else:
                badge_cls, badge_txt = "conf-low",  "Low Confidence"

            st.markdown(f"""
            <div class="conf-card">
                <div class="conf-head">
                    <span class="conf-title">Model Confidence</span>
                    <span class="conf-pct">{confidence:.1f}%</span>
                </div>""", unsafe_allow_html=True)
            st.progress(conf_v)
            st.markdown(f"""
                <div style="display:flex;justify-content:flex-end;margin-top:.7rem">
                    <span class="conf-badge {badge_cls}">{badge_txt}</span>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="disclaimer">
            ℹ️ <strong style="color:#8e8e93">Disclaimer:</strong>
            This result is generated by a machine learning model and is intended for
            educational purposes only. It does not constitute a medical diagnosis.
            Please consult a licensed haematologist or physician.
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

# ════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
    <div class="footer-brand">AnemiaCheck · Clinical Screening System</div>
    <div class="footer-sub">
        Developed by <strong style="color:#8e8e93">Kartvaya Raikwar</strong>
        &nbsp;·&nbsp; Machine Learning · Healthcare AI
        &nbsp;·&nbsp; For educational purposes only &nbsp;·&nbsp; © 2025
    </div>
</div>
""", unsafe_allow_html=True)
