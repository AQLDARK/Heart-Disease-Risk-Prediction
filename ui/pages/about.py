import streamlit as st
from ui.components import inject_page_background

def render_about_page():
    inject_page_background("care")
    st.subheader("About")

    st.markdown("""
**Heart Disease Risk Prediction System** is a web-based decision-support tool.

- Dataset: UCI / Cleveland Heart Disease dataset  
- Tools: Python, scikit-learn, SHAP, Streamlit  
- Disclaimer: This is not a medical diagnosis system.
""")