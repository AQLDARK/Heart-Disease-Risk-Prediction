import streamlit as st
import logging
from ml.storage import create_user, authenticate_user
from ml.validation import validate_email, validate_password, ValidationError
from ui.components import inject_dark_css, info_box

logger = logging.getLogger(__name__)


def render_auth_page():
    # Apply styling
    st.set_page_config(page_title="Heart Disease Risk Prediction", layout="wide")
    inject_dark_css()
    
    # Center content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">❤️</div>
            <h1 style="margin: 0;">Heart Risk AI</h1>
            <p style="color: #9ca3af; font-size: 1.1rem; margin-top: 0.5rem;">
                Intelligent Heart Disease Risk Assessment
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["🔓 Login", "🆕 Sign Up"])

        with tab_login:
            st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)
            with st.form("login_form", border=True):
                email = st.text_input("📧 Email", placeholder="your@email.com")
                password = st.text_input("🔑 Password", type="password", placeholder="••••••••")
                ok = st.form_submit_button("🚀 Login", use_container_width=True)

            if ok:
                if not email or not password:
                    info_box("Email and password are required.", "warning")
                    return
                    
                try:
                    validate_email(email)
                    user = authenticate_user(email, password)
                    if user:
                        st.session_state["auth"] = True
                        st.session_state["user"] = user
                        logger.info(f"User logged in: {email}")
                        info_box("Login successful! Redirecting...", "success")
                        st.rerun()
                    else:
                        logger.warning(f"Failed login attempt for email: {email}")
                        info_box("Invalid email or password. Please try again.", "error")
                except ValidationError as e:
                    info_box(str(e), "error")
                except Exception as e:
                    logger.error(f"Login error: {e}")
                    info_box(f"Login failed: {e}", "error")

        with tab_signup:
            st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)
            with st.form("signup_form", border=True):
                full_name = st.text_input("👤 Full Name", placeholder="John Doe")
                email2 = st.text_input("📧 Email", key="signup_email", placeholder="your@email.com")
                password2 = st.text_input("🔑 Password", type="password", key="signup_pw", placeholder="••••••••")
                role = st.selectbox("👨‍⚕️ Role", ["Patient", "Clinician / Staff"], index=0)
                ok2 = st.form_submit_button("✨ Create Account", use_container_width=True)

            if ok2:
                try:
                    if not full_name or not email2 or not password2:
                        info_box("All fields are required.", "warning")
                        return
                        
                    validate_email(email2)
                    validate_password(password2)
                    
                    create_user(
                        full_name, 
                        email2, 
                        password2, 
                        role="Clinician / Staff" if role.startswith("Clinician") else "Patient"
                    )
                    logger.info(f"New user created: {email2}")
                    info_box("Account created successfully! You can now login.", "success")
                except ValidationError as e:
                    info_box(str(e), "error")
                except ValueError as e:
                    if str(e) == "EMAIL_EXISTS":
                        info_box("This email is already registered. Please login instead.", "warning")
                        logger.warning(f"Signup attempted with existing email: {email2}")
                    else:
                        info_box(f"Signup failed: {e}", "error")
                        logger.error(f"Signup error: {e}")
                except Exception as e:
                    info_box(f"Signup failed: {e}", "error")
                    logger.error(f"Unexpected signup error: {e}")
        
        # Footer
        st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; color: #6b7280; font-size: 0.85rem; padding-top: 2rem; border-top: 1px solid rgba(0, 212, 255, 0.1);">
            <p>🔒 Your data is secure and encrypted | © 2026 Heart Risk AI</p>
        </div>
        """, unsafe_allow_html=True)
