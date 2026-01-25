import streamlit as st
import pandas as pd

from ml.utils import load_json
from ml.predict import predict_risk
from ui.components import risk_badge

def render_predict_page():
    st.subheader("Predict")

    schema = load_json("models/feature_schema.json")

    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.markdown("### Patient Inputs")
        with st.form("patient_form"):
            age = st.number_input("age", min_value=1, max_value=120, value=45)
            sex = st.selectbox("sex (0=Female, 1=Male)", [0, 1], index=1)
            cp = st.selectbox("cp (0–3)", [0,1,2,3], index=1)
            trestbps = st.number_input("trestbps", min_value=50, max_value=250, value=130)
            chol = st.number_input("chol", min_value=50, max_value=600, value=240)
            fbs = st.selectbox("fbs (0/1)", [0,1], index=0)
            restecg = st.selectbox("restecg (0–2)", [0,1,2], index=0)
            thalach = st.number_input("thalach", min_value=50, max_value=250, value=150)
            exang = st.selectbox("exang (0/1)", [0,1], index=0)
            oldpeak = st.number_input("oldpeak", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
            slope = st.selectbox("slope (0–2)", [0,1,2], index=1)
            ca = st.selectbox("ca (0–3)", [0,1,2,3], index=0)
            thal = st.selectbox("thal (0–3)", [0,1,2,3], index=2)

            submitted = st.form_submit_button("Predict Risk")

        user_dict = {
            "age": age, "sex": sex, "cp": cp, "trestbps": trestbps, "chol": chol,
            "fbs": fbs, "restecg": restecg, "thalach": thalach, "exang": exang,
            "oldpeak": oldpeak, "slope": slope, "ca": ca, "thal": thal
        }

    with col_right:
        st.markdown("### Results")
        if submitted:
            out = predict_risk(user_dict, schema)
            p = out["proba"]
            label = out["label"]

            st.metric("Risk Probability", f"{p:.2f}")
            st.markdown(f"**Risk Label:** {risk_badge(label)}")
            st.caption("Disclaimer: This is a decision-support tool, not a medical diagnosis.")

            # Store latest prediction in session for Explainability page
            st.session_state["latest_input"] = user_dict
            st.session_state["latest_clean_df"] = out["cleaned_df"]

        else:
            st.info("Fill the form and click **Predict Risk** to see results.")
