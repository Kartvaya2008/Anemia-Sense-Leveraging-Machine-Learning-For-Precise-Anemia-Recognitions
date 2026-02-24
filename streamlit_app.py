import numpy as np
import pickle
import streamlit as st
import os
import time
import datetime

# ═══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="HemaScope AI · Clinical Screening",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ═══════════════════════════════════════════════════════════════
if "history" not in st.session_state:
    st.session_state.history = []
if "result" not in st.session_state:
    st.session_state.result = None
if "confidence" not in st.session_state:
    st.session_state.confidence = None
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "last_inputs" not in st.session_state:
    st.session_state.last_inputs = {}

# ═══════════════════════════════════════════════════════════════
#  THEME TOKENS
# ═══════════════════════════════════════════════════════════════
DARK = {
    "bg":       "#020617",
    "bg2":      "#0f172a",
    "bg3":      "#1e293b",
    "card":     "rgba(255,255,255,0.04)",
    "card2":    "rgba(255,255,255,0.07)",
    "border":   "rgba(255,255,255,0.08)",
    "t1":       "#f1f5f9",
    "t2":       "#94a3b8",
    "t3":       "#475569",
    "teal":     "#22d3ee",
    "cyan":     "#06b6d4",
    "green":    "#10b981",
    "rose":     "#f43f5e",
    "amber":    "#f59e0b",
    "sb_bg":    "#060d1c",
}
LIGHT = {
    "bg":       "#f8fafc",
    "bg2":      "#f1f5f9",
    "bg3":      "#e2e8f0",
    "card":     "rgba(255,255,255,0.9)",
    "card2":    "rgba(255,255,255,1.0)",
    "border":   "rgba(0,0,0,0.1)",
    "t1":       "#0f172a",
    "t2":       "#475569",
    "t3":       "#94a3b8",
    "teal":     "#0891b2",
    "cyan":     "#0e7490",
    "green":    "#059669",
    "rose":     "#e11d48",
    "amber":    "#d97706",
    "sb_bg":    "#f1f5f9",
}
T = DARK if st.session_state.theme == "dark" else LIGHT
IS_DARK = st.session_state.theme == "dark"

# ═══════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {{
    --bg:      {T['bg']};
    --bg2:     {T['bg2']};
    --bg3:     {T['bg3']};
    --card:    {T['card']};
    --card2:   {T['card2']};
    --border:  {T['border']};
    --t1:      {T['t1']};
    --t2:      {T['t2']};
    --t3:      {T['t3']};
    --teal:    {T['teal']};
    --cyan:    {T['cyan']};
    --green:   {T['green']};
    --rose:    {T['rose']};
    --amber:   {T['amber']};
    --sb-bg:   {T['sb_bg']};
    --glow-c:  rgba(34,211,238,0.18);
    --glow-g:  rgba(16,185,129,0.18);
    --glow-r:  rgba(244,63,94,0.18);
}}

/* ── GLOBAL ── */
html,body,[data-testid="stAppViewContainer"] {{
    background: var(--bg) !important;
    font-family: 'Outfit', sans-serif !important;
    color: var(--t1) !important;
}}
[data-testid="stAppViewContainer"]>.main {{ background: var(--bg) !important; }}
[data-testid="stHeader"] {{
    background: rgba(2,6,23,0.88) !important;
    backdrop-filter: blur(24px) !important;
    border-bottom: 1px solid var(--border) !important;
}}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {{
    background: var(--sb-bg) !important;
    border-right: 1px solid var(--border) !important;
}}
[data-testid="stSidebar"] * {{ font-family:'Outfit',sans-serif !important; color: var(--t2) !important; }}

/* ── INPUTS ── */
.stNumberInput [data-baseweb="input"] {{
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--t1) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 15px !important;
    transition: border-color .25s, box-shadow .25s !important;
}}
.stNumberInput [data-baseweb="input"]:focus-within {{
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(34,211,238,0.15) !important;
}}
.stNumberInput input {{ color: var(--t1) !important; background: transparent !important; }}
.stNumberInput label {{
    color: var(--t2) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
}}

