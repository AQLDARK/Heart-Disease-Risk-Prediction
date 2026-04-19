import streamlit as st
import pandas as pd

from ml.utils import load_json
from ui.components import inject_page_background

def render_performance_page():
    inject_page_background("analytics")
    st.subheader("Model Performance")

    metrics = load_json("models/metrics.json")
    best = metrics["best_model"]
    allm = metrics["all_models"]

    st.markdown(f"**Best model selected:** `{best}`")

    rows = []
    for name, m in allm.items():
        rows.append({
            "model": name,
            "accuracy": m["accuracy"],
            "precision": m["precision"],
            "recall": m["recall"],
            "f1": m["f1"],
            "roc_auc": m["roc_auc"]
        })

    df = pd.DataFrame(rows).sort_values("roc_auc", ascending=False)
    st.dataframe(df, use_container_width=True)

    st.markdown("### Confusion Matrix (best model)")
    cm = allm[best]["confusion_matrix"]
    st.write(cm)
