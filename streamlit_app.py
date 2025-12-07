# app.py
import streamlit as st
from datetime import date, datetime

# ---------------------------
# Minimal styling to keep clean UI
# ---------------------------
st.set_page_config(page_title="Campaign UI", page_icon="🧭", layout="centered")

st.markdown(
    """
    <style>
    /* Page background & container */
    .stApp {
        background-color: #ffffff;
        color: #111111;
    }
    /* Center main content and constrain width */
    .main-container {
        max-width: 1100px;
        margin-left: auto;
        margin-right: auto;
        padding-top: 30px;
        padding-bottom: 30px;
    }
    /* Headings */
    .landing-title {font-size:34px; font-weight:700; margin-bottom:6px;}
    .landing-sub {font-size:16px; color:#6b6b6b; margin-bottom:18px;}
    /* Inputs look */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, textarea {
        border-radius: 8px;
        border: 1px solid #e6e6e6;
        padding: 10px 12px;
    }
    .section-box {
        padding:16px;
        border-radius:10px;
        border:1px solid #f0f0f0;
        background: #ffffff;
    }
    .section-title {font-size:16px; font-weight:600; margin-bottom:8px;}
    .muted {color:#808080; font-size:13px;}
    .footer-text {color:#9a9a9a; font-size:13px; text-align:center; padding-top:20px; padding-bottom:20px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Simple navigation using session_state
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "rules" not in st.session_state:
    st.session_state.rules = []  # list of dicts: {name, condition, action, active}

# ---------------------------
# Helper: navigate
# ---------------------------
def go_to_main():
    st.session_state.page = "main"

# ---------------------------
# PAGE 1: Landing
# ---------------------------
def page_landing():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center">', unsafe_allow_html=True)

    st.markdown('<div class="landing-title">Spark Your Creativity with AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="landing-sub">Unleash your content genius with a clean and simple workflow.</div>', unsafe_allow_html=True)

    # Centered Start button
    start_clicked = st.button("Start", key="start_button")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if start_clicked:
        go_to_main()

# ---------------------------
# PAGE 2: Campaign Settings
# ---------------------------
def page_main():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Page title
    st.markdown('<div style="display:flex; align-items:center; justify-content:space-between;">'
                '<h2 style="margin:0">Campaign Settings</h2>'
                '</div>', unsafe_allow_html=True)
    st.caption("Configure campaign details, audience, schedule, and rules.")

    st.write("")  # spacer

    # -----------------------
    # SECTION 1: Main Details
    # -----------------------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Main Details</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        campaign_name = st.text_input("Campaign name", placeholder="Taste the Future: Frozen Delights Delivered", max_chars=100)
    with col2:
        brand = st.text_input("Brand", placeholder="Damory Food Indonesia")

    st.write("")  # small gap
    channels = st.multiselect("Channel", options=["Instagram", "Google Ads", "Facebook", "YouTube", "Twitter"], default=["Instagram"])
    description = st.text_area("Description", placeholder="A social media and Google Ads campaign showcasing Damory Food Indonesia's frozen product line...", height=120)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")  # gap between sections

    # -----------------------
    # SECTION 2: Audience
    # -----------------------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Audience</div>', unsafe_allow_html=True)

    a_col1, a_col2, a_col3, a_col4 = st.columns([1,1,1,1])
    with a_col1:
        target_customers = st.number_input("Target customers", min_value=0, step=1, value=10000)
    with a_col2:
        email_only = st.number_input("Email only", min_value=0, step=1, value=3890)
    with a_col3:
        sms_only = st.number_input("Sms only", min_value=0, step=1, value=2956)
    with a_col4:
        customer_type = st.selectbox("Customers", options=["All customers", "Professionals", "College Students", "Family"])

    # Warning if sum > target
    if (email_only + sms_only) > target_customers:
        st.warning("Email only + SMS only counts exceed Target customers. Please verify values.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")  # gap

    # -----------------------
    # SECTION 3: Time Manage
    # -----------------------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Time Manage</div>', unsafe_allow_html=True)

    tcol1, tcol2 = st.columns([1,2])
    with tcol1:
        check_freq = st.selectbox("Check", options=["Every hour", "Every day", "Weekly", "Custom"])
        if check_freq == "Custom":
            custom_every_n = st.number_input("Custom frequency (n)", min_value=1, step=1, value=1, help="Repeat every n units")
            custom_unit = st.selectbox("Unit", options=["Hours","Days","Weeks"])
    with tcol2:
        today = date.today()
        date_range = st.date_input("Run length (start - end)", value=(today, today.replace(year=today.year+1)))
        # Ensure tuple structure
        if isinstance(date_range, tuple) and len(date_range) == 2:
            date_start, date_end = date_range
        else:
            # Fallback
            date_start, date_end = today, today

    start_now = st.checkbox("Start now", value=False, key="start_now_checkbox")
    if start_now:
        # Lock start date to today
        date_start = today
        st.info(f"Start now enabled — start date set to {date_start.isoformat()}")

    # Validate date order
    if date_start > date_end:
        st.error("Start date must be before or equal to End date.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")  # gap

    # -----------------------
    # SECTION 4: Create Rules (placeholder + simple composer)
    # -----------------------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Create Rules</div>', unsafe_allow_html=True)

    # Show rules list
    if st.session_state.rules:
        for idx, r in enumerate(st.session_state.rules):
            cols = st.columns([5,1])
            with cols[0]:
                st.markdown(f"**{idx+1}. {r['name']}** — Condition: {r['condition']} — Action: {r['action']}")
            with cols[1]:
                remove_key = f"remove_rule_{idx}"
                if st.button("Remove", key=remove_key):
                    st.session_state.rules.pop(idx)
                    st.experimental_rerun()
    else:
        st.markdown("<div class='muted'>No rules yet. Add rules to customize campaign behavior.</div>", unsafe_allow_html=True)

    st.write("")  # small gap

    # Add rule composer (collapsed by default)
    with st.expander("+ Add rule", expanded=False):
        rule_name = st.text_input("Rule name", key="rule_name_input")
        rule_condition = st.selectbox("Condition", options=["On schedule", "Target reached", "Custom condition"], key="rule_condition_select")
        rule_action = st.selectbox("Action", options=["Send email", "Pause campaign", "Notify team"], key="rule_action_select")
        rule_active = st.checkbox("Active", value=True, key="rule_active_checkbox")

        if st.button("Save rule", key="save_rule_button"):
            if not rule_name:
                st.error("Rule name is required.")
            else:
                new_rule = {
                    "name": rule_name,
                    "condition": rule_condition,
                    "action": rule_action,
                    "active": rule_active,
                    "created_at": datetime.utcnow().isoformat()
                }
                st.session_state.rules.append(new_rule)
                st.success("Rule added.")
                # clear composer fields by rerun
                st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")  # gap

    # -----------------------
    # Save / Submit area (minimal, no backend)
    # -----------------------
    save_cols = st.columns([1,1,1])
    with save_cols[0]:
        if st.button("Save draft"):
            st.success("Draft saved (session only).")
    with save_cols[1]:
        if st.button("Validate"):
            # Basic validations as final check
            errors = []
            if not campaign_name:
                errors.append("Campaign name is required.")
            if date_start > date_end:
                errors.append("Start date must be before or equal to End date.")
            if (email_only + sms_only) > target_customers:
                errors.append("Email+SMS counts exceed target customers.")
            if errors:
                for e in errors:
                    st.error(e)
            else:
                st.success("Validation passed.")
    with save_cols[2]:
        if st.button("Reset (session)"):
            # Reset non structural state
            st.session_state.rules = []
            st.experimental_rerun()

    # Footer (only on Page 2)
    st.markdown('<div class="footer-text">Developed by Kartvaya Raikwar</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # end main container

# ---------------------------
# Page Router
# ---------------------------
if st.session_state.page == "landing":
    page_landing()
elif st.session_state.page == "main":
    page_main()
else:
    # fallback
    st.session_state.page = "landing"
    page_landing()
