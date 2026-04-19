import streamlit as st

def inject_premium_background():
    """Inject premium healthcare background images for all pages."""
    st.markdown(
        """
        <style>
        /* Premium Healthcare Background */
        .stApp {
            background-image: 
                linear-gradient(135deg, rgba(15, 20, 25, 0.92) 0%, rgba(26, 31, 46, 0.92) 100%),
                url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"><defs><pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M 60 0 L 0 0 0 60" fill="none" stroke="rgba(0,212,255,0.03)" stroke-width="1"/></pattern><pattern id="dots" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="2" fill="rgba(0,212,255,0.08)"/></pattern></defs><rect width="1200" height="800" fill="url(%23grid)"/><rect width="1200" height="800" fill="url(%23dots)"/></svg>');
            background-attachment: fixed;
            background-size: cover, 100px 100px;
            background-position: center, 0 0;
            color: #e6e8ee;
        }
        
        /* Medical theme elements */
        .medical-accent {
            color: #00d4ff;
            font-weight: 600;
        }
        
        .health-gradient {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(34, 197, 94, 0.1) 100%);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid rgba(0, 212, 255, 0.2);
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def inject_page_background(theme="medical"):
    """Inject specific page background based on theme type.
    
    Args:
        theme: Type of background - "medical", "analytics", "secure", "care"
    """
    backgrounds = {
        "medical": """
        <style>
        .page-container {
            background: linear-gradient(135deg, rgba(15, 20, 25, 0.95) 0%, rgba(20, 25, 40, 0.95) 100%),
                        url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><pattern id="heartbeat" x="0" y="0" width="200" height="200" patternUnits="userSpaceOnUse"><path d="M10,100 L50,80 L70,120 L110,40 L150,100 L190,100" stroke="rgba(0,212,255,0.05)" stroke-width="2" fill="none"/></pattern></defs><rect width="1000" height="1000" fill="url(%23heartbeat)"/></svg>');
            background-attachment: fixed;
        }
        </style>
        """,
        "analytics": """
        <style>
        .page-container {
            background: linear-gradient(135deg, rgba(15, 20, 25, 0.95) 0%, rgba(25, 35, 50, 0.95) 100%),
                        url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><pattern id="analytics" x="0" y="0" width="150" height="150" patternUnits="userSpaceOnUse"><circle cx="30" cy="30" r="2" fill="rgba(0,212,255,0.1)"/><line x1="30" y1="50" x2="80" y2="80" stroke="rgba(34,197,94,0.08)" stroke-width="1"/></pattern></defs><rect width="1000" height="1000" fill="url(%23analytics)"/></svg>');
            background-attachment: fixed;
        }
        </style>
        """,
        "secure": """
        <style>
        .page-container {
            background: linear-gradient(135deg, rgba(15, 20, 25, 0.95) 0%, rgba(30, 20, 40, 0.95) 100%),
                        url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><pattern id="secure" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M50,10 L90,30 L90,60 Q50,85 10,60 L10,30 Z" stroke="rgba(0,212,255,0.08)" fill="none" stroke-width="1.5"/></pattern></defs><rect width="1000" height="1000" fill="url(%23secure)"/></svg>');
            background-attachment: fixed;
        }
        </style>
        """,
        "care": """
        <style>
        .page-container {
            background: linear-gradient(135deg, rgba(15, 20, 25, 0.95) 0%, rgba(20, 30, 35, 0.95) 100%),
                        url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><pattern id="care" x="0" y="0" width="180" height="180" patternUnits="userSpaceOnUse"><circle cx="90" cy="90" r="60" stroke="rgba(34,197,94,0.08)" fill="none" stroke-width="1"/><circle cx="90" cy="90" r="40" stroke="rgba(0,212,255,0.08)" fill="none" stroke-width="1"/></pattern></defs><rect width="1000" height="1000" fill="url(%23care)"/></svg>');
            background-attachment: fixed;
        }
        </style>
        """
    }
    
    selected_bg = backgrounds.get(theme, backgrounds["medical"])
    st.markdown(selected_bg, unsafe_allow_html=True)


def inject_dark_css():
    """Inject modern, attractive dark theme with gradients and animations."""
    st.markdown(
        """
        <style>
        /* ============ Global Styles ============ */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        .stApp { 
            background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
            color: #e6e8ee;
        }
        
        /* ============ Typography ============ */
        h1 {
            color: #ffffff;
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }
        
        h2 {
            color: #ffffff;
            font-size: 1.8rem;
            font-weight: 600;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
        }
        
        h3 {
            color: #00d4ff;
            font-size: 1.3rem;
            font-weight: 600;
        }
        
        h4 { color: #ffffff; font-weight: 600; }
        
        /* ============ Top Navigation ============ */
        .navbar {
            background: rgba(10, 15, 25, 0.8);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(0, 212, 255, 0.2);
            padding: 1rem 1.5rem;
            position: sticky;
            top: 3.5rem;
            z-index: 999;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .navbar-brand {
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .navbar-menu {
            display: flex;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .nav-item {
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.95rem;
            font-weight: 500;
            border: 1px solid transparent;
            color: #e6e8ee;
        }
        
        .nav-item:hover {
            background: rgba(0, 212, 255, 0.1);
            border-color: rgba(0, 212, 255, 0.3);
            color: #00d4ff;
        }
        
        .nav-item.active {
            background: rgba(0, 212, 255, 0.2);
            border-color: #00d4ff;
            color: #00d4ff;
        }
        
        /* ============ Cards & Containers ============ */
        .card {
            background: rgba(30, 45, 80, 0.3);
            border: 1px solid rgba(0, 212, 255, 0.15);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        .card:hover {
            border-color: rgba(0, 212, 255, 0.4);
            box-shadow: 0 12px 40px rgba(0, 212, 255, 0.15);
            transform: translateY(-2px);
        }
        
        .card-title {
            color: #00d4ff;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.8rem;
        }
        
        .card-body {
            color: #c5c7d0;
            font-size: 0.95rem;
            line-height: 1.6;
        }
        
        /* ============ Badges & Pills ============ */
        .badge {
            display: inline-block;
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            text-align: center;
            margin: 0.2rem;
        }
        
        .badge-low {
            background: rgba(34, 197, 94, 0.2);
            color: #22c55e;
            border: 1px solid rgba(34, 197, 94, 0.4);
        }
        
        .badge-medium {
            background: rgba(249, 115, 22, 0.2);
            color: #f97316;
            border: 1px solid rgba(249, 115, 22, 0.4);
        }
        
        .badge-high {
            background: rgba(239, 68, 68, 0.2);
            color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.4);
        }
        
        /* ============ Buttons ============ */
        .stButton > button {
            background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
        }
        
        .stButton > button:hover {
            box-shadow: 0 6px 25px rgba(0, 212, 255, 0.5);
            transform: translateY(-2px);
        }
        
        /* ============ Inputs ============ */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {
            background: rgba(30, 45, 80, 0.5) !important;
            border: 1px solid rgba(0, 212, 255, 0.2) !important;
            color: #e6e8ee !important;
            border-radius: 8px;
            padding: 0.6rem;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #00d4ff !important;
            box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.2) !important;
        }
        
        /* ============ Metrics ============ */
        .metric {
            background: rgba(30, 45, 80, 0.4);
            border-left: 3px solid #00d4ff;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #00d4ff;
        }
        
        .metric-label {
            color: #9ca3af;
            font-size: 0.9rem;
            margin-top: 0.3rem;
        }
        
        /* ============ Alerts ============ */
        .stAlert {
            border-radius: 8px;
            border-left: 4px solid;
        }
        
        .stSuccess { 
            background: rgba(34, 197, 94, 0.1) !important;
            border-left-color: #22c55e !important;
        }
        
        .stWarning {
            background: rgba(249, 115, 22, 0.1) !important;
            border-left-color: #f97316 !important;
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.1) !important;
            border-left-color: #ef4444 !important;
        }
        
        .stInfo {
            background: rgba(0, 212, 255, 0.1) !important;
            border-left-color: #00d4ff !important;
        }
        
        /* ============ Forms ============ */
        .stForm {
            background: rgba(30, 45, 80, 0.25);
            border: 1px solid rgba(0, 212, 255, 0.15);
            border-radius: 12px;
            padding: 2rem;
        }
        
        /* ============ Tables ============ */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
        }
        
        /* ============ Block Container ============ */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
        }
        
        /* ============ Utility Classes ============ */
        .muted { 
            color: rgba(230, 232, 238, 0.7);
            font-size: 0.9rem;
        }
        
        .divider {
            border-bottom: 1px solid rgba(0, 212, 255, 0.2);
            margin: 1.5rem 0;
        }
        
        /* ============ Responsive ============ */
        @media (max-width: 768px) {
            .navbar {
                flex-direction: column;
                gap: 1rem;
            }
            
            h1 { font-size: 1.8rem; }
            h2 { font-size: 1.4rem; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_top_navbar(current_page: str, pages: list, user: dict, plan: str, role: str, on_logout, on_role_change):
    """Render professional top navigation bar with proper Streamlit layout."""
    
    # Create navbar container with proper styling
    st.markdown("""
    <div style="
        background: linear-gradient(90deg, rgba(10, 15, 25, 0.95) 0%, rgba(20, 30, 50, 0.92) 100%);
        border-bottom: 2px solid rgba(0, 212, 255, 0.4);
        border-radius: 12px;
        padding: 1.2rem 2rem;
        margin: 0 0 2rem 0;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1);
        backdrop-filter: blur(10px);
    ">
    """, unsafe_allow_html=True)
    
    # Header row with brand, search space, and user info
    header_cols = st.columns([2, 3, 2])
    
    # Brand/Logo Column
    with header_cols[0]:
        st.markdown("""
        <div style="
            font-size: 1.4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.5px;
        ">❤️ HeartRisk.AI</div>
        """, unsafe_allow_html=True)
    
    # Middle spacer
    with header_cols[1]:
        pass
    
    # User info Column
    with header_cols[2]:
        st.markdown(f"""
        <div style="
            text-align: right;
            background: rgba(0, 212, 255, 0.05);
            padding: 0.8rem 1rem;
            border-radius: 8px;
            border: 1px solid rgba(0, 212, 255, 0.15);
        ">
            <div style="color: #9ca3af; font-size: 0.75rem; font-weight: 500; letter-spacing: 0.5px;">USER PROFILE</div>
            <div style="color: #00d4ff; font-weight: 700; font-size: 1rem; margin: 0.2rem 0;">{user.get('full_name', 'User')}</div>
            <div style="color: #6b7280; font-size: 0.8rem;">📊 {plan} • 👤 {role}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation separator
    st.markdown('<div style="height: 0.8rem;"></div>', unsafe_allow_html=True)
    
    # Navigation buttons row
    nav_cols = st.columns([0.15] + [1.2] * len(pages) + [0.8])
    
    # Left spacing
    with nav_cols[0]:
        pass
    
    # Navigation buttons
    for idx, page in enumerate(pages):
        with nav_cols[idx + 1]:
            is_active = current_page == page
            button_label = f"✓ {page}" if is_active else f"📍 {page}"
            
            if st.button(
                label=button_label,
                key=f"nav_{page}_{idx}",
                use_container_width=True,
                help=f"Navigate to {page} page"
            ):
                st.session_state["current_page"] = page
                st.rerun()
    
    # Right action buttons column
    with nav_cols[-1]:
        col_logout, col_profile = st.columns(2)
        
        with col_logout:
            if st.button("🚪", key="logout_btn", help="Logout from the application", use_container_width=True):
                on_logout()
                st.rerun()
        
        with col_profile:
            if st.button("⚙️", key="settings_btn", help="User settings", use_container_width=True):
                pass  # Can be extended for settings page
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="margin-top: 0.5rem;"></div>', unsafe_allow_html=True)


def risk_badge(label: str) -> str:
    """Return HTML badge for risk level with modern styling."""
    if label == "Low":
        return '<span class="badge badge-low">🟢 Low Risk</span>'
    elif label == "Medium":
        return '<span class="badge badge-medium">🟠 Medium Risk</span>'
    else:
        return '<span class="badge badge-high">🔴 High Risk</span>'


def stat_card(title: str, value: str, unit: str = "", icon: str = "📊"):
    """Render a modern metric card."""
    st.markdown(f"""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <div class="card-title">{title}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{unit}</div>
            </div>
            <div style="font-size: 2rem;">{icon}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def card(title: str, body_html: str, icon: str = ""):
    """Render a modern card with optional icon."""
    st.markdown(f"""
    <div class="card">
        <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1rem;">
            <div style="font-size: 1.5rem;">{icon}</div>
            <h4 style="margin: 0;">{title}</h4>
        </div>
        <div class="card-body">{body_html}</div>
    </div>
    """, unsafe_allow_html=True)


def info_box(text: str, color: str = "info"):
    """Render info/warning/success box."""
    colors = {
        "success": ("🟢", "#22c55e", "rgba(34, 197, 94, 0.1)"),
        "warning": ("🟠", "#f97316", "rgba(249, 115, 22, 0.1)"),
        "error": ("🔴", "#ef4444", "rgba(239, 68, 68, 0.1)"),
        "info": ("ℹ️", "#00d4ff", "rgba(0, 212, 255, 0.1)")
    }
    
    icon, color_val, bg = colors.get(color, colors["info"])
    
    st.markdown(f"""
    <div style="
        background: {bg};
        border-left: 4px solid {color_val};
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    ">
        <span style="color: {color_val}; font-weight: 600;">{icon} {text}</span>
    </div>
    """, unsafe_allow_html=True)


def divider():
    """Render a styled divider."""
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
