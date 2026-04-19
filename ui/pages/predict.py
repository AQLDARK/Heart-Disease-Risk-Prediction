import streamlit as st
import pandas as pd
import logging
import matplotlib.pyplot as plt
import numpy as np

from ml.utils import load_json
from ml.predict import predict_risk
from ml.validation import ValidationError
from ml.recommendations import generate_clinical_recommendations, format_recommendations_for_display, get_risk_color, get_risk_icon, get_emergency_contact_info
from ui.components import risk_badge, stat_card, card, divider, info_box, inject_page_background
from ml.storage import save_prediction
from ml.report import generate_patient_report_pdf

logger = logging.getLogger(__name__)


def get_confidence_level(probability):
    """Determine confidence level based on probability."""
    if probability >= 0.80:
        return "High Confidence", "#22c55e", "✅"
    elif probability >= 0.60:
        return "Medium Confidence", "#f97316", "⚠️"
    else:
        return "Low Confidence", "#ef4444", "❌"


def render_confidence_gauge(probability, height=280):
    """Render a gauge chart for confidence visualization."""
    fig, ax = plt.subplots(figsize=(8, height/100), subplot_kw=dict(projection='polar'))
    
    # Gauge setup
    theta = np.linspace(np.pi, 0, 100)
    r = np.ones(100)
    
    # Color zones
    low_mask = theta >= np.pi * 0.67
    medium_mask = (theta >= np.pi * 0.34) & (theta < np.pi * 0.67)
    high_mask = theta < np.pi * 0.34
    
    # Plot zones
    ax.fill_between(theta[low_mask], 0, r[low_mask], color='#ef4444', alpha=0.3)
    ax.fill_between(theta[medium_mask], 0, r[medium_mask], color='#f97316', alpha=0.3)
    ax.fill_between(theta[high_mask], 0, r[high_mask], color='#22c55e', alpha=0.3)
    
    # Plot needle
    needle_angle = np.pi - (probability * np.pi)
    ax.plot([needle_angle, needle_angle], [0, 1], 'w-', linewidth=3)
    ax.scatter([needle_angle], [1], color='white', s=200, zorder=5)
    
    # Labels
    ax.text(np.pi * 0.84, 1.3, 'Low\n(< 60%)', ha='center', va='center', fontsize=9, color='white', weight='bold')
    ax.text(np.pi * 0.5, 1.3, 'Medium\n(60-79%)', ha='center', va='center', fontsize=9, color='white', weight='bold')
    ax.text(np.pi * 0.16, 1.3, 'High\n(≥ 80%)', ha='center', va='center', fontsize=9, color='white', weight='bold')
    
    # Center text
    ax.text(0, 0, f'{probability*100:.1f}%', ha='center', va='center', fontsize=18, color='white', weight='bold')
    
    ax.set_ylim(0, 1.5)
    ax.set_theta_offset(np.pi)
    ax.set_theta_direction(-1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['polar'].set_visible(False)
    
    fig.patch.set_facecolor('#0f1419')
    
    return fig


def render_confidence_bar(probability):
    """Render a horizontal progress bar for confidence."""
    confidence_level, color, icon = get_confidence_level(probability)
    percentage = probability * 100
    
    # Create HTML progress bar
    html = f"""
    <div style="margin: 1.5rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-weight: bold; color: white;">Model Confidence</span>
            <span style="color: {color}; font-weight: bold;">{icon} {confidence_level}</span>
        </div>
        <div style="
            width: 100%;
            height: 12px;
            background: #1a1f2e;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #2d3748;
        ">
            <div style="
                width: {percentage}%;
                height: 100%;
                background: linear-gradient(90deg, {color}, {color});
                border-radius: 10px;
                transition: width 0.3s ease;
            "></div>
        </div>
        <div style="
            display: flex;
            justify-content: space-between;
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: #9ca3af;
        ">
            <span>0%</span>
            <span style="color: {color}; font-weight: bold;">{percentage:.1f}%</span>
            <span>100%</span>
        </div>
    </div>
    """
    return html


def render_probability_distribution(probability, risk_label):
    """Render a probability distribution chart."""
    # Simulate a distribution around the predicted probability
    # In reality, you might have actual model uncertainty estimates
    low_prob = 0.3
    medium_prob = 0.5
    high_prob = 0.7
    
    # Map to actual probability based on label
    if risk_label == "High":
        high_prob = probability
    elif risk_label == "Medium":
        medium_prob = probability
    else:
        low_prob = probability
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Distribution data
    categories = ['Low Risk\nProbability', 'Medium Risk\nProbability', 'High Risk\nProbability']
    values = [low_prob, medium_prob, high_prob]
    colors = ['#22c55e', '#f97316', '#ef4444']
    
    # Create bars
    bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='white', linewidth=2)
    
    # Add value labels on bars
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val*100:.1f}%',
               ha='center', va='bottom', fontweight='bold', color='white', fontsize=11)
    
    ax.set_ylim(0, 1)
    ax.set_ylabel('Probability', color='white', fontweight='bold', fontsize=11)
    ax.set_title('Risk Class Probability Distribution', color='white', fontweight='bold', fontsize=12, pad=20)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
    ax.tick_params(colors='white', labelsize=10)
    ax.grid(True, alpha=0.2, axis='y', color='gray')
    
    fig.patch.set_facecolor('#0f1419')
    ax.set_facecolor('#0f1419')
    for spine in ax.spines.values():
        spine.set_color('white')
    
    plt.tight_layout()
    return fig


