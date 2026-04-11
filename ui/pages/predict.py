import streamlit as st
import pandas as pd

from ml.utils import load_json
from ml.predict import predict_risk
from ui.components import risk_badge
from ml.storage import save_prediction
from ml.report import generate_patient_report_pdf


def render_predict_page(plan='Free'):
    st.subheader("Predict")

    schema = load_json("models/feature_schema.json")

    # Persist values across reruns (Streamlit reruns top-to-bottom)
    if "latest_proba" not in st.session_state:
        st.session_state["latest_proba"] = None
    if "latest_label" not in st.session_state:
        st.session_state["latest_label"] = None
    if "latest_out" not in st.session_state:
        st.session_state["latest_out"] = None

    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.markdown("### Patient Inputs")
        with st.form("patient_form"):
            age = st.number_input("age", min_value=1, max_value=120, value=45)
            sex = st.selectbox("sex (0=Female, 1=Male)", [0, 1], index=1)
            cp = st.selectbox("cp (0–3)", [0, 1, 2, 3], index=1)
            trestbps = st.number_input("trestbps", min_value=50, max_value=250, value=130)
            chol = st.number_input("chol", min_value=50, max_value=600, value=240)
            fbs = st.selectbox("fbs (0/1)", [0, 1], index=0)
            restecg = st.selectbox("restecg (0–2)", [0, 1, 2], index=0)
            thalach = st.number_input("thalach", min_value=50, max_value=250, value=150)
            exang = st.selectbox("exang (0/1)", [0, 1], index=0)
            oldpeak = st.number_input("oldpeak", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
            slope = st.selectbox("slope (0–2)", [0, 1, 2], index=1)
            ca = st.selectbox("ca (0–3)", [0, 1, 2, 3], index=0)
            thal = st.selectbox("thal (0–3)", [0, 1, 2, 3], index=2)

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
            p = float(out["proba"])          # ensure numeric for formatting
            label = out["label"]

            st.session_state["latest_proba"] = p
            st.session_state["latest_label"] = label
            st.session_state["latest_out"] = out

            pdf_bytes = generate_patient_report_pdf(
                patient_data=user_dict,
                probability=p,
                label=label,
                shap_top_drivers=None
            )

            if plan == "Premium":
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_bytes,
                    file_name="heart_risk_report.pdf",
                    mime="application/pdf"
                )
            else:
                st.info("🔒 PDF reports are available on the **Premium** plan. Upgrade in **Subscription & Billing**.")

            

        # Show results if we have them (after submit, and also persists on rerun)
        p = st.session_state.get("latest_proba", None)
        label = st.session_state.get("latest_label", None)
        out = st.session_state.get("latest_out", None)

        if p is not None and label is not None and out is not None:
            st.metric("Risk Probability", f"{p:.2f}")
            st.markdown(f"**Risk Label:** {risk_badge(label)}")
            st.caption("Disclaimer: This is a decision-support tool, not a medical diagnosis.")

            # Store latest prediction in session for Explainability page
            st.session_state["latest_input"] = user_dict
            st.session_state["latest_clean_df"] = out["cleaned_df"]

            save_to_history = st.checkbox("Save this prediction to history", value=True)
            if save_to_history:
                save_prediction(user_dict, p, label)
                st.success("Saved to prediction history.")
        else:
            st.info("Fill the form and click **Predict Risk** to see results.")