/* ── BUTTON ── */
.stButton>button {{
    background: linear-gradient(135deg,#06b6d4 0%,#0284c7 50%,#7c3aed 100%) !important;
    color: #fff !important;
    font-family: 'Outfit',sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    width: 100% !important;
    transition: all .35s cubic-bezier(.34,1.56,.64,1) !important;
    box-shadow: 0 8px 30px rgba(6,182,212,0.35), 0 0 0 1px rgba(255,255,255,0.08) !important;
    position: relative !important;
}}
.stButton>button:hover {{
    transform: translateY(-4px) scale(1.02) !important;
    box-shadow: 0 20px 50px rgba(6,182,212,0.5), 0 0 60px rgba(124,58,237,0.25) !important;
    filter: brightness(1.12) !important;
}}
.stButton>button:active {{ transform: translateY(-1px) scale(.99) !important; }}

/* ── PROGRESS BAR ── */
.stProgress>div>div>div>div {{
    background: linear-gradient(90deg,var(--teal),var(--cyan)) !important;
    border-radius: 99px !important;
    transition: width .8s cubic-bezier(.16,1,.3,1) !important;
}}
.stProgress>div>div>div {{
    background: rgba(255,255,255,0.06) !important;
    border-radius: 99px !important;
}}

/* ── SCROLLBAR ── */
::-webkit-scrollbar{{width:5px}}
::-webkit-scrollbar-track{{background:transparent}}
::-webkit-scrollbar-thumb{{background:var(--border);border-radius:99px}}

/* ── SELECT/RADIO (theme toggle) ── */
.stRadio>div {{flex-direction:row !important; gap:10px !important}}
.stRadio label {{color:var(--t2) !important; font-size:13px !important}}
div[data-baseweb="radio"]>div {{background:transparent !important}}

hr{{border-color:var(--border) !important; margin:1.5rem 0 !important}}

/* ══════════════════════════════
   CUSTOM COMPONENT STYLES
══════════════════════════════ */

/* Hero card */
.hero-card {{
    background: linear-gradient(135deg,
        rgba(6,182,212,0.08) 0%,
        rgba(255,255,255,0.03) 50%,
        rgba(124,58,237,0.06) 100%);
    border: 1px solid rgba(6,182,212,0.2);
    border-radius: 24px;
    padding: 40px 44px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 80px rgba(6,182,212,0.06), inset 0 1px 0 rgba(255,255,255,0.06);
    animation: heroIn .7s cubic-bezier(.16,1,.3,1) both;
}}
.hero-card::before {{
    content:'';
    position:absolute; top:-80px; right:-80px;
    width:300px; height:300px;
    background: radial-gradient(circle, rgba(6,182,212,0.12) 0%, transparent 70%);
    pointer-events:none;
}}
@keyframes heroIn {{
    from{{opacity:0;transform:translateY(-20px)}}
    to{{opacity:1;transform:translateY(0)}}
}}

.badge-clinical {{
    display:inline-flex; align-items:center; gap:6px;
    padding:5px 14px; border-radius:99px;
    background:rgba(6,182,212,0.12); color:var(--teal);
    border:1px solid rgba(6,182,212,0.3);
    font-size:11px; font-weight:700; letter-spacing:.1em;
    text-transform:uppercase; margin-bottom:14px;
}}
.badge-clinical::before {{
    content:''; width:7px; height:7px; background:var(--teal);
    border-radius:50%; animation:dot-blink 1.6s ease-in-out infinite;
}}
@keyframes dot-blink{{0%,100%{{opacity:1;box-shadow:0 0 0 0 rgba(34,211,238,.5)}}
50%{{opacity:.5;box-shadow:0 0 0 6px rgba(34,211,238,0)}}}}

.hero-title {{
    font-size:36px; font-weight:900; line-height:1.1;
    color:var(--t1); margin:0 0 10px; letter-spacing:-.02em;
}}
.hero-hl {{
    background:linear-gradient(90deg,var(--teal),#818cf8);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}}
.hero-sub {{ font-size:16px; color:var(--t2); max-width:560px; line-height:1.6; margin:0; }}

/* Metric cards */
.metric-row {{ animation:fadeUp .5s .15s both; }}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:translateY(0)}}}}

.mc {{
    background:var(--card); border:1px solid var(--border);
    border-radius:16px; padding:20px 22px;
    transition:all .3s ease; cursor:default;
    box-shadow:0 4px 20px rgba(0,0,0,0.3);
    animation:fadeUp .5s both;
}}
.mc:hover {{
    background:var(--card2); border-color:rgba(34,211,238,0.25);
    transform:translateY(-4px); box-shadow:0 12px 40px rgba(0,0,0,0.4),0 0 30px var(--glow-c);
}}
.mc-ico {{ font-size:24px; margin-bottom:10px; }}
.mc-val {{
    font-family:'Outfit',sans-serif; font-size:22px; font-weight:800;
    color:var(--t1); margin:2px 0 4px; letter-spacing:-.01em;
}}
.mc-lbl {{ font-size:11px; color:var(--t3); text-transform:uppercase; letter-spacing:.08em; font-weight:600; }}

/* Section header */
.sec-hdr {{
    display:flex; align-items:center; gap:12px; margin-bottom:20px;
    animation:fadeUp .5s .25s both;
}}
.sec-hdr-line {{
    flex:1; height:1px;
    background:linear-gradient(90deg,rgba(34,211,238,0.3),transparent);
}}
.sec-hdr-text {{
    font-size:12px; font-weight:700; color:var(--teal);
    letter-spacing:.12em; text-transform:uppercase;
}}
.sec-hdr-ico {{ font-size:18px; }}

/* Input card */
.inp-card {{
    background:var(--card); border:1px solid var(--border);
    border-radius:18px; padding:26px 28px;
    box-shadow:0 8px 32px rgba(0,0,0,0.3),inset 0 1px 0 rgba(255,255,255,0.04);
    backdrop-filter:blur(12px); animation:fadeUp .5s .3s both;
    transition:border-color .3s;
}}
.inp-card:hover {{ border-color:rgba(34,211,238,0.15); }}

.inp-grp-lbl {{
    font-size:11px; font-weight:700; color:var(--t3);
    letter-spacing:.1em; text-transform:uppercase;
    padding:6px 0 12px; border-bottom:1px solid var(--border);
    margin-bottom:16px; display:flex; align-items:center; gap:8px;
}}

.inp-hint {{
    font-size:11px; color:var(--t3); margin-top:3px;
    font-style:italic; padding-left:2px;
}}

/* Warning box */
.inp-warn {{
    background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.25);
    border-left:3px solid var(--amber); border-radius:8px;
    padding:8px 12px; font-size:12px; color:var(--amber);
    margin-top:6px; display:flex; align-items:center; gap:6px;
}}
.inp-ok {{
    background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.15);
    border-left:3px solid var(--green); border-radius:8px;
    padding:8px 12px; font-size:12px; color:var(--green);
    margin-top:6px; display:flex; align-items:center; gap:6px;
}}