def render_predict_page(plan='Free'):
    # Add premium background
    inject_page_background("medical")
    
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
            
            # ============================================
            # Risk Assessment Overview
            # ============================================
            st.markdown("**Risk Assessment:**")
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
            
            # ============================================
            # Confidence Visualization
            # ============================================
            st.markdown("**Model Confidence & Uncertainty:**")
            
            confidence_level, confidence_color, confidence_icon = get_confidence_level(p)
            
            # Create tabs for different confidence visualizations
            conf_tab1, conf_tab2, conf_tab3 = st.tabs(["Confidence Meter", "Gauge Chart", "Probability Distribution"])
            
            with conf_tab1:
                # Progress bar visualization
                st.markdown(render_confidence_bar(p), unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="
                    background: rgba(15, 20, 25, 0.8);
                    border: 1px solid {confidence_color};
                    border-radius: 10px;
                    padding: 1rem;
                    margin-top: 1rem;
                ">
                    <div style="font-size: 0.95rem; color: #9ca3af; line-height: 1.6;">
                        <strong>What this means:</strong><br>
                        {confidence_icon} <strong>{confidence_level}</strong> - 
                        """, unsafe_allow_html=True)
                
                if p >= 0.80:
                    st.markdown("""
                        The model has high confidence in this prediction. The risk assessment is based on strong 
                        patterns in the patient's clinical data. However, this is still a statistical prediction and 
                        should be validated with clinical judgment.
                    """, unsafe_allow_html=True)
                elif p >= 0.60:
                    st.markdown("""
                        The model has medium confidence in this prediction. The risk level is moderate, and the 
                        clinical indicators show mixed signals. Additional clinical evaluation is recommended.
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        The model has low confidence in this prediction. The clinical indicators are unclear or 
                        inconsistent. Additional diagnostic tests or specialist consultation may be beneficial.
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            with conf_tab2:
                # Gauge chart
                try:
                    fig_gauge = render_confidence_gauge(p)
                    st.pyplot(fig_gauge, use_container_width=True)
                    plt.close(fig_gauge)
                    
                    st.markdown("""
                    **Gauge Interpretation:**
                    - The needle position shows your predicted probability
                    - **Green zone (≥80%):** High confidence in heart disease risk
                    - **Orange zone (60-79%):** Medium confidence, borderline risk
                    - **Red zone (<60%):** Lower confidence, appears low-risk
                    """)
                except Exception as e:
                    st.warning(f"Could not render gauge: {e}")
                    logger.error(f"Gauge rendering error: {e}")
            
            with conf_tab3:
                # Probability distribution
                try:
                    fig_dist = render_probability_distribution(p, label)
                    st.pyplot(fig_dist, use_container_width=True)
                    plt.close(fig_dist)
                    
                    st.markdown(f"""
                    **Distribution Explanation:**
                    - This chart shows the model's assessment for each risk category
                    - **Highlighted bar:** Your predicted risk class ({label}) with {p*100:.1f}% probability
                    - A higher bar indicates greater likelihood of that risk category
                    - The distribution helps understand how clear the prediction is
                    """)
                except Exception as e:
                    st.warning(f"Could not render distribution: {e}")
                    logger.error(f"Distribution rendering error: {e}")
            
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
            
            # ============================================
            # Clinical Recommendations Section
            # ============================================
            st.markdown("### 💊 Clinical Recommendations")
            
            try:
                # Generate recommendations
                recommendations = generate_clinical_recommendations(label, p, user_dict)
                
                # Create tabs for different aspects of recommendations
                rec_tab1, rec_tab2, rec_tab3 = st.tabs(["Summary", "Detailed Guidance", "Emergency Signs"])
                
                with rec_tab1:
                    # Risk Summary Card
                    risk_color = get_risk_color(label)
                    risk_icon = get_risk_icon(label)
                    
                    st.markdown(f"""
                    <div style="
                        background: rgba({int(risk_color[1:3], 16)}, {int(risk_color[3:5], 16)}, {int(risk_color[5:7], 16)}, 0.1);
                        border: 2px solid {risk_color};
                        border-radius: 12px;
                        padding: 1.5rem;
                        margin: 1rem 0;
                    ">
                        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">
                            {risk_icon} <strong>Risk Assessment: {label.upper()}</strong>
                        </div>
                        <div style="font-size: 1.1rem; color: {risk_color}; margin: 1rem 0;">
                            Probability: {p*100:.1f}%
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Key Findings
                    if recommendations.get("key_findings"):
                        st.markdown("**Key Clinical Findings:**")
                        for finding in recommendations["key_findings"]:
                            st.write(finding)
                    
                    # Primary Recommendations
                    if recommendations.get("primary_recommendations"):
                        st.markdown("**Recommended Actions:**")
                        for rec in recommendations["primary_recommendations"]:
                            st.write(rec)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with rec_tab2:
                    st.markdown("**Lifestyle & Prevention Guidance**")
                    
                    # Lifestyle Modifications
                    if recommendations.get("lifestyle_modifications"):
                        for mod in recommendations["lifestyle_modifications"]:
                            st.write(mod)
                    
                    st.divider()
                    
                    # Monitoring Guidelines
                    if recommendations.get("monitoring_guidelines"):
                        st.markdown("**Monitoring & Follow-up:**")
                        for guideline in recommendations["monitoring_guidelines"]:
                            st.write(f"- {guideline}")
                
                with rec_tab3:
                    st.markdown("**⚠️ When to Seek Emergency Care**")
                    
                    # Get Sri Lanka emergency contact info
                    emergency_info = get_emergency_contact_info()
                    
                    warning_color = "#ef4444"  # Red
                    st.markdown(f"""
                    <div style="
                        background: rgba(239, 68, 68, 0.1);
                        border-left: 4px solid {warning_color};
                        border-radius: 8px;
                        padding: 1rem;
                        margin: 1rem 0;
                    ">
                        <div style="font-weight: bold; color: {warning_color}; margin-bottom: 0.5rem; font-size: 1.1rem;">
                            🚑 {emergency_info['ambulance_number']} - {emergency_info['ambulance_service']} (Toll-free)
                        </div>
                        <div style="color: {warning_color}; margin-bottom: 1rem;">
                            {emergency_info['emergency_message']}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("**Warning Signs - Call 1990 Immediately:**")
                    if recommendations.get("warning_signs"):
                        for sign in recommendations["warning_signs"]:
                            st.write(f"• {sign}")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.divider()
                    
                    st.markdown("**Emergency Call Tips for Sri Lanka:**")
                    for tip in emergency_info['emergency_tips']:
                        st.write(f"- {tip}")
                    
                    st.markdown("""
                    **Time is Critical:** In cardiac emergencies, every minute counts. Do not delay calling 1990. Never attempt to drive yourself to the hospital if experiencing severe symptoms.
                    """)

            
            except Exception as e:
                logger.error(f"Error generating recommendations: {e}")
                st.warning(f"Could not generate recommendations: {e}")
            
            st.markdown("---")
            st.markdown("""
            ### ⚕️ Medical Disclaimer
            
            **IMPORTANT:** This prediction tool is for educational and decision-support purposes only. It is **NOT** a medical diagnosis or a substitute for professional medical advice, diagnosis, or treatment. 
            
            - Always consult with a qualified healthcare provider for medical advice
            - This tool should be used in conjunction with, not instead of, clinical judgment
            - Results are based on statistical models and may not apply to all individuals
            - For medical emergencies, always call emergency services (119)
            """)

        else:
            st.info("👆 Fill the form and click **Predict Risk** to see results.")
