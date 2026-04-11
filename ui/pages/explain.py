import streamlit as st
import numpy as np
import shap
import matplotlib.pyplot as plt
import joblib

from ml.utils import load_json
from ml.explain import build_explainer, explain_one, top_drivers
from ui.components import section_header

def render_explain_page():
    section_header("🧠 Model Explainability")
    st.markdown("**Understand why the model made its prediction using SHAP analysis**")
    st.divider()

    if "latest_input" not in st.session_state:
        st.warning("⚠️ Make a prediction first (Predict tab).")
        return

    schema = load_json("models/feature_schema.json")

    preprocess = joblib.load("models/preprocess.pkl")
    model = joblib.load("models/best_model.pkl")

    df = st.session_state["latest_clean_df"]

    # Preprocess to model input space
    X_row = preprocess.transform(df)

    # Get transformed feature names (important!)
    try:
        feature_names = preprocess.get_feature_names_out()
    except Exception:
        feature_names = [f"f{i}" for i in range(X_row.shape[1])]

    # Background for SHAP (small synthetic background)
    # For academic demo: sample from zeros + small noise
    bg = np.zeros((50, X_row.shape[1]))
    explainer = build_explainer(model, bg)

    shap_values = explain_one(explainer, X_row)

    col1, col2 = st.columns([1,1], gap="large")

    with col1:
        st.markdown("### Local explanation (this prediction)")
        drivers = top_drivers(shap_values, feature_names, top_k=5)
        st.write("**Top 5 drivers (SHAP):**")
        for f, v in drivers:
            st.write(f"- {f}: {v:+.4f}")

        fig = plt.figure()
        shap.plots.waterfall(shap_values[0], max_display=10, show=False)
        st.pyplot(fig, clear_figure=True)

    with col2:
        st.markdown("### Global explanation (overview)")
        st.caption("For speed, this global plot uses a small background. For best results, precompute global SHAP offline.")

        fig2 = plt.figure()
        shap.plots.bar(shap_values, max_display=12, show=False)
        st.pyplot(fig2, clear_figure=True)
