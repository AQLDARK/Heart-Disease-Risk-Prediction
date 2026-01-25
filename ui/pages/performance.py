import streamlit as st
import pandas as pd

from ml.utils import load_json

def render_performance_page():
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
