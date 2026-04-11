import streamlit as st

def render_about_page():
    st.subheader("About")

    st.markdown("""
**Heart Disease Risk Prediction System** is a web-based decision-support tool.

- Dataset: UCI / Cleveland Heart Disease dataset  
- Tools: Python, scikit-learn, SHAP, Streamlit  
- Disclaimer: This is not a medical diagnosis system.
""")