/* Live risk indicator */
.live-panel {{
    background:var(--card); border:1px solid var(--border);
    border-radius:14px; padding:16px 20px;
    display:flex; align-items:center; justify-content:space-between;
    margin-bottom:20px; animation:fadeUp .5s .35s both;
    transition:border-color .4s, box-shadow .4s;
}}
.live-dot {{
    width:8px; height:8px; border-radius:50%;
    animation:dot-blink 1.4s ease-in-out infinite;
    display:inline-block; margin-right:8px;
}}
.live-label {{
    font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:var(--t3);
}}
.live-val {{
    font-family:'JetBrains Mono',monospace; font-size:18px; font-weight:700; color:var(--t1);
}}

/* Result panel */
.result-panel {{
    border-radius:20px; padding:36px 40px; text-align:center;
    animation:resultReveal .65s cubic-bezier(.16,1,.3,1) both;
    position:relative; overflow:hidden;
    margin-top:4px;
}}
@keyframes resultReveal{{
    from{{opacity:0;transform:translateY(28px) scale(.97)}}
    to{{opacity:1;transform:translateY(0) scale(1)}}
}}
.result-neg {{
    background:linear-gradient(135deg,rgba(244,63,94,0.1),rgba(244,63,94,0.05));
    border:1px solid rgba(244,63,94,0.35);
    box-shadow:0 0 80px rgba(244,63,94,0.1),inset 0 1px 0 rgba(255,255,255,0.04);
}}
.result-pos {{
    background:linear-gradient(135deg,rgba(16,185,129,0.1),rgba(16,185,129,0.04));
    border:1px solid rgba(16,185,129,0.35);
    box-shadow:0 0 80px rgba(16,185,129,0.1),inset 0 1px 0 rgba(255,255,255,0.04);
}}
.result-ico {{ font-size:56px; margin-bottom:12px; }}
.result-title {{
    font-family:'Outfit',sans-serif; font-size:30px; font-weight:900;
    letter-spacing:-.02em; margin-bottom:8px;
}}
.result-sub {{ font-size:15px; color:var(--t2); max-width:400px; margin:0 auto 20px; line-height:1.65; }}
.result-badge {{
    display:inline-block; padding:5px 18px; border-radius:99px;
    font-size:12px; font-weight:700; letter-spacing:.08em; text-transform:uppercase;
    margin-bottom:24px;
}}

/* Empty state */
.empty-state {{
    background:var(--card); border:1px solid var(--border);
    border-radius:20px; padding:52px; text-align:center;
    animation:fadeUp .6s both;
}}
.empty-ico {{ font-size:48px; margin-bottom:16px; opacity:.5; }}
.empty-title {{ font-size:18px; font-weight:700; color:var(--t2); margin-bottom:6px; }}
.empty-sub {{ font-size:14px; color:var(--t3); line-height:1.6; }}

/* History table */
.hist-row {{
    display:flex; align-items:center; gap:12px;
    padding:10px 14px; border-radius:10px;
    background:var(--card); border:1px solid var(--border);
    margin-bottom:6px; font-size:13px; color:var(--t2);
    transition:background .2s;
}}
.hist-row:hover {{ background:var(--card2); }}
.hist-badge-pos {{
    padding:3px 10px; border-radius:99px; font-size:11px; font-weight:700;
    background:rgba(16,185,129,0.15); color:var(--green);
    border:1px solid rgba(16,185,129,0.3);
}}
.hist-badge-neg {{
    padding:3px 10px; border-radius:99px; font-size:11px; font-weight:700;
    background:rgba(244,63,94,0.15); color:var(--rose);
    border:1px solid rgba(244,63,94,0.3);
}}
.hist-time {{ font-family:'JetBrains Mono',monospace; font-size:11px; color:var(--t3); margin-left:auto; }}

/* Summary card */
.sum-card {{
    background:var(--card); border:1px solid var(--border);
    border-radius:14px; padding:18px 20px; margin-bottom:14px;
    animation:fadeUp .5s both;
}}
.sum-item {{
    display:flex; justify-content:space-between; align-items:center;
    padding:7px 0; border-bottom:1px solid var(--border); font-size:13px;
}}
.sum-item:last-child {{ border-bottom:none; }}
.sum-key {{ color:var(--t3); font-weight:500; }}
.sum-val {{ font-family:'JetBrains Mono',monospace; color:var(--t1); font-weight:600; }}

/* Sidebar specific */
.sb-logo {{
    display:flex; align-items:center; gap:10px;
    padding-bottom:18px; border-bottom:1px solid var(--border); margin-bottom:20px;
}}
.sb-name {{
    font-family:'Outfit',sans-serif !important; font-size:17px !important;
    font-weight:800 !important; color:{T['t1']} !important; letter-spacing:-.01em;
}}
.sb-sec {{ margin-bottom:24px; }}
.sb-sh {{
    font-size:10px !important; letter-spacing:.14em !important;
    text-transform:uppercase !important;
    color:rgba(148,163,184,0.4) !important;
    font-weight:700 !important; margin-bottom:10px !important; display:block;
}}
.sb-item {{
    display:flex; align-items:flex-start; gap:10px; padding:9px 12px;
    border-radius:10px; margin-bottom:3px; font-size:13px !important;
    color:var(--t2) !important; cursor:default; transition:background .2s;
}}
.sb-item:hover {{ background:rgba(255,255,255,0.04); }}
.sb-item-ico {{ font-size:15px; margin-top:1px; flex-shrink:0; }}
.sb-item-key {{ font-size:11px; color:var(--t3) !important; letter-spacing:.04em; }}
.sb-item-val {{ font-size:13px; color:{T['t1']} !important; font-weight:600; }}
.sb-ref-row {{
    display:flex; justify-content:space-between; padding:7px 0;
    border-bottom:1px solid var(--border); font-size:12px !important;
}}
.sb-ref-lbl {{ color:var(--t3) !important; }}
.sb-ref-val {{ font-family:'JetBrains Mono',monospace; color:var(--teal) !important; font-weight:600; }}
.sb-disc {{
    background:rgba(245,158,11,0.06); border:1px solid rgba(245,158,11,0.15);
    border-left:3px solid var(--amber); border-radius:8px;
    padding:10px 12px; font-size:11px !important;
    color:rgba(245,158,11,0.8) !important; line-height:1.6;
}}

