import streamlit as st

from ml.storage import init_db, get_subscription
from ui.components import inject_dark_css

from ui.pages.predict import render_predict_page
from ui.pages.explain import render_explain_page
from ui.pages.history import render_history_page
from ui.pages.admin_dashboard import render_admin_dashboard
from ui.pages.performance import render_performance_page
from ui.pages.about import render_about_page
from ui.pages.subscription import render_subscription_page  # ✅ NEW
from ui.pages.auth import render_auth_page
from ml.storage import init_db, get_subscription_for_user


def main():
    init_db()

    # If not logged in → show auth page and stop
    if not st.session_state.get("auth"):
        render_auth_page()
        return

    # Logged-in user details
    user = st.session_state["user"]
    user_id = user["user_id"]
    role = user["role"]
    plan = get_subscription_for_user(user_id)

    st.set_page_config(page_title="Heart Disease Risk Prediction System", layout="wide")
    inject_dark_css()

    # ✅ Read current plan from DB
    plan = get_subscription()

    st.title("Heart Disease Risk Prediction System")
    st.caption("Decision-support dashboard — not a medical diagnosis.")

    # ✅ Sidebar
    st.sidebar.title("Access Control")
    role = st.sidebar.selectbox("Select role", ["Patient", "Clinician / Staff", "Administrator"])
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Subscription Plan:** `{plan}`")
    st.sidebar.markdown("Upgrade to unlock more features.")
    st.sidebar.markdown(f"**Logged in as:** {user['full_name']}")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    # ✅ Page list depends on role (platform feel)
    if role == "Patient":
        pages = ["Predict", "Explainability", "Subscription & Billing", "About"]
    elif role == "Clinician / Staff":
        pages = ["Predict", "Explainability", "History", "Subscription & Billing", "About"]
    else:
        pages = ["Predict", "Explainability", "History", "Admin Dashboard", "Model Performance", "Subscription & Billing", "About"]

    page = st.sidebar.radio("Navigate", pages)

    # ✅ Routing + Restrictions
    if page == "Predict":
        render_predict_page(plan=plan)  # ✅ pass plan for PDF gating if you want

    elif page == "Explainability":
        render_explain_page()

    elif page == "History":
        if plan in ["Standard", "Premium"]:
            render_history_page()
        else:
            st.warning("🔒 History is available on **Standard** or **Premium** plans.")
            st.info("Go to **Subscription & Billing** to upgrade.")

    elif page == "Admin Dashboard":
        if plan == "Premium":
            render_admin_dashboard()
        else:
            st.warning("🔒 Admin Analytics is available only on the **Premium** plan.")
            st.info("Go to **Subscription & Billing** to upgrade.")

    elif page == "Model Performance":
        render_performance_page()

    elif page == "Subscription & Billing":
        render_subscription_page()
        st.info("After selecting a plan, refresh the page or re-open the app if needed.")

    elif page == "About":
        render_about_page()


if __name__ == "__main__":
    main()
