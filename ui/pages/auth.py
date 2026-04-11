import streamlit as st
from ml.storage import create_user, authenticate_user

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
            user = authenticate_user(email, password)
            if user:
                st.session_state["auth"] = True
                st.session_state["user"] = user
                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Invalid email or password.")

    with tab_signup:
        with st.form("signup_form"):
            full_name = st.text_input("Full name")
            email2 = st.text_input("Email", key="signup_email")
            password2 = st.text_input("Password", type="password", key="signup_pw")
            role = st.selectbox("Role", ["Patient", "Clinician / Staff"], index=0)
            ok2 = st.form_submit_button("Create account")

        if ok2:
            if len(password2) < 6:
                st.error("Password must be at least 6 characters.")
                return
            try:
                create_user(full_name, email2, password2, role="Clinician / Staff" if role.startswith("Clinician") else "Patient")
                st.success("Account created. You can login now.")
            except ValueError as e:
                if str(e) == "EMAIL_EXISTS":
                    st.error("This email is already registered. Please login instead.")
                else:
                    st.error("Signup failed. Please try again.")