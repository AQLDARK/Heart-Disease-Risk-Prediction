import streamlit as st
from ml.storage import get_subscription, set_subscription
from ml.storage import get_subscription_for_user, set_subscription_for_user


    

def render_subscription_page():
    user = st.session_state["user"]
    user_id = user["user_id"]

    current_plan = get_subscription_for_user(user_id)

    st.subheader("Subscription & Billing")
    st.caption("Mock payment interface — no real transactions.")

    st.markdown(f"### Current Plan: **{current_plan}**")
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Free")
        st.write("• Basic prediction")
        st.write("• No history access")
        if st.button("Activate Free", key="plan_free"):
            set_subscription_for_user(user_id, "Free")
            st.success("Free plan activated.")
            st.rerun()

    with col2:
        st.markdown("### Standard")
        st.write("• Prediction history")
        st.write("• CSV export")
        if st.button("Activate Standard", key="plan_standard"):
            set_subscription_for_user(user_id, "Standard")
            st.success("Standard plan activated.")
            st.rerun()

    with col3:
        st.markdown("### Premium")
        st.write("• Admin analytics")
        st.write("• Global SHAP insights")
        st.write("• PDF reports")
        if st.button("Activate Premium", key="plan_premium"):
            set_subscription_for_user(user_id, "Premium")
            st.success("Premium plan activated.")
            st.rerun()
