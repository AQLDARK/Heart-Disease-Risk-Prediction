import streamlit as st
import logging

from ml.logger import setup_logging, get_logger
from ml.storage import init_db, get_subscription, get_subscription_for_user
from ui.components import inject_dark_css, render_top_navbar

from ui.pages.predict import render_predict_page
from ui.pages.explain import render_explain_page
from ui.pages.history import render_history_page
from ui.pages.admin_dashboard import render_admin_dashboard
from ui.pages.performance import render_performance_page
from ui.pages.about import render_about_page
from ui.pages.subscription import render_subscription_page
from ui.pages.auth import render_auth_page
from ui.pages.profile import profile

# Setup logging
setup_logging(log_level=logging.INFO)
logger = get_logger(__name__)


def main():
    # Set page config at the very start
    st.set_page_config(
        page_title="Heart Disease Risk Prediction System",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply CSS immediately
    inject_dark_css()
    
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
        # Get role from session state (updated by profile page) or from user data
        role = st.session_state.get("role", st.session_state.get("current_role", user.get("role", "Patient")))
        plan = get_subscription_for_user(user_id) if user_id else "Free"
    except Exception as e:
        logger.error(f"Failed to retrieve user info: {e}")
        st.error("Failed to retrieve user information. Please log in again.")
        st.session_state.clear()
        st.rerun()
        return

    # Initialize current_page in session state
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Predict"

    # ✅ Page list depends on role
    if role == "Patient":
        pages = ["Predict", "Explainability", "Subscription & Billing", "Profile", "About"]
    elif role == "Clinician / Staff" or role == "Doctor":
        pages = ["Predict", "Explainability", "History", "Subscription & Billing", "Profile", "About"]
    elif role == "Administrator":
        pages = ["Predict", "Explainability", "History", "Admin Dashboard", "Model Performance", "Subscription & Billing", "Profile", "About"]
    else:
        pages = ["Predict", "Explainability", "History", "Subscription & Billing", "Profile", "About"]

    current_page = st.session_state.get("current_page", "Predict")
    
    # Handle logout
    def on_logout():
        st.session_state.clear()
        logger.info(f"User {user.get('email', 'unknown')} logged out")
    
    def on_role_change(new_role):
        st.session_state["current_role"] = new_role
        st.rerun()

    # Render top navigation
    st.markdown("")  # Small spacing
    render_top_navbar(current_page, pages, user, plan, role, on_logout, on_role_change)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Main content area
    st.markdown("")  # Spacing
    
    try:
        # ✅ Routing + Restrictions based on plan
        if current_page == "Predict":
            render_predict_page(plan=plan)

        elif current_page == "Explainability":
            # Explainability available on Standard and Premium
            if plan in ["Standard", "Premium"]:
                render_explain_page()
            else:
                st.warning("🔒 Explainability is available on **Standard** or **Premium** plans.")
                st.info("Upgrade your plan in **Subscription & Billing** to access detailed explanations.")

        elif current_page == "History":
            # History available on Standard and Premium
            if plan in ["Standard", "Premium"]:
                render_history_page()
            else:
                st.warning("🔒 Prediction History is available on **Standard** or **Premium** plans.")
                st.info("Upgrade your plan in **Subscription & Billing** to view your prediction history.")

        elif current_page == "Admin Dashboard":
            # Admin Dashboard only for Premium + Administrator role
            if plan == "Premium" and role == "Administrator":
                render_admin_dashboard()
            elif role != "Administrator":
                st.warning("🔒 Admin Dashboard is available only for Administrators.")
                st.info("Go to **Profile** to change your role to Administrator.")
            else:
                st.warning("🔒 Admin Dashboard is available on **Premium** plan.")
                st.info("Upgrade your plan in **Subscription & Billing** to access admin analytics.")

        elif current_page == "Model Performance":
            # Model Performance only for Premium + Administrator role
            if plan == "Premium" and role == "Administrator":
                render_performance_page()
            elif role != "Administrator":
                st.warning("🔒 Model Performance is available only for Administrators.")
                st.info("Go to **Profile** to change your role to Administrator.")
            else:
                st.warning("🔒 Model Performance is available on **Premium** plan.")
                st.info("Upgrade your plan in **Subscription & Billing** to access model analytics.")

        elif current_page == "Subscription & Billing":
            render_subscription_page()

        elif current_page == "Profile":
            profile()

        elif current_page == "About":
            render_about_page()
            
    except Exception as e:
        logger.error(f"Error rendering page '{current_page}': {e}")
        st.error(f"An error occurred on this page: {e}")


if __name__ == "__main__":
    logger.info("Application started")
    main()
