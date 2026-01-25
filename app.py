import streamlit as st

from ui.components import inject_dark_css
from ui.pages.predict import render_predict_page
from ui.pages.explain import render_explain_page
from ui.pages.performance import render_performance_page
from ui.pages.about import render_about_page

def main():
    st.set_page_config(
        page_title="Heart Disease Risk Prediction System",
        layout="wide"
    )

    inject_dark_css()

    st.title("Heart Disease Risk Prediction System")
    st.caption("Decision-support dashboard — not a medical diagnosis.")

    tabs = st.tabs(["Predict", "Explainability", "Model Performance", "About"])

    with tabs[0]:
        render_predict_page()
    with tabs[1]:
        render_explain_page()
    with tabs[2]:
        render_performance_page()
    with tabs[3]:
        render_about_page()

if __name__ == "__main__":
    main()