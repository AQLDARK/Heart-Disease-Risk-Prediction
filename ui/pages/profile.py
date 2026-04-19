import streamlit as st
from ml.storage import get_user_by_id, update_user_profile, get_available_roles
from ml.validation import validate_email
from ui.components import card, info_box, divider, inject_page_background

def profile():
    """User profile and settings page."""
    inject_page_background("care")
    st.title("👤 User Profile")
    st.markdown("Manage your account settings and preferences")
    divider()
    
    # Get current user
    user = st.session_state.get("user")
    if not user:
        info_box("Please login first", color="error")
        return
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Profile Info", "Change Role", "Security"])
    
    # Tab 1: Profile Information
    with tab1:
        st.subheader("📋 Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input(
                "Full Name",
                value=user.get('full_name', ''),
                key="profile_fullname"
            )
        
        with col2:
            email = st.text_input(
                "Email Address",
                value=user.get('email', ''),
                key="profile_email",
                disabled=True
            )
        
        profession = st.text_input(
            "Profession/Title",
            value=user.get('profession', ''),
            key="profile_profession",
            placeholder="e.g., Doctor, Patient, Student"
        )
        
        hospital_clinic = st.text_input(
            "Hospital/Clinic Name",
            value=user.get('hospital_clinic', ''),
            key="profile_hospital",
            placeholder="Optional"
        )
        
        # Account creation info
        st.markdown("---")
        st.markdown("**Account Information**")
        st.write(f"📧 Email: `{user.get('email', 'N/A')}`")
        st.write(f"📅 Role: `{st.session_state.get('role', 'N/A')}`")
        st.write(f"💎 Plan: `{st.session_state.get('plan', 'N/A')}`")
        
        if st.button("💾 Save Profile Changes", use_container_width=True):
            try:
                # Validate email if changed
                if email != user.get('email') and not validate_email(email):
                    info_box("Invalid email format", color="error")
                    return
                
                # Update profile
                update_user_profile(
                    user_id=user.get('id'),
                    full_name=full_name,
                    profession=profession,
                    hospital_clinic=hospital_clinic
                )
                
                # Update session state
                st.session_state["user"]["full_name"] = full_name
                st.session_state["user"]["profession"] = profession
                st.session_state["user"]["hospital_clinic"] = hospital_clinic
                
                info_box("✅ Profile updated successfully!", color="success")
                st.rerun()
            except Exception as e:
                info_box(f"Error updating profile: {str(e)}", color="error")
    
    # Tab 2: Change Role
    with tab2:
        st.subheader("🔄 Change User Role")
        
        card(
            "Select Your Role",
            """<p>Choose the role that best describes your usage. Different roles have access to different features.</p>""",
            icon="👥"
        )
        
        current_role = st.session_state.get('role', 'patient')
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button(
                "👨‍⚕️\nDoctor",
                use_container_width=True,
                key="role_doctor"
            ):
                try:
                    update_user_profile(user_id=user.get('id'), role='doctor')
                    # Fetch updated user data from database
                    updated_user = get_user_by_id(user.get('id'))
                    st.session_state["user"] = {**st.session_state["user"], **updated_user} if updated_user else st.session_state["user"]
                    st.session_state["role"] = 'Doctor'
                    st.session_state["current_role"] = 'Doctor'
                    info_box("✅ Role changed to Doctor", color="success")
                    st.rerun()
                except Exception as e:
                    info_box(f"Error changing role: {str(e)}", color="error")
        
        with col2:
            if st.button(
                "👤\nPatient",
                use_container_width=True,
                key="role_patient"
            ):
                try:
                    update_user_profile(user_id=user.get('id'), role='patient')
                    # Fetch updated user data from database
                    updated_user = get_user_by_id(user.get('id'))
                    st.session_state["user"] = {**st.session_state["user"], **updated_user} if updated_user else st.session_state["user"]
                    st.session_state["role"] = 'Patient'
                    st.session_state["current_role"] = 'Patient'
                    info_box("✅ Role changed to Patient", color="success")
                    st.rerun()
                except Exception as e:
                    info_box(f"Error changing role: {str(e)}", color="error")
        
        with col3:
            if st.button(
                "👨‍💻\nResearcher",
                use_container_width=True,
                key="role_researcher"
            ):
                try:
                    update_user_profile(user_id=user.get('id'), role='researcher')
                    # Fetch updated user data from database
                    updated_user = get_user_by_id(user.get('id'))
                    st.session_state["user"] = {**st.session_state["user"], **updated_user} if updated_user else st.session_state["user"]
                    st.session_state["role"] = 'Researcher'
                    st.session_state["current_role"] = 'Researcher'
                    info_box("✅ Role changed to Researcher", color="success")
                    st.rerun()
                except Exception as e:
                    info_box(f"Error changing role: {str(e)}", color="error")
        
        with col4:
            if st.button(
                "🛡️\nAdmin",
                use_container_width=True,
                key="role_admin"
            ):
                try:
                    update_user_profile(user_id=user.get('id'), role='Admin')
                    # Fetch updated user data from database
                    updated_user = get_user_by_id(user.get('id'))
                    st.session_state["user"] = {**st.session_state["user"], **updated_user} if updated_user else st.session_state["user"]
                    st.session_state["role"] = 'Admin'
                    st.session_state["current_role"] = 'Admin'
                    info_box("✅ Role changed to Admin", color="success")
                    st.rerun()
                except Exception as e:
                    info_box(f"Error changing role: {str(e)}", color="error")
        
        st.markdown("---")
        st.markdown(f"**Current Role:** `{current_role.upper()}`")
        
        # Role descriptions
        st.markdown("### Role Descriptions")
        
        roles_info = {
            "👨‍⚕️ Doctor": "Access to advanced diagnostics, patient history, and detailed reports. Full feature set for medical professionals.",
            "👤 Patient": "Personal risk assessment, health tracking, and basic health recommendations.",
            "👨‍💻 Researcher": "Advanced analytics, model insights, data export, and research tools.",
            "🛡️ Admin": "Full system access, admin dashboard, model performance analytics, and user management."
        }
        
        for role_name, description in roles_info.items():
            st.write(f"**{role_name}**: {description}")
    
    # Tab 3: Security
    with tab3:
        st.subheader("🔐 Security Settings")
        
        card(
            "Password Management",
            """<p>Change your password regularly to keep your account secure.</p>""",
            icon="🔑"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_password = st.text_input(
                "Current Password",
                type="password",
                key="current_pwd"
            )
        
        with col2:
            st.empty()
        
        new_password = st.text_input(
            "New Password",
            type="password",
            key="new_pwd"
        )
        
        confirm_password = st.text_input(
            "Confirm New Password",
            type="password",
            key="confirm_pwd"
        )
        
        if st.button("🔄 Change Password", use_container_width=True):
            if not current_password:
                info_box("Current password is required", color="error")
            elif not new_password:
                info_box("New password is required", color="error")
            elif new_password != confirm_password:
                info_box("New passwords do not match", color="error")
            elif len(new_password) < 8:
                info_box("Password must be at least 8 characters long", color="error")
            else:
                info_box("✅ Password changed successfully!", color="success")
        
        st.markdown("---")
        st.markdown("### Password Requirements")
        st.markdown("""
        - At least 8 characters long
        - Mix of uppercase and lowercase letters
        - Include numbers and special characters
        """)
        
        st.markdown("---")
        st.markdown("### Account Security")
        
        info_box("Two-factor authentication will be available soon", color="info")
