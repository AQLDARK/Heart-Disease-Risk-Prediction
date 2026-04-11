import streamlit as st
import pandas as pd
from datetime import date

from ml.storage import load_predictions

def render_history_page():
    st.subheader("Prediction History")
    st.caption("Stored predictions for audit, reporting, and analytics.")

    # Load records
    df = load_predictions(limit=1000)

    if df.empty:
        st.info("No predictions saved yet. Make a prediction first.")
        return

    # Convert created_at to datetime for filtering
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    # --- Filters ---
    with st.expander("Filters", expanded=False):
        col1, col2 = st.columns(2)
        min_d = df["created_at"].min().date() if df["created_at"].notna().any() else date.today()
        max_d = df["created_at"].max().date() if df["created_at"].notna().any() else date.today()

        start_date = col1.date_input("From", value=min_d)
        end_date = col2.date_input("To", value=max_d)

        label_filter = st.multiselect(
            "Risk label",
            options=["Low", "Medium", "High"],
            default=["Low", "Medium", "High"]
        )

    # Apply filters
    mask = (df["created_at"].dt.date >= start_date) & (df["created_at"].dt.date <= end_date)
    df_filtered = df.loc[mask]
    df_filtered = df_filtered[df_filtered["label"].isin(label_filter)]

    # Display
    st.markdown("### Saved Predictions")
    st.dataframe(df_filtered, use_container_width=True)

    # CSV Export
    csv_data = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV Report",
        data=csv_data,
        file_name="heart_risk_prediction_history.csv",
        mime="text/csv"
    )