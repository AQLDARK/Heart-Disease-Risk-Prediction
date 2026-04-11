import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from ml.storage import load_predictions
from ml.utils import load_json
from ml.storage import get_subscription



def render_admin_dashboard():
    st.subheader("Administrative Analytics Dashboard")
    st.caption("Population-level heart disease risk insights")

    df = load_predictions(limit=5000)

    if df.empty:
        st.warning("No prediction data available yet.")
        return

    # ---------------------------------
    # Data preparation
    # ---------------------------------

    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    # Age groups
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 30, 45, 60, 120],
        labels=["18–30", "31–45", "46–60", "60+"]
    )

    # Gender mapping
    df["gender"] = df["sex"].map({0: "Female", 1: "Male"})

    # ---------------------------------
    # KPI Cards
    # ---------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Predictions", len(df))
    col2.metric("High-Risk Patients", int((df["label"] == "High").sum()))
    col3.metric("Low-Risk Patients", int((df["label"] == "Low").sum()))

    st.divider()

    # ---------------------------------
    # Risk Distribution
    # ---------------------------------

    st.markdown("### Risk Distribution")

    risk_counts = df["label"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(
        risk_counts,
        labels=risk_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax1.axis("equal")
    st.pyplot(fig1)

    # ---------------------------------
    # Risk by Age Group
    # ---------------------------------

    st.markdown("### Risk by Age Group")

    age_risk = (
        df.groupby(["age_group", "label"])
        .size()
        .unstack(fill_value=0)
    )

    st.bar_chart(age_risk)

    # ---------------------------------
    # Risk by Gender
    # ---------------------------------

    st.markdown("### Risk by Gender")

    gender_risk = (
        df.groupby(["gender", "label"])
        .size()
        .unstack(fill_value=0)
    )

    st.bar_chart(gender_risk)

    # ---------------------------------
    # Prediction Trend
    # ---------------------------------

    st.markdown("### Prediction Trend Over Time")

    df["date"] = df["created_at"].dt.date
    trend = df.groupby("date").size()

    st.line_chart(trend)

    st.divider()

    st.caption(
        "Insights generated from aggregated prediction records. "
        "Used for population-level healthcare planning and preventive analysis."
    )

    st.markdown("### Top Contributing Risk Factors (Global SHAP)")

    try:
        shap_dict = load_json("models/global_shap_grouped.json")

        shap_series = (
            pd.Series(shap_dict)
            .sort_values(ascending=False)
            .head(12)
        )

        st.write("Grouped global feature importance (summed across one-hot encoded categories).")

        st.bar_chart(shap_series)

        st.dataframe(
            shap_series.reset_index().rename(columns={"index": "feature", 0: "mean_abs_shap"}),
            use_container_width=True
        )

    except FileNotFoundError:
        st.warning("Grouped global SHAP file not found. Re-run training to generate models/global_shap_grouped.json.")

