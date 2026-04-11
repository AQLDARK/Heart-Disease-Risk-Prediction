import streamlit as st
import pandas as pd
import logging

from ml.utils import load_json
from ml.predict import predict_risk
from ml.validation import ValidationError
from ui.components import risk_badge, section_header, metric_card
from ml.storage import save_prediction
from ml.report import generate_patient_report_pdf

logger = logging.getLogger(__name__)


def render_predict_page(plan='Free'):
    section_header("🔍 Risk Prediction")
    st.markdown("**Enter patient information to predict cardiovascular disease risk**")
    st.divider()

    try:
        schema = load_json("models/feature_schema.json")
    except Exception as e:
        st.error(f"Failed to load model schema: {e}")
        logger.error(f"Schema loading error: {e}")
        return

    # Persist values across reruns
    if "latest_proba" not in st.session_state:
        st.session_state["latest_proba"] = None
    if "latest_label" not in st.session_state:
        st.session_state["latest_label"] = None
    if "latest_out" not in st.session_state:
        st.session_state["latest_out"] = None

    col_left, col_right = st.columns([1.2, 1], gap="large")

    with col_left:
        st.markdown("### 👤 Patient Information")
        with st.form("patient_form"):
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Age", min_value=1, max_value=120, value=45)
                sex = st.selectbox("Sex", ["Female (0)", "Male (1)"], index=1)
                sex_val = 1 if sex == "Male (1)" else 0
                
                cp = st.selectbox("Chest Pain Type", 
                                 ["Typical Angina (0)", "Atypical Angina (1)", "Non-anginal Pain (2)", "Asymptomatic (3)"], 
                                 index=1)
                cp_val = int(cp.split("(")[1].strip(")"))
                
                trestbps = st.number_input("Resting BP (mmHg)", min_value=50, max_value=250, value=130)
                chol = st.number_input("Cholesterol (mg/dl)", min_value=50, max_value=600, value=240)
            
            with col2:
                fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", ["No (0)", "Yes (1)"], index=0)
                fbs_val = 1 if fbs == "Yes (1)" else 0
                
                restecg = st.selectbox("Resting ECG", 
                                      ["Normal (0)", "ST-T Abnormality (1)", "LV Hypertrophy (2)"], 
                                      index=0)
                restecg_val = int(restecg.split("(")[1].strip(")"))
                
                thalach = st.number_input("Max Heart Rate", min_value=50, max_value=250, value=150)
                exang = st.selectbox("Exercise Induced Angina", ["No (0)", "Yes (1)"], index=0)
                exang_val = 1 if exang == "Yes (1)" else 0
            
            col1, col2 = st.columns(2)
            with col1:
                oldpeak = st.number_input("ST Depression", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
                slope = st.selectbox("ST Slope", ["Upsloping (0)", "Flat (1)", "Downsloping (2)"], index=1)
                slope_val = int(slope.split("(")[1].strip(")"))
            
            with col2:
                ca = st.selectbox("Major Vessels (0-3)", [0, 1, 2, 3], index=0)
                thal = st.selectbox("Thalassemia", ["Normal (0)", "Fixed Defect (1)", "Reversible Defect (2)", "Severe (3)"], index=2)
                thal_val = int(thal.split("(")[1].strip(")"))

            submitted = st.form_submit_button("🚀 Predict Risk", use_container_width=True)

        user_dict = {
            "age": age, "sex": sex_val, "cp": cp_val, "trestbps": trestbps, "chol": chol,
            "fbs": fbs_val, "restecg": restecg_val, "thalach": thalach, "exang": exang_val,
            "oldpeak": oldpeak, "slope": slope_val, "ca": ca, "thal": thal_val
        }

    with col_right:
        st.markdown("### 📊 Prediction Results")
        
        if submitted:
            with st.spinner("Analyzing patient data..."):
                try:
                    out = predict_risk(user_dict, schema)
                    p = float(out["proba"])
                    label = out["label"]

                    st.session_state["latest_proba"] = p
                    st.session_state["latest_label"] = label
                    st.session_state["latest_out"] = out

                    try:
                        pdf_bytes = generate_patient_report_pdf(
                            patient_data=user_dict,
                            probability=p,
                            label=label,
                            shap_top_drivers=None
                        )

                        if plan == "Premium":
                            st.download_button(
                                label="📥 Download PDF Report",
                                data=pdf_bytes,
                                file_name="heart_risk_report.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        else:
                            st.info("🔒 PDF reports are available on the **Premium** plan. Upgrade in **Subscription & Billing**.")
                    except Exception as e:
                        logger.error(f"PDF generation failed: {e}")
                        st.warning(f"PDF report generation failed: {e}")
                        
                except ValidationError as e:
                    st.error(f"❌ Input validation error: {e}")
                    logger.warning(f"Validation error: {e}")
                except RuntimeError as e:
                    st.error(f"❌ Prediction failed: {e}")
                    logger.error(f"Prediction error: {e}")
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {e}")
                    logger.error(f"Unexpected error in prediction: {e}")

        # Show results if we have them
        p = st.session_state.get("latest_proba", None)
        label = st.session_state.get("latest_label", None)
        out = st.session_state.get("latest_out", None)

        if p is not None and label is not None and out is not None:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Risk Probability", f"{p*100:.1f}%", delta=None)
            with col2:
                st.markdown(f"**Risk Level:** {risk_badge(label)}", unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.caption("⚕️ Disclaimer: This is a decision-support tool, not a medical diagnosis.")

            # Store for Explainability page
            st.session_state["latest_input"] = user_dict
            st.session_state["latest_clean_df"] = out["cleaned_df"]

            st.divider()
            save_to_history = st.checkbox("💾 Save prediction to history", value=True)
            if save_to_history:
                try:
                    save_prediction(user_dict, p, label)
                    st.success("✅ Saved to prediction history.")
                    logger.info(f"Prediction saved")
                except Exception as e:
                    st.warning(f"Could not save to history: {e}")
                    logger.error(f"Failed to save prediction: {e}")
        else:
            st.info("Fill the form and click **Predict Risk** to see results.")

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
                try:
                    save_prediction(user_dict, p, label)
                    st.success("✅ Saved to prediction history.")
                    logger.info(f"Prediction saved for user")
                except Exception as e:
                    st.warning(f"Could not save to history: {e}")
                    logger.error(f"Failed to save prediction: {e}")
        else:
            st.info("Fill the form and click **Predict Risk** to see results.")
