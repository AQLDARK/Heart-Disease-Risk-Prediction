import streamlit as st
import logging
from ml.storage import create_user, authenticate_user
from ml.validation import validate_email, validate_password, ValidationError
from ui.components import inject_dark_css, info_box

logger = logging.getLogger(__name__)


def inject_auth_premium_background():
    """Inject premium healthcare background for login/signup page."""
    st.markdown(
        """
        <style>
        /* Premium Healthcare Auth Background */
        .stApp {
            background: linear-gradient(135deg, #001f3f 0%, #003d5c 50%, #004d73 100%);
            background-attachment: fixed;
            background-size: cover;
        }
        
        /* Medical hero pattern overlay */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: 
                radial-gradient(circle at 20% 50%, rgba(0, 212, 255, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(34, 197, 94, 0.08) 0%, transparent 50%),
                url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"><defs><pattern id="medical" x="0" y="0" width="300" height="300" patternUnits="userSpaceOnUse"><circle cx="150" cy="150" r="100" stroke="rgba(0,212,255,0.04)" fill="none" stroke-width="1"/><path d="M80,150 Q150,100 220,150 T280,150" stroke="rgba(0,212,255,0.05)" fill="none" stroke-width="1.5"/><circle cx="100" cy="100" r="8" fill="rgba(34,197,94,0.06)"/><circle cx="200" cy="200" r="6" fill="rgba(0,212,255,0.06)"/><rect x="130" y="130" width="40" height="40" stroke="rgba(0,212,255,0.04)" fill="none"/></pattern></defs><rect width="1200" height="800" fill="url(%23medical)"/></svg>');
            background-attachment: fixed;
            pointer-events: none;
            z-index: 0;
        }
        
        /* Main content positioning */
        .main {
            position: relative;
            z-index: 1;
        }
        
        /* Hero section styling */
        .hero-section {
            background: linear-gradient(180deg, rgba(0, 50, 100, 0.7) 0%, rgba(0, 77, 115, 0.8) 100%);
            border-radius: 20px;
            padding: 2.5rem;
            margin: 2rem 0;
            border: 1px solid rgba(0, 212, 255, 0.3);
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 0 20px rgba(0, 212, 255, 0.1);
        }
        
        /* Auth form styling */
        .auth-form {
            background: linear-gradient(135deg, rgba(15, 20, 35, 0.95) 0%, rgba(25, 40, 60, 0.95) 100%);
            border-radius: 16px;
            padding: 2rem;
            border: 2px solid rgba(0, 212, 255, 0.2);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(15px);
        }
        
        /* Medical accent colors */
        .medical-blue { color: #00d4ff; }
        .medical-green { color: #22c55e; }
        .medical-accent { color: #0099ff; }
        
        /* Tab styling for auth */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(0, 30, 60, 0.8);
            border-radius: 12px;
            padding: 0.5rem;
            border: 1px solid rgba(0, 212, 255, 0.2);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(0, 50, 100, 0.5);
            border-radius: 8px;
            color: #9ca3af;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.2) 0%, rgba(0, 153, 255, 0.1) 100%);
            color: #00d4ff;
            border: 1px solid rgba(0, 212, 255, 0.4);
        }
        
        /* Form input styling */
        .stTextInput input, .stSelectbox select {
            background: rgba(0, 50, 100, 0.6) !important;
            border: 1px solid rgba(0, 212, 255, 0.2) !important;
            color: #ffffff !important;
            border-radius: 8px !important;
            padding: 0.75rem !important;
            transition: all 0.3s ease;
        }
        
        .stTextInput input:focus, .stSelectbox select:focus {
            border-color: rgba(0, 212, 255, 0.6) !important;
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.2) !important;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
            color: #000;
            font-weight: 700;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 212, 255, 0.4);
        }
        
        /* Footer styling */
        .auth-footer {
            text-align: center;
            color: #6b7280;
            font-size: 0.85rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(0, 212, 255, 0.1);
            margin-top: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_auth_page():
    # Apply styling
    st.set_page_config(page_title="Heart Disease Risk Prediction", layout="wide")
    inject_dark_css()
    inject_auth_premium_background()
    
    # Center content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="hero-section" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">❤️</div>
            <h1 style="margin: 0; font-size: 2.5rem;">Heart Risk AI</h1>
            <p style="color: #9ca3af; font-size: 1.1rem; margin-top: 0.5rem;">
                Intelligent Heart Disease Risk Assessment
            </p>
            <p style="color: #00d4ff; font-size: 0.95rem; margin-top: 1rem; font-weight: 500;">
                🏥 Premium Healthcare Analytics Platform
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["🔓 Login", "🆕 Sign Up"])

        with tab_login:
            st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)
            st.markdown("**Select your role to login:**")
            with st.form("login_form", border=True):
                # Role selection for login
                role_options = ["Patient", "Doctor", "Researcher", "Admin"]
                selected_role = st.selectbox(
                    "👥 Select Role",
                    role_options,
                    index=0,
                    help="Choose your role in the healthcare system"
                )
                
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
                        # Verify role matches
                        if user["role"] != selected_role:
                            info_box(
                                f"Role mismatch! Your account is registered as '{user['role']}', not '{selected_role}'.",
                                "warning"
                            )
                            logger.warning(f"Login role mismatch for {email}: attempted {selected_role}, actual {user['role']}")
                            return
                        
                        st.session_state["auth"] = True
                        st.session_state["user"] = user
                        st.session_state["role"] = selected_role
                        logger.info(f"User logged in: {email} (Role: {selected_role})")
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
            st.markdown("**Create your account by selecting your role:**")
            with st.form("signup_form", border=True):
                full_name = st.text_input("👤 Full Name", placeholder="John Doe")
                email2 = st.text_input("📧 Email", key="signup_email", placeholder="your@email.com")
                
                # Enhanced role selection for signup with descriptions
                role_options = ["Patient", "Doctor", "Researcher", "Admin"]
                role_descriptions = {
                    "Patient": "Individual getting health assessment",
                    "Doctor": "Medical professional providing clinical guidance",
                    "Researcher": "Healthcare researcher for studies and analysis",
                    "Admin": "System administrator with full access"
                }
                
                selected_role = st.selectbox(
                    "👥 Select Your Role",
                    role_options,
                    index=0,
                    help="Choose your role in the healthcare system"
                )
                st.caption(f"ℹ️ {role_descriptions[selected_role]}")
                
                password2 = st.text_input("🔑 Password", type="password", key="signup_pw", placeholder="••••••••")
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
                        role=selected_role
                    )
                    logger.info(f"New user created: {email2} (Role: {selected_role})")
                    info_box(f"Account created successfully as '{selected_role}'! You can now login.", "success")
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
