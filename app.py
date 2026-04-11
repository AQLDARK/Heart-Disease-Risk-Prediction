import streamlit as st
import logging

from ml.logger import setup_logging, get_logger
from ml.storage import init_db, get_subscription, get_subscription_for_user
from ui.components import inject_dark_css

from ui.pages.predict import render_predict_page
from ui.pages.explain import render_explain_page
from ui.pages.history import render_history_page
from ui.pages.admin_dashboard import render_admin_dashboard
from ui.pages.performance import render_performance_page
from ui.pages.about import render_about_page
from ui.pages.subscription import render_subscription_page
from ui.pages.auth import render_auth_page

# Setup logging
setup_logging(log_level=logging.INFO)
logger = get_logger(__name__)


def main():
    try:
        init_db()
    except Exception as e:
        st.error(f"Failed to initialize database: {e}")
        logger.error(f"Database initialization error: {e}")
        return

    # If not logged in → show auth page and stop
    if not st.session_state.get("auth"):
        render_auth_page()
        return

    # Logged-in user details
    try:
        user = st.session_state.get("user")
        if not user:
            st.error("User session lost. Please log in again.")
            st.session_state.clear()
            st.rerun()
            return
            
        user_id = user.get("user_id")
        role = user.get("role", "Patient")
        plan = get_subscription_for_user(user_id) if user_id else "Free"
    except Exception as e:
        logger.error(f"Failed to retrieve user info: {e}")
        st.error("Failed to retrieve user information. Please log in again.")
        st.session_state.clear()
        st.rerun()
        return

    st.set_page_config(page_title="Heart Disease Risk Prediction System", layout="wide")
    inject_dark_css()

    st.title("Heart Disease Risk Prediction System")
    st.caption("Decision-support dashboard — not a medical diagnosis.")

    # ✅ Sidebar
    st.sidebar.title("Access Control")
    role = st.sidebar.selectbox("Select role", ["Patient", "Clinician / Staff", "Administrator"], 
                                index=["Patient", "Clinician / Staff", "Administrator"].index(role))
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Subscription Plan:** `{plan}`")
    st.sidebar.markdown("Upgrade to unlock more features.")
    st.sidebar.markdown(f"**Logged in as:** {user.get('full_name', 'Unknown')}")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        logger.info(f"User {user.get('email', 'unknown')} logged out")
        st.rerun()

    # ✅ Page list depends on role (platform feel)
    if role == "Patient":
        pages = ["Predict", "Explainability", "Subscription & Billing", "About"]
    elif role == "Clinician / Staff":
        pages = ["Predict", "Explainability", "History", "Subscription & Billing", "About"]
    else:
        pages = ["Predict", "Explainability", "History", "Admin Dashboard", "Model Performance", "Subscription & Billing", "About"]

    page = st.sidebar.radio("Navigate", pages)

    try:
        # ✅ Routing + Restrictions
        if page == "Predict":
            render_predict_page(plan=plan)

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
            
    except Exception as e:
        logger.error(f"Error rendering page '{page}': {e}")
        st.error(f"An error occurred on this page: {e}")


if __name__ == "__main__":
    logger.info("Application started")
    main()
