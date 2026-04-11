import streamlit as st
from ui.components import section_header, card

def render_about_page():
    section_header("ℹ️ About CardioPredict")
    st.divider()

    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 🎯 Mission")
        card("What We Do", 
             "CardioPredict is a decision-support tool designed to help healthcare professionals and patients understand cardiovascular disease risk using machine learning and interpretable AI.")
        
        st.markdown("### 📊 Data & Model")
        card("Dataset", 
             "<strong>Source:</strong> UCI Machine Learning Repository<br><strong>Cases:</strong> Cleveland Heart Disease Dataset<br><strong>Features:</strong> 13 clinical indicators")
        
        card("Algorithm", 
             "<strong>Model:</strong> Random Forest Classifier<br><strong>Accuracy:</strong> ~85%<br><strong>Validation:</strong> 5-fold cross-validation")
    
    with col2:
        st.markdown("### 🛠️ Technology Stack")
        card("Backend", 
             "<strong>Language:</strong> Python 3.13<br><strong>ML:</strong> scikit-learn, XGBoost<br><strong>Explainability:</strong> SHAP")
        
        card("Frontend", 
             "<strong>Framework:</strong> Streamlit<br><strong>Styling:</strong> Custom CSS + Gradients<br><strong>Security:</strong> Bcrypt, Input Validation")
        
        card("Database", 
             "<strong>Engine:</strong> SQLite<br><strong>Storage:</strong> User accounts, predictions, audit logs<br><strong>Backup:</strong> Daily automatic")
    
    st.divider()
    
    st.markdown("### ⚠️ Important Disclaimer")
    st.warning("""
    **CardioPredict is NOT a medical diagnosis system.** 
    
    This tool is designed as a **decision-support aid** for healthcare professionals and educational purposes only. 
    It should never replace:
    - Professional medical evaluation
    - Clinical judgment by licensed physicians
    - Proper diagnostic testing and examination
    
    Always consult with qualified healthcare professionals for accurate diagnosis and treatment.
    """)
    
    st.markdown("### 📝 Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("✅ **Risk Prediction**\nML-powered risk assessment")
        st.markdown("✅ **Interpretability**\nSHAP explanations")
    
    with col2:
        st.markdown("✅ **Secure Auth**\nBcrypt password hashing")
        st.markdown("✅ **Audit Trail**\nFull prediction history")
    
    with col3:
        st.markdown("✅ **Multi-role**\nPatient, Clinician, Admin")
        st.markdown("✅ **PDF Reports**\nPremium feature")
    
    st.divider()
    
    st.markdown(
        """
        <div style="text-align: center; color: #94a3b8; font-size: 0.9rem; margin-top: 2rem;">
        <p>❤️ Built with ❤️ for better health outcomes</p>
        <p style="margin-top: 1rem;">© 2026 CardioPredict • Version 1.0</p>
        </div>
        """,
        unsafe_allow_html=True
    )