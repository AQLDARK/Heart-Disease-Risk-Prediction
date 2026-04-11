import streamlit as st
import logging
from ml.storage import create_user, authenticate_user
from ml.validation import validate_email, validate_password, ValidationError
from ui.components import inject_modern_css

logger = logging.getLogger(__name__)


def render_auth_page():
    st.set_page_config(
        page_title="CardioPredict - Login",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    inject_modern_css()
    
    # Center the content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            """
            <div style="text-align: center; margin-top: 4rem; margin-bottom: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">❤️</div>
                <h1 style="margin: 0; font-size: 2.5rem;">CardioPredict</h1>
                <p style="color: #94a3b8; font-size: 1.1rem; margin: 0.5rem 0;">Heart Disease Risk Prediction</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.divider()
        
        tab_login, tab_signup = st.tabs(["🔐 Login", "📝 Sign Up"])

        with tab_login:
            st.markdown("### Welcome Back")
            with st.form("login_form"):
                email = st.text_input("Email Address", placeholder="your@email.com")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                ok = st.form_submit_button("🚀 Login", use_container_width=True)

            if ok:
                if not email or not password:
                    st.error("Email and password are required.")
                    return
                    
                try:
                    validate_email(email)
                    user = authenticate_user(email, password)
                    if user:
                        st.session_state["auth"] = True
                        st.session_state["user"] = user
                        logger.info(f"User logged in: {email}")
                        st.success("✅ Login successful. Redirecting...")
                        st.rerun()
                    else:
                        logger.warning(f"Failed login attempt for email: {email}")
                        st.error("❌ Invalid email or password.")
                except ValidationError as e:
                    st.error(f"❌ {e}")
                except Exception as e:
                    logger.error(f"Login error: {e}")
                    st.error(f"❌ Login failed: {e}")

        with tab_signup:
            st.markdown("### Create Account")
            with st.form("signup_form"):
                full_name = st.text_input("Full Name", placeholder="John Doe")
                email2 = st.text_input("Email Address", key="signup_email", placeholder="your@email.com")
                password2 = st.text_input("Password", type="password", key="signup_pw", placeholder="Min 6 characters")
                role = st.selectbox("Account Type", ["👤 Patient", "🏥 Clinician / Staff"], index=0)
                ok2 = st.form_submit_button("📝 Create Account", use_container_width=True)

            if ok2:
                try:
                    if not full_name or not email2 or not password2:
                        st.error("All fields are required.")
                        return
                        
                    validate_email(email2)
                    validate_password(password2)
                    
                    create_user(
                        full_name, 
                        email2, 
                        password2, 
                        role="Clinician / Staff" if role.startswith("🏥") else "Patient"
                    )
                    logger.info(f"New user created: {email2}")
                    st.success("✅ Account created successfully! Please login now.")
                except ValidationError as e:
                    st.error(f"❌ {e}")
                except ValueError as e:
                    if str(e) == "EMAIL_EXISTS":
                        st.error("❌ This email is already registered. Please login instead.")
                        logger.warning(f"Signup attempted with existing email: {email2}")
                    else:
                        st.error(f"❌ Signup failed: {e}")
                        logger.error(f"Signup error: {e}")
                except Exception as e:
                    st.error(f"❌ Signup failed: {e}")
                    logger.error(f"Unexpected signup error: {e}")
        
        st.divider()
        st.markdown(
            """
            <div style="text-align: center; color: #94a3b8; font-size: 0.85rem; margin-top: 2rem;">
            <p>⚕️ Decision-support tool • Not a medical diagnosis</p>
            </div>
            """,
            unsafe_allow_html=True
        )