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
from ui.pages.model_comparison import render_model_comparison
from ui.pages.about import render_about_page
from ui.pages.subscription import render_subscription_page
from ui.pages.auth import render_auth_page
from ui.pages.profile import profile
from ui.pages.payment_history import render_payment_history_page

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
        pages = ["Predict", "Explainability", "History", "Subscription & Billing", "Profile", "About"]
    elif role == "Doctor":
        pages = ["Predict", "Explainability", "History", "Subscription & Billing", "Profile", "About", "Model Performance"]
    elif role == "Researcher":
        pages = ["Explainability", "Model Performance", "Model Comparison", "Profile", "About"]
    elif role == "Admin":
        pages = ["Admin Dashboard", "Model Performance", "Model Comparison", "Payment History", "History", "Profile", "About"]
    else:
        pages = ["Predict", "Explainability", "History", "Profile", "About"]

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
        # ✅ Routing + Role-Based Access Control
        
        # Define allowed roles per page
        role_access = {
            "Predict": ["Patient", "Doctor"],
            "Explainability": ["Patient", "Doctor", "Researcher"],
            "History": ["Patient", "Doctor", "Admin"],
            "Subscription & Billing": ["Patient", "Doctor"],
            "Profile": ["Patient", "Doctor", "Researcher", "Admin"],
            "About": ["Patient", "Doctor", "Researcher", "Admin"],
            "Model Performance": ["Doctor", "Researcher", "Admin"],
            "Model Comparison": ["Researcher", "Admin"],
            "Admin Dashboard": ["Admin"],
            "Payment History": ["Admin"],
        }
        
        # Check access
        allowed_roles = role_access.get(current_page, [])
        
        if current_page not in role_access:
            st.error(f"❌ **Access Denied** - Page not found: {current_page}")
            logger.warning(f"User {user.get('email')} attempted to access non-existent page: {current_page}")
        
        elif role not in allowed_roles:
            st.error(f"❌ **Access Denied** - You don't have permission to view this page.")
            st.info(f"📌 **Your Role:** {role}\n\n**Allowed Roles:** {', '.join(allowed_roles)}")
            logger.warning(f"Unauthorized access attempt by {user.get('email')} (role: {role}) to page: {current_page}")
        
        elif current_page == "Predict":
            render_predict_page(plan=plan)

        elif current_page == "Explainability":
            render_explain_page()

        elif current_page == "History":
            render_history_page(role=role)

        elif current_page == "Admin Dashboard":
            render_admin_dashboard()

        elif current_page == "Model Performance":
            render_performance_page()

        elif current_page == "Model Comparison":
            render_model_comparison()

        elif current_page == "Payment History":
            render_payment_history_page()

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