/* Explainability bar */
.exp-bar-wrap {{ margin-bottom:10px; }}
.exp-bar-label {{
    display:flex; justify-content:space-between; font-size:12px;
    color:var(--t2); margin-bottom:4px; font-weight:500;
}}
.exp-bar-track {{
    height:8px; background:rgba(255,255,255,0.06);
    border-radius:99px; overflow:hidden;
}}
.exp-bar-fill {{
    height:100%; border-radius:99px;
    background:linear-gradient(90deg,var(--teal),var(--cyan));
    transition:width 1s cubic-bezier(.16,1,.3,1);
}}

/* Footer */
.footer {{
    text-align:center; padding:28px 0 12px;
    border-top:1px solid var(--border); margin-top:36px;
}}
.footer-brand {{
    font-family:'Outfit',sans-serif; font-size:14px; font-weight:700;
    color:var(--t2);
}}
.footer-hl {{
    background:linear-gradient(90deg,var(--teal),#818cf8);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}}
.footer-sub {{ font-size:12px; color:var(--t3); margin-top:5px; }}

/* PDF btn override */
div[data-testid="stDownloadButton"]>button {{
    background:rgba(255,255,255,0.05) !important;
    border:1px solid var(--border) !important;
    color:var(--t2) !important;
    font-size:13px !important; padding:8px 18px !important;
    border-radius:10px !important; width:auto !important;
    box-shadow:none !important; text-transform:none !important;
    letter-spacing:normal !important;
    transition:all .25s !important;
}}
div[data-testid="stDownloadButton"]>button:hover {{
    background:rgba(34,211,238,0.08) !important;
    border-color:rgba(34,211,238,0.3) !important;
    color:var(--teal) !important; transform:translateY(-2px) !important;
    box-shadow:none !important;
}}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  LOAD MODEL
# ═══════════════════════════════════════════════════════════════
model_path = os.path.join(os.path.dirname(__file__), "trained_model.sav")
if not os.path.exists(model_path):
    st.error("❌ trained_model.sav not found in app directory.")
    st.stop()
with open(model_path, "rb") as f:
    model = pickle.load(f)

# ═══════════════════════════════════════════════════════════════
#  PREDICTION FUNCTION  (unchanged logic)
# ═══════════════════════════════════════════════════════════════
def predict_diabetes(data):
    arr = np.asarray(data, dtype=float).reshape(1, -1)
    pred = model.predict(arr)[0]
    try:
        proba = model.predict_proba(arr)[0]
        confidence = max(proba) * 100
        risk_prob = proba[1] * 100 if len(proba) > 1 else (confidence if pred == 1 else 100 - confidence)
    except Exception:
        confidence = None
        risk_prob = None
    label = "Diabetic" if pred == 1 else "Not Diabetic"
    return label, confidence, risk_prob

# ═══════════════════════════════════════════════════════════════
#  HELPER — PURE CSS/SVG GAUGE (no plotly dependency)
# ═══════════════════════════════════════════════════════════════
def make_gauge_html(value: float) -> str:
    """Render a semicircular SVG arc gauge with zone colouring."""
    # clamp
    v = max(0.0, min(float(value), 100.0))

    # arc geometry  (semicircle, r=80, cx=100, cy=100)
    cx, cy, r = 100, 100, 78
    import math
    def polar(deg):
        rad = math.radians(deg)
        return cx + r * math.cos(rad), cy + r * math.sin(rad)

    # 180° sweep from 180° → 0°  (left → right along top)
    # map value 0-100 → angle 180° → 0°
    angle = 180 - (v / 100.0) * 180   # degrees from left
    nx, ny = polar(angle)

    # zone arc colours (green 0-40, amber 40-70, red 70-100)
    def arc_path(a1, a2, col, opa):
        x1, y1 = polar(180 - a1 / 100 * 180)
        x2, y2 = polar(180 - a2 / 100 * 180)
        large = 1 if (a2 - a1) > 50 else 0
        return (f'<path d="M {x1:.2f} {y1:.2f} A {r} {r} 0 {large} 1 {x2:.2f} {y2:.2f}" '
                f'fill="none" stroke="{col}" stroke-width="14" '
                f'stroke-opacity="{opa}" stroke-linecap="round"/>')

    # needle
    nlen = r - 10
    nx2 = cx + nlen * math.cos(math.radians(angle))
    ny2 = cy + nlen * math.sin(math.radians(angle))

    # colour of value text
    if v < 40:
        txt_col = "#10b981"
    elif v < 70:
        txt_col = "#f59e0b"
    else:
        txt_col = "#f43f5e"

    svg = f"""
    <div style="text-align:center;padding:8px 0 0;">
      <svg viewBox="20 20 160 100" width="100%" style="max-width:220px;overflow:visible;">
        <!-- track -->
        <path d="M 22 100 A 78 78 0 0 1 178 100"
              fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="14" stroke-linecap="round"/>
        <!-- zones -->
        {arc_path(0,  40, '#10b981', '0.55')}
        {arc_path(40, 70, '#f59e0b', '0.55')}
        {arc_path(70,100, '#f43f5e', '0.55')}
        <!-- needle -->
        <line x1="{cx}" y1="{cy}"
              x2="{nx2:.2f}" y2="{ny2:.2f}"
              stroke="#22d3ee" stroke-width="2.5" stroke-linecap="round"/>
        <!-- pivot -->
        <circle cx="{cx}" cy="{cy}" r="5" fill="#22d3ee"/>
        <!-- value text -->
        <text x="{cx}" y="92" text-anchor="middle"
              font-family="Outfit,sans-serif" font-size="18" font-weight="900"
              fill="{txt_col}">{v:.0f}%</text>
        <text x="{cx}" y="110" text-anchor="middle"
              font-family="Outfit,sans-serif" font-size="7" font-weight="600"
              fill="rgba(148,163,184,0.6)" letter-spacing="1">RISK SCORE</text>
      </svg>
      <div style="display:flex;justify-content:center;gap:14px;font-size:10px;
                  font-weight:700;letter-spacing:.05em;margin-top:2px;">
        <span style="color:#10b981;">● LOW</span>
        <span style="color:#f59e0b;">● MOD</span>
        <span style="color:#f43f5e;">● HIGH</span>
      </div>
    </div>
    """
    return svg

# ═══════════════════════════════════════════════════════════════
#  HELPER — LIVE RISK ESTIMATE (heuristic, model-agnostic)
# ═══════════════════════════════════════════════════════════════
def live_risk_estimate(pregnancies, glucose, bp, skin, insulin, bmi, pedigree, age):
    score = 0
    if glucose > 140:  score += 30
    elif glucose > 100: score += 15
    if bmi > 30:       score += 20
    elif bmi > 25:     score += 10
    if age > 50:       score += 15
    elif age > 35:     score += 8
    if pregnancies > 4: score += 10
    if pedigree > 0.8:  score += 15
    elif pedigree > 0.4: score += 7
    if insulin > 200:   score += 10
    if bp > 90:         score += 5
    return min(score, 95)

# ═══════════════════════════════════════════════════════════════
#  HELPER — PDF REPORT (plain text with formatting)
# ═══════════════════════════════════════════════════════════════
def generate_report(inputs: dict, result: str, confidence, risk_prob, ts: str) -> str:
    conf_str = f"{confidence:.1f}%" if confidence else "N/A"
    risk_str = f"{risk_prob:.1f}%" if risk_prob else "N/A"
    lines = [
        "═" * 60,
        "   HEMASCOPE AI · CLINICAL SCREENING REPORT",
        "═" * 60,
        f"  Generated : {ts}",
        f"  System    : Diabetes Risk Assessment v2.0",
        "═" * 60,
        "",
        "  PATIENT BIOMARKERS",
        "  " + "─" * 40,
    ]
    for k, v in inputs.items():
        lines.append(f"  {k:<32} {v}")
    lines += [
        "",
        "  PREDICTION OUTCOME",
        "  " + "─" * 40,
        f"  Diagnosis Estimate    : {result}",
        f"  Model Confidence      : {conf_str}",
        f"  Risk Probability      : {risk_str}",
        "",
        "  CLINICAL DISCLAIMER",
        "  " + "─" * 40,
        "  This report is generated by a machine learning model",
        "  trained on the PIMA Indian Diabetes Dataset. It is",
        "  intended for EDUCATIONAL purposes only and must NOT",
        "  be used as a substitute for professional medical",
        "  diagnosis or clinical decision-making.",
        "",
        "═" * 60,
        "  Developed by Kartvaya Raikwar | ML Research Project",
        "═" * 60,
    ]
    return "\n".join(lines)

# ═══════════════════════════════════════════════════════════════
#  FEATURE IMPORTANCE (model-agnostic fallback)
# ═══════════════════════════════════════════════════════════════
FEATURE_NAMES = ["Pregnancies","Glucose","Blood Pressure","Skin Thickness",
                 "Insulin","BMI","Pedigree Fn.","Age"]

def get_feature_importance():
    try:
        if hasattr(model, "feature_importances_"):
            fi = model.feature_importances_
            fi = fi / fi.sum() * 100
            return list(zip(FEATURE_NAMES, fi.tolist()))
        if hasattr(model, "coef_"):
            fi = np.abs(model.coef_[0])
            fi = fi / fi.sum() * 100
            return list(zip(FEATURE_NAMES, fi.tolist()))
    except Exception:
        pass
    # Fallback: domain-knowledge based importance
    fi = [8, 28, 7, 6, 10, 18, 12, 11]
    total = sum(fi)
    return list(zip(FEATURE_NAMES, [v/total*100 for v in fi]))

# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div class='sb-logo'>
        <span style='font-size:28px'>🩸</span>
        <span class='sb-name'>HemaScope AI</span>
    </div>
    """, unsafe_allow_html=True)

    # Theme toggle
    st.markdown("<span class='sb-sh'>Interface Theme</span>", unsafe_allow_html=True)
    theme_choice = st.radio("", ["🌑 Dark", "☀️ Light"], index=0 if IS_DARK else 1, label_visibility="collapsed")
    if ("Dark" in theme_choice and st.session_state.theme != "dark") or \
       ("Light" in theme_choice and st.session_state.theme != "light"):
        st.session_state.theme = "dark" if "Dark" in theme_choice else "light"
        st.rerun()

    st.markdown("<div class='sb-sec'>", unsafe_allow_html=True)
    st.markdown("<span class='sb-sh'>System Info</span>", unsafe_allow_html=True)
    info_items = [
        ("🤖", "Model", "PIMA Diabetes Classifier"),
        ("🎯", "Task", "Binary Classification"),
        ("🧬", "Features", "8 Blood Biomarkers"),
        ("📊", "Output", "Diabetic / Not Diabetic"),
        ("⚡", "Inference", "< 1 ms"),
    ]
    for ico, key, val in info_items:
        st.markdown(f"""
        <div class='sb-item'>
            <span class='sb-item-ico'>{ico}</span>
            <div>
                <div class='sb-item-key'>{key}</div>
                <div class='sb-item-val'>{val}</div>
            </div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sb-sec'>", unsafe_allow_html=True)
    st.markdown("<span class='sb-sh'>Clinical Reference Ranges</span>", unsafe_allow_html=True)
    refs = [
        ("Glucose","70–140 mg/dL"),("Blood Pressure","60–80 mmHg"),
        ("BMI","18.5–24.9"),("Insulin","16–166 μU/mL"),
        ("Skin Fold","10–50 mm"),("Age","—"),
    ]
    for lbl, rng in refs:
        st.markdown(f"""
        <div class='sb-ref-row'>
            <span class='sb-ref-lbl'>{lbl}</span>
            <span class='sb-ref-val'>{rng}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='sb-disc'>
        ⚠️ Educational use only. This tool does not constitute medical advice. 
        Always consult a qualified physician for clinical decisions.
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:11px;color:{T['t3']};text-align:center;margin-top:18px;'>
        v2.0 · Kartvaya Raikwar
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  HERO HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class='hero-card'>
    <div class='badge-clinical'>Clinical Screening System</div>
    <div class='hero-title'>
        Diabetes <span class='hero-hl'>Risk Assessment</span><br>Dashboard
    </div>
    <p class='hero-sub'>
        Enter patient blood biomarkers below for instant AI-powered diabetes risk stratification.
        Results are generated by a model trained on the PIMA Indian Diabetes Dataset.
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  METRIC CARDS
# ═══════════════════════════════════════════════════════════════
mc1, mc2, mc3, mc4 = st.columns(4)
mdata = [
    ("🧬","8","Blood Biomarkers",".15s"),
    ("🤖","ML","Classification Model",".2s"),
    ("🎯","Binary","Output Classes",".25s"),
    ("⚡","<1ms","Response Time",".3s"),
]
for col, (ico, val, lbl, delay) in zip([mc1,mc2,mc3,mc4], mdata):
    with col:
        st.markdown(f"""
        <div class='mc' style='animation-delay:{delay}'>
            <div class='mc-ico'>{ico}</div>
            <div class='mc-val'>{val}</div>
            <div class='mc-lbl'>{lbl}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  INPUT FORM
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class='sec-hdr'>
    <span class='sec-hdr-ico'>🩸</span>
    <span class='sec-hdr-text'>Blood Biomarkers — Patient Data Entry</span>
    <div class='sec-hdr-line'></div>
</div>""", unsafe_allow_html=True)

left_col, right_col = st.columns(2, gap="large")

with left_col:
    st.markdown("""
    <div class='inp-card'>
        <div class='inp-grp-lbl'>🔬 Primary Markers</div>
    </div>""", unsafe_allow_html=True)

    pregnancies = st.number_input("👶  Pregnancies", min_value=0, max_value=20, value=0, step=1,
                                  help="Total number of pregnancies")
    glucose = st.number_input("🩸  Plasma Glucose (mg/dL)", min_value=0, max_value=300, value=100,
                              help="2-hr plasma glucose · Normal: 70–140 mg/dL")
    if glucose > 200:
        st.markdown("<div class='inp-warn'>⚠️ Critically high glucose — verify reading</div>", unsafe_allow_html=True)
    elif glucose > 140:
        st.markdown("<div class='inp-warn'>⚠️ Above normal range (>140 mg/dL)</div>", unsafe_allow_html=True)
    elif glucose >= 70:
        st.markdown("<div class='inp-ok'>✓ Within normal range</div>", unsafe_allow_html=True)

    blood_pressure = st.number_input("💓  Diastolic BP (mmHg)", min_value=0, max_value=200, value=70,
                                     help="Diastolic blood pressure · Normal: 60–80 mmHg")
    if blood_pressure > 100:
        st.markdown("<div class='inp-warn'>⚠️ High diastolic pressure (>100 mmHg)</div>", unsafe_allow_html=True)

    skin_thickness = st.number_input("📏  Skin Fold Thickness (mm)", min_value=0, max_value=100, value=20,
                                     help="Triceps skin fold · Normal: 10–50 mm")

with right_col:
    st.markdown("""
    <div class='inp-card'>
        <div class='inp-grp-lbl'>📐 Secondary Markers</div>
    </div>""", unsafe_allow_html=True)

    insulin = st.number_input("💉  2-Hr Serum Insulin (μU/mL)", min_value=0, max_value=900, value=80,
                              help="Serum insulin · Normal: 16–166 μU/mL")
    if insulin > 300:
        st.markdown("<div class='inp-warn'>⚠️ Very high insulin level</div>", unsafe_allow_html=True)

    bmi = st.number_input("⚖️  Body Mass Index (kg/m²)", min_value=0.0, max_value=70.0, value=25.0, step=0.1,
                          help="BMI · Normal: 18.5–24.9")
    if bmi > 35:
        st.markdown("<div class='inp-warn'>⚠️ Obese Class II+ (BMI > 35)</div>", unsafe_allow_html=True)
    elif bmi > 25:
        st.markdown("<div class='inp-warn'>⚠️ Overweight range (BMI > 25)</div>", unsafe_allow_html=True)
    elif bmi >= 18.5:
        st.markdown("<div class='inp-ok'>✓ Healthy BMI range</div>", unsafe_allow_html=True)

    pedigree = st.number_input("🧬  Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.47, step=0.01,
                               help="Hereditary risk score · Range: 0.08–2.42")
    age = st.number_input("🗓️  Age (years)", min_value=1, max_value=120, value=30,
                          help="Patient age in years")
    if age > 60:
        st.markdown("<div class='inp-warn'>⚠️ Elevated age risk factor (>60)</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  LIVE RISK PREVIEW
# ═══════════════════════════════════════════════════════════════
live_score = live_risk_estimate(pregnancies, glucose, blood_pressure,
                                skin_thickness, insulin, bmi, pedigree, age)
if live_score < 30:
    live_col, live_label_text, live_bg = "#10b981", "LOW RISK ZONE", "rgba(16,185,129,0.08)"
    live_border = "rgba(16,185,129,0.25)"
elif live_score < 60:
    live_col, live_label_text, live_bg = "#f59e0b", "MODERATE RISK ZONE", "rgba(245,158,11,0.08)"
    live_border = "rgba(245,158,11,0.25)"
else:
    live_col, live_label_text, live_bg = "#f43f5e", "ELEVATED RISK ZONE", "rgba(244,63,94,0.08)"
    live_border = "rgba(244,63,94,0.25)"

st.markdown(f"""
<div class='live-panel' style='background:{live_bg};border-color:{live_border};'>
    <div style='display:flex;align-items:center;'>
        <span class='live-dot' style='background:{live_col};box-shadow:0 0 0 3px {live_col}33;'></span>
        <div>
            <div class='live-label'>Live Risk Preview</div>
            <div style='font-size:13px;color:{live_col};font-weight:700;letter-spacing:.04em;'>{live_label_text}</div>
        </div>
    </div>
    <div>
        <div class='live-val' style='color:{live_col};'>{live_score}%</div>
        <div style='font-size:10px;color:var(--t3);text-align:right;'>heuristic estimate</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  PREDICT BUTTON
# ═══════════════════════════════════════════════════════════════
_, btn_mid, _ = st.columns([1, 2, 1])
with btn_mid:
    clicked = st.button("🔬  Analyze Clinical Risk Profile", use_container_width=True)

# ═══════════════════════════════════════════════════════════════
#  PREDICTION EXECUTION
# ═══════════════════════════════════════════════════════════════
if clicked:
    data = [pregnancies, glucose, blood_pressure, skin_thickness,
            insulin, bmi, pedigree, age]
    with st.spinner("Running clinical analysis…"):
        time.sleep(0.85)
    result, confidence, risk_prob = predict_diabetes(data)
    st.session_state.result = result
    st.session_state.confidence = confidence
    st.session_state.risk_prob = risk_prob
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.last_inputs = {
        "Pregnancies": pregnancies,
        "Glucose (mg/dL)": glucose,
        "Blood Pressure (mmHg)": blood_pressure,
        "Skin Thickness (mm)": skin_thickness,
        "Insulin (μU/mL)": insulin,
        "BMI": f"{bmi:.1f}",
        "Pedigree Fn.": f"{pedigree:.2f}",
        "Age (yrs)": age,
    }
    conf_disp = f"{confidence:.1f}%" if confidence else "N/A"
    st.session_state.history.insert(0, {
        "ts": ts, "result": result,
        "confidence": conf_disp,
        "glucose": glucose, "bmi": f"{bmi:.1f}", "age": age
    })
    if len(st.session_state.history) > 10:
        st.session_state.history = st.session_state.history[:10]

# ═══════════════════════════════════════════════════════════════
#  RESULT DISPLAY
# ═══════════════════════════════════════════════════════════════
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

if st.session_state.result is None:
    # Empty state
    st.markdown("""
    <div class='empty-state'>
        <div class='empty-ico'>🔬</div>
        <div class='empty-title'>Awaiting Patient Data</div>
        <div class='empty-sub'>
            Enter blood biomarker values above and click<br>
            <strong style='color:var(--teal)'>Analyze Clinical Risk Profile</strong>
            to generate your assessment.
        </div>
    </div>""", unsafe_allow_html=True)
else:
    result     = st.session_state.result
    confidence = st.session_state.confidence
    risk_prob  = st.session_state.get("risk_prob", None)
    is_diabetic = result == "Diabetic"

    panel_cls = "result-neg" if is_diabetic else "result-pos"
    ico       = "⚠️" if is_diabetic else "✅"
    color     = T["rose"] if is_diabetic else T["green"]
    badge_bg  = "rgba(244,63,94,0.15)" if is_diabetic else "rgba(16,185,129,0.15)"
    badge_bd  = "rgba(244,63,94,0.4)"  if is_diabetic else "rgba(16,185,129,0.4)"
    sub_msg   = (
        "Elevated markers suggest positive diabetes screening. "
        "Clinical confirmation and specialist consultation are strongly recommended."
        if is_diabetic else
        "Biomarkers fall within lower-risk parameters. Maintain healthy lifestyle "
        "practices and schedule routine follow-up assessments."
    )
    conf_val = (confidence / 100.0) if confidence else 0.0

    # Result panel
    st.markdown(f"""
    <div class='result-panel {panel_cls}'>
        <div class='result-ico'>{ico}</div>
        <div style='display:inline-block;padding:4px 16px;border-radius:99px;
             background:{badge_bg};border:1px solid {badge_bd};
             font-size:11px;font-weight:700;letter-spacing:.1em;
             text-transform:uppercase;color:{color};margin-bottom:12px;'>
            {"HIGH RISK · DIABETIC" if is_diabetic else "LOW RISK · NON-DIABETIC"}
        </div>
        <div class='result-title' style='color:{color};'>{result}</div>
        <div class='result-sub'>{sub_msg}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Gauge + Confidence + Summary
    g_col, c_col, s_col = st.columns([1.2, 1, 1.2])

    with g_col:
        gauge_val = risk_prob if risk_prob is not None else (confidence if confidence else 50.0)
        st.markdown(f"""
        <div style='background:var(--card);border:1px solid var(--border);
             border-radius:16px;padding:18px 12px 12px;text-align:center;'>
            <div style='font-size:11px;font-weight:700;letter-spacing:.1em;
                 text-transform:uppercase;color:var(--t3);margin-bottom:4px;'>Risk Gauge</div>
            {make_gauge_html(gauge_val)}
        </div>""", unsafe_allow_html=True)

    with c_col:
        st.markdown(f"""
        <div style='background:var(--card);border:1px solid var(--border);
             border-radius:16px;padding:22px 20px;height:100%;'>
            <div style='font-size:11px;font-weight:700;letter-spacing:.1em;
                 text-transform:uppercase;color:var(--t3);margin-bottom:18px;'>Confidence</div>
        """, unsafe_allow_html=True)
        conf_pct = f"{confidence:.1f}%" if confidence else "N/A"
        st.markdown(f"""
            <div style='font-family:Outfit,sans-serif;font-size:42px;font-weight:900;
                 color:{color};text-align:center;margin:12px 0;'>{conf_pct}</div>
            <div style='font-size:12px;color:var(--t3);text-align:center;margin-bottom:16px;'>
                Model certainty
            </div>
        """, unsafe_allow_html=True)
        st.progress(conf_val)
        certainty = "High" if conf_val > 0.8 else "Moderate" if conf_val > 0.6 else "Low"
        st.markdown(f"""
            <div style='font-size:11px;color:var(--t3);text-align:center;margin-top:6px;'>
                {certainty} certainty zone
            </div>
        </div>""", unsafe_allow_html=True)

    with s_col:
        inputs = st.session_state.last_inputs
        st.markdown("""
        <div style='background:var(--card);border:1px solid var(--border);
             border-radius:16px;padding:22px 20px;'>
            <div style='font-size:11px;font-weight:700;letter-spacing:.1em;
                 text-transform:uppercase;color:var(--t3);margin-bottom:14px;'>Patient Summary</div>
        <div class='sum-card' style='background:transparent;border:none;padding:0;'>
        """, unsafe_allow_html=True)
        for k, v in list(inputs.items())[:6]:
            st.markdown(f"""
            <div class='sum-item'>
                <span class='sum-key'>{k}</span>
                <span class='sum-val'>{v}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    # Confidence bar for progress animation
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Model Explainability ──────────────────────────────────
    st.markdown("""
    <div class='sec-hdr' style='margin-top:8px;'>
        <span class='sec-hdr-ico'>📊</span>
        <span class='sec-hdr-text'>Feature Contribution Analysis</span>
        <div class='sec-hdr-line'></div>
    </div>""", unsafe_allow_html=True)

    fi_data = get_feature_importance()
    fi_data_sorted = sorted(fi_data, key=lambda x: x[1], reverse=True)

    exp_col1, exp_col2 = st.columns(2)
    for i, (fname, fval) in enumerate(fi_data_sorted):
        col = exp_col1 if i % 2 == 0 else exp_col2
        with col:
            width = min(fval, 100)
            st.markdown(f"""
            <div class='exp-bar-wrap'>
                <div class='exp-bar-label'>
                    <span>{fname}</span>
                    <span style='font-family:JetBrains Mono,monospace;'>{fval:.1f}%</span>
                </div>
                <div class='exp-bar-track'>
                    <div class='exp-bar-fill' style='width:{width}%;'></div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── PDF Download ──────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    ts_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_text = generate_report(
        st.session_state.last_inputs, result, confidence,
        risk_prob, ts_now
    )
    dl_col1, dl_col2, dl_col3 = st.columns([1, 1, 1])
    with dl_col2:
        st.download_button(
            label="📄  Download Clinical Report (.txt)",
            data=report_text,
            file_name=f"hemascope_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

# ═══════════════════════════════════════════════════════════════
#  RISK HISTORY
# ═══════════════════════════════════════════════════════════════
if st.session_state.history:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='sec-hdr'>
        <span class='sec-hdr-ico'>🗂️</span>
        <span class='sec-hdr-text'>Session Risk History</span>
        <div class='sec-hdr-line'></div>
    </div>""", unsafe_allow_html=True)

    for entry in st.session_state.history[:5]:
        is_bad = entry["result"] == "Diabetic"
        badge_cls = "hist-badge-neg" if is_bad else "hist-badge-pos"
        badge_txt = "DIABETIC" if is_bad else "CLEAR"
        st.markdown(f"""
        <div class='hist-row'>
            <span>{'⚠️' if is_bad else '✅'}</span>
            <span class='{badge_cls}'>{badge_txt}</span>
            <span style='color:var(--t2);font-size:13px;'>
                Glucose: <strong>{entry['glucose']}</strong> ·
                BMI: <strong>{entry['bmi']}</strong> ·
                Age: <strong>{entry['age']}</strong>
            </span>
            <span style='margin-left:auto;font-family:JetBrains Mono,monospace;
                 font-size:11px;color:var(--t3);'>{entry['confidence']}</span>
            <span class='hist-time'>{entry['ts']}</span>
        </div>""", unsafe_allow_html=True)

    if st.button("🗑️  Clear History", key="clear_hist"):
        st.session_state.history = []
        st.rerun()

# ═══════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class='footer'>
    <div class='footer-brand'>
        🩸 <span class='footer-hl'>HemaScope AI</span>
        · Diabetes Risk Assessment Platform
    </div>
    <div class='footer-sub'>
        Developed by Kartvaya Raikwar · Machine Learning Research Project ·
        PIMA Indian Diabetes Dataset · For educational use only.
    </div>
</div>""", unsafe_allow_html=True)
