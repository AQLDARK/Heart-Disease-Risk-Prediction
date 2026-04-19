import streamlit as st
import pandas as pd
from datetime import date, timedelta
import logging

from ml.storage import get_all_transactions
from ui.components import divider, info_box, inject_page_background

logger = logging.getLogger(__name__)


def render_payment_history_page():
    """Render admin payment history page with filtering by date."""
    inject_page_background("analytics")
    st.title("💳 Payment History")
    st.markdown("View and manage all system transactions")
    divider()

    # Load all transactions
    transactions = get_all_transactions(limit=5000)

    if not transactions:
        st.info("No transactions found in the system.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(transactions)
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    # ============================================
    # Filtering Section
    # ============================================
    st.markdown("### 🔍 Filters")

    with st.expander("Date & Status Filters", expanded=True):
        col1, col2, col3 = st.columns(3)

        # Date range selection
        with col1:
            min_date = df["created_at"].min().date() if df["created_at"].notna().any() else date.today()
            max_date = df["created_at"].max().date() if df["created_at"].notna().any() else date.today()

            start_date = st.date_input("From Date", value=min_date, min_value=min_date, max_value=max_date)

        with col2:
            end_date = st.date_input("To Date", value=max_date, min_value=min_date, max_value=max_date)

        with col3:
            status_filter = st.multiselect(
                "Payment Status",
                options=df["status"].unique().tolist() if "status" in df.columns else ["completed"],
                default=df["status"].unique().tolist() if "status" in df.columns else ["completed"],
                help="Filter by transaction status"
            )

        # Payment method filter
        col4, col5 = st.columns(2)

        with col4:
            plan_filter = st.multiselect(
                "Plan Type",
                options=df["plan"].unique().tolist() if "plan" in df.columns else ["Free", "Standard", "Premium"],
                default=df["plan"].unique().tolist() if "plan" in df.columns else ["Free", "Standard", "Premium"],
                help="Filter by subscription plan"
            )

        with col5:
            payment_method_filter = st.multiselect(
                "Payment Method",
                options=df["payment_method"].unique().tolist() if "payment_method" in df.columns else ["Credit Card"],
                default=df["payment_method"].unique().tolist() if "payment_method" in df.columns else ["Credit Card"],
                help="Filter by payment method"
            )

    # Apply filters
    df_filtered = df[
        (df["created_at"].dt.date >= start_date) &
        (df["created_at"].dt.date <= end_date) &
        (df["status"].isin(status_filter)) &
        (df["plan"].isin(plan_filter)) &
        (df["payment_method"].isin(payment_method_filter))
    ].copy()

    # ============================================
    # Summary Statistics
    # ============================================
    st.markdown("### 📊 Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Transactions", len(df_filtered))

    with col2:
        total_revenue = df_filtered["amount"].sum() if "amount" in df_filtered.columns else 0
        st.metric("Total Revenue", f"${total_revenue:,.2f}")

    with col3:
        completed_count = len(df_filtered[df_filtered["status"] == "completed"]) if "status" in df_filtered.columns else 0
        st.metric("Completed", completed_count)

    with col4:
        avg_transaction = df_filtered["amount"].mean() if "amount" in df_filtered.columns and len(df_filtered) > 0 else 0
        st.metric("Avg Transaction", f"${avg_transaction:,.2f}")

    st.divider()

    # ============================================
    # Transactions Table
    # ============================================
    st.markdown("### 📋 Transactions")

    if df_filtered.empty:
        st.info("No transactions match the selected filters.")
    else:
        # Prepare display dataframe
        display_df = df_filtered[[
            "created_at", "user_name", "user_email", "plan", "amount", 
            "currency", "payment_method", "status", "transaction_id", "invoice_id"
        ]].copy()

        # Format datetime
        display_df["created_at"] = display_df["created_at"].dt.strftime("%Y-%m-%d %H:%M:%S")

        # Rename columns for display
        display_df.columns = [
            "Date & Time", "User Name", "Email", "Plan", "Amount",
            "Currency", "Payment Method", "Status", "Transaction ID", "Invoice ID"
        ]

        # Display dataframe with height
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=min(400, len(display_df) * 35 + 100)
        )

        st.divider()

        # ============================================
        # Export Options
        # ============================================
        st.markdown("### 📥 Export Data")

        col1, col2, col3 = st.columns(3)

        # CSV Export
        with col1:
            csv_data = display_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"payment_history_{start_date}_{end_date}.csv",
                mime="text/csv",
                use_container_width=True
            )

        # Excel Export (if available)
        with col2:
            try:
                import openpyxl
                from io import BytesIO

                output = BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    display_df.to_excel(writer, sheet_name="Transactions", index=False)
                excel_data = output.getvalue()

                st.download_button(
                    label="📊 Download Excel",
                    data=excel_data,
                    file_name=f"payment_history_{start_date}_{end_date}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except ImportError:
                st.info("Excel export requires openpyxl library")

        with col3:
            st.markdown(f"**Showing {len(display_df)} of {len(df)} total transactions**")

    # ============================================
    # Revenue Analytics
    # ============================================
    st.markdown("### 💰 Revenue Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Revenue by Plan**")
        if "plan" in df_filtered.columns and "amount" in df_filtered.columns:
            revenue_by_plan = df_filtered.groupby("plan")["amount"].sum().sort_values(ascending=False)
            st.bar_chart(revenue_by_plan)
        else:
            st.info("No plan data available")

    with col2:
        st.markdown("**Revenue by Payment Method**")
        if "payment_method" in df_filtered.columns and "amount" in df_filtered.columns:
            revenue_by_method = df_filtered.groupby("payment_method")["amount"].sum().sort_values(ascending=False)
            st.bar_chart(revenue_by_method)
        else:
            st.info("No payment method data available")

    st.divider()

    # ============================================
    # Footer
    # ============================================
    st.caption(
        "💡 **Admin Note:** This view shows all payment transactions in the system. "
        "Use filters to search for specific date ranges or payment methods. "
        f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
