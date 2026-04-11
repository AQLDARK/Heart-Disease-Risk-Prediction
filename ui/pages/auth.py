import streamlit as st
import logging
from ml.storage import create_user, authenticate_user
from ml.validation import validate_email, validate_password, ValidationError

logger = logging.getLogger(__name__)


def render_auth_page():
    st.title("Welcome")
    st.caption("Login or create an account to use the Heart Risk Platform.")

    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            ok = st.form_submit_button("Login")

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
                    st.success("✅ Login successful.")
                    st.rerun()
                else:
                    logger.warning(f"Failed login attempt for email: {email}")
                    st.error("Invalid email or password.")
            except ValidationError as e:
                st.error(f"❌ {e}")
            except Exception as e:
                logger.error(f"Login error: {e}")
                st.error(f"Login failed: {e}")

    with tab_signup:
        with st.form("signup_form"):
            full_name = st.text_input("Full name")
            email2 = st.text_input("Email", key="signup_email")
            password2 = st.text_input("Password", type="password", key="signup_pw")
            role = st.selectbox("Role", ["Patient", "Clinician / Staff"], index=0)
            ok2 = st.form_submit_button("Create account")

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
                    role="Clinician / Staff" if role.startswith("Clinician") else "Patient"
                )
                logger.info(f"New user created: {email2}")
                st.success("✅ Account created. You can login now.")
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