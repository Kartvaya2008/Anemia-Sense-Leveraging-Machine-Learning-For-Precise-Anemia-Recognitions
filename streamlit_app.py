# app.py
import streamlit as st
import numpy as np
import pickle
from typing import List

st.set_page_config(page_title="AnemiaSense", page_icon="🩸", layout="centered")

# ---------------------------
# CONFIG: Edit these to match your model's expected feature order.
# Keep the first feature 'gender' encoded as 0 (Male) or 1 (Female).
# Add or remove feature names to match your dataset/model input order.
# Example default set (common hematology columns).
FEATURE_COLUMNS: List[str] = [
    "gender",        # 0 = Male, 1 = Female
    "hemoglobin",    # g/dL
    "mch",           # Mean Corpuscular Hemoglobin
    "mchc",          # Mean Corpuscular Hemoglobin Concentration
    "mcv",           # Mean Corpuscular Volume
    "rbc",           # Red Blood Cell count (optional)
    "wbc",           # White Blood Cell count (optional)
    "platelets",     # Platelet count (optional)
    "pcv"            # Packed Cell Volume (optional)
]
MODEL_FILENAME = "model.pkl"  # expected model file in project root

# ---------------------------
# Session state for simple routing
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

def goto_main():
    st.session_state.page = "main"

# ---------------------------
# Landing Page (Page 1)
# ---------------------------
def render_landing():
    st.title("Spark Your Creativity with AI")
    st.markdown("**Unleash your content genius — AnemiaSense**")
    st.write("")  # spacing
    if st.button("Start", key="start_btn"):
        goto_main()

# ---------------------------
# Validation helpers
# ---------------------------
def positive_number(value):
    try:
        val = float(value)
        return val >= 0
    except Exception:
        return False

def load_model(path: str):
    with open(path, "rb") as f:
        return pickle.load(f)

# ---------------------------
# Main Page (Page 2) — Anemia Prediction Form
# ---------------------------
def render_main():
    st.header("Anemia Prediction")
    st.write("Enter blood parameter values below and click **Predict Anemia**.")

    # Layout: create two columns for inputs to keep them compact
    num_features = len(FEATURE_COLUMNS)
    cols_per_row = 2
    input_values = {}

    # Gender input handled specially
    if "gender" not in FEATURE_COLUMNS:
        st.error("Configuration error: 'gender' must be present in FEATURE_COLUMNS as the first feature.")
        return

    # First row: gender + first numeric feature (if exists)
    st.subheader("Patient Parameters")
    # Build input widgets dynamically in two-column rows
    for i in range(0, num_features, cols_per_row):
        cols = st.columns(cols_per_row)
        for col_index in range(cols_per_row):
            idx = i + col_index
            if idx >= num_features:
                # fill empty space if odd number of fields
                cols[col_index].empty()
                continue
            feature = FEATURE_COLUMNS[idx]
            # Render gender as selectbox (0 or 1)
            if feature.lower() == "gender":
                val = cols[col_index].selectbox(
                    "Gender",
                    options=[0, 1],
                    format_func=lambda x: "Male (0)" if x == 0 else "Female (1)",
                    help="Select 0 for Male, 1 for Female",
                    key="gender_input"
                )
                input_values["gender"] = int(val)
            else:
                # Generic numeric input
                # Provide placeholder examples for common names
                placeholder_map = {
                    "hemoglobin": "e.g., 13.5 (g/dL)",
                    "mch": "e.g., 22.7",
                    "mchc": "e.g., 29.1",
                    "mcv": "e.g., 83.7",
                    "rbc": "e.g., 4.5",
                    "wbc": "e.g., 7.1",
                    "platelets": "e.g., 250",
                    "pcv": "e.g., 40"
                }
                ph = placeholder_map.get(feature.lower(), "")
                # use number_input for numeric validation and consistent UI
                # default to 0.0 for floats; allow step=0.1 for medical values
                # For large integers like platelets, user can type appropriate number
                try:
                    default = 0.0
                    step = 0.1
                    if feature.lower() in ["platelets", "rbc", "wbc"]:
                        # platelets often integer; rbc/wbc often floats
                        step = 0.1
                    value = cols[col_index].number_input(
                        label=feature.replace("_", " ").title(),
                        min_value=0.0,
                        value=default,
                        step=step,
                        format="%.2f",
                        help=ph,
                        key=f"inp_{feature}"
                    )
                    input_values[feature] = float(value)
                except Exception:
                    # fallback: text input (should not occur)
                    v = cols[col_index].text_input(feature.replace("_", " ").title(), key=f"txt_{feature}")
                    input_values[feature] = float(v) if v.strip() != "" else 0.0

    st.write("")  # spacer

    # Predict button
    predict_clicked = st.button("Predict Anemia", key="predict_btn")

    # Result area
    result_area = st.empty()

    if predict_clicked:
        # Validate inputs
        errors = []
        # gender must be exactly 0 or 1
        g = input_values.get("gender", None)
        if g not in (0, 1):
            errors.append("Gender must be 0 (Male) or 1 (Female).")

        # Validate all numeric features are non-negative numbers
        for feat, val in input_values.items():
            if feat == "gender":
                continue
            try:
                num = float(val)
                if num < 0:
                    errors.append(f"{feat.replace('_',' ').title()} must be a non-negative number.")
            except Exception:
                errors.append(f"{feat.replace('_',' ').title()} must be a valid number.")

        if errors:
            for e in errors:
                result_area.error(e)
            return

        # Prepare input array for model: ensure order matches FEATURE_COLUMNS
        try:
            feature_vector = [float(input_values[f]) if f in input_values else 0.0 for f in FEATURE_COLUMNS]
            arr = np.array(feature_vector, dtype=float).reshape(1, -1)
        except Exception as ex:
            result_area.error("Failed to prepare input vector: " + str(ex))
            return

        # Load model and predict
        try:
            model = load_pickle_model(MODEL_FILENAME)
        except FileNotFoundError:
            result_area.error(f"Model file '{MODEL_FILENAME}' not found in project root. Place the trained model at this path.")
            return
        except Exception as ex:
            result_area.error("Failed to load model: " + str(ex))
            return

        # Model prediction
        try:
            pred = model.predict(arr)
            # predict may return array
            label = int(pred[0]) if hasattr(pred, "__iter__") else int(pred)
            # Optionally show probability if available
            prob_text = ""
            if hasattr(model, "predict_proba"):
                try:
                    proba = model.predict_proba(arr)
                    # If binary, take proba for class 1
                    p = float(proba[0][1]) if proba.shape[1] > 1 else float(proba[0][0])
                    prob_text = f" (risk score: {p:.2f})"
                except Exception:
                    prob_text = ""
            if label == 0:
                result_area.success("No Anemia detected." + prob_text)
            else:
                result_area.error("Anemia detected." + prob_text)
        except Exception as ex:
            result_area.error("Prediction failed: " + str(ex))

# ---------------------------
# Minimal helper to load model with clear error semantics
# ---------------------------
def load_pickle_model(path: str):
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        raise
    except Exception as e:
        # propagate other errors
        raise

# ---------------------------
# Router
# ---------------------------
if st.session_state.page == "landing":
    render_landing()
elif st.session_state.page == "main":
    render_main()
else:
    # fallback safety
    st.session_state.page = "landing"
    render_landing()
