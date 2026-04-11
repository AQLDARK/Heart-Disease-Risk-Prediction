import streamlit as st
import pandas as pd
import logging

from ml.utils import load_json
from ml.predict import predict_risk
from ml.validation import ValidationError
from ui.components import risk_badge, stat_card, card, divider, info_box
from ml.storage import save_prediction
from ml.report import generate_patient_report_pdf

logger = logging.getLogger(__name__)


def render_predict_page(plan='Free'):
    st.markdown("## 🔬 Risk Prediction")
    st.markdown("*Enter patient information to assess heart disease risk*")

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

    col_left, col_right = st.columns([1.2, 1.2], gap="large")

    with col_left:
        st.markdown("### 📋 Patient Data")
        with st.form("patient_form", border=True):
            # Demographics
            st.markdown("**👤 Age & Sex**")
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                age = st.number_input("Age (years)", min_value=1, max_value=120, value=45)
            with col_a2:
                sex = st.selectbox("Sex", ["Female", "Male"], index=1)
                sex_val = 0 if sex == "Female" else 1
            
            st.divider()
            
            # Vitals
            st.markdown("**💓 Vital Signs**")
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                trestbps = st.number_input("BP (mmHg)", min_value=50, max_value=250, value=130)
            with col_v2:
                chol = st.number_input("Cholesterol (mg/dL)", min_value=50, max_value=600, value=240)
            
            col_v3, col_v4 = st.columns(2)
            with col_v3:
                thalach = st.number_input("Max HR (bpm)", min_value=50, max_value=250, value=150)
            with col_v4:
                oldpeak = st.number_input("ST Depression", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
            
            st.divider()
            
            # Clinical Indicators
            st.markdown("**🔬 Clinical Indicators**")
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                cp = st.selectbox("Chest Pain", [0, 1, 2, 3], index=1, help="Angina type (0-3)")
            with col_c2:
                exang = st.selectbox("Exercise Angina", [0, 1], index=0, help="0=No, 1=Yes")
            with col_c3:
                fbs = st.selectbox("Fasting BS", [0, 1], index=0, help=">120 mg/dL?")
            
            col_c4, col_c5, col_c6 = st.columns(3)
            with col_c4:
                restecg = st.selectbox("Rest ECG", [0, 1, 2], index=0)
            with col_c5:
                slope = st.selectbox("ST Slope", [0, 1, 2], index=1)
            with col_c6:
                ca = st.selectbox("Vessels", [0, 1, 2, 3], index=0, help="Calcified")
            
            st.markdown("**🧬 Additional**")
            thal = st.selectbox("Thalassemia Type", [0, 1, 2, 3], index=2)

            submitted = st.form_submit_button("🚀 Predict Risk", use_container_width=True)

        user_dict = {
            "age": age, "sex": sex_val, "cp": cp, "trestbps": trestbps, "chol": chol,
            "fbs": fbs, "restecg": restecg, "thalach": thalach, "exang": exang,
            "oldpeak": oldpeak, "slope": slope, "ca": ca, "thal": thal
        }

    with col_right:
        st.markdown("### 📊 Results")

        if submitted:
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
                            label="📄 Download PDF Report",
                            data=pdf_bytes,
                            file_name="heart_risk_report.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    else:
                        info_box("PDF reports available on Premium plan", "warning")
                except Exception as e:
                    logger.error(f"PDF generation failed: {e}")
                    st.warning(f"PDF generation failed: {e}")
                    
            except ValidationError as e:
                info_box(f"Validation error: {e}", "error")
                logger.warning(f"Validation error: {e}")
            except RuntimeError as e:
                info_box(f"Prediction failed: {e}", "error")
                logger.error(f"Prediction error: {e}")
            except Exception as e:
                info_box(f"Unexpected error: {e}", "error")
                logger.error(f"Unexpected error: {e}")

        # Show results if we have them
        p = st.session_state.get("latest_proba", None)
        label = st.session_state.get("latest_label", None)
        out = st.session_state.get("latest_out", None)

        if p is not None and label is not None and out is not None:
            st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)
            
            # Show risk metrics
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="metric">
                    <div class="metric-label">Risk Probability</div>
                    <div class="metric-value">{p*100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric">
                    <div class="metric-label">Risk Level</div>
                    <div style="font-size: 1.5rem; margin-top: 0.3rem;">
                        {risk_badge(label)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # Store for explainability page
            st.session_state["latest_input"] = user_dict
            st.session_state["latest_clean_df"] = out["cleaned_df"]

            # Save option
            col_save1, col_save2 = st.columns([3, 1])
            with col_save1:
                save_to_history = st.checkbox("💾 Save to history")
            with col_save2:
                pass
            
            if save_to_history:
                try:
                    save_prediction(user_dict, p, label)
                    info_box("Prediction saved to history", "success")
                    logger.info("Prediction saved")
                except Exception as e:
                    info_box(f"Could not save: {e}", "warning")
                    logger.error(f"Failed to save prediction: {e}")
            
            st.markdown("---")
            st.markdown("ℹ️ *This is a decision-support tool, not a medical diagnosis.*")
        else:
            st.info("👆 Fill the form and click **Predict Risk** to see results.")
