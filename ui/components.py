import streamlit as st

def inject_modern_css():
    """Inject modern, visually appealing CSS with top navigation support."""
    st.markdown(
        """
        <style>
        /* Global Styles */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        .stApp { 
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
            color: #f1f5f9;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 { 
            color: #ffffff;
            font-weight: 600;
            letter-spacing: -0.5px;
        }
        
        h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
        h2 { font-size: 1.875rem; margin-top: 1.5rem; margin-bottom: 1rem; }
        h3 { font-size: 1.5rem; margin-top: 1.25rem; margin-bottom: 0.75rem; }
        
        /* Block Container */
        .block-container { 
            padding: 2rem;
            max-width: 1400px;
        }
        
        /* Top Navigation Bar */
        .top-nav {
            background: linear-gradient(90deg, rgba(15,23,42,0.95) 0%, rgba(30,41,59,0.95) 100%);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(148,163,184,0.2);
            padding: 1rem 2rem;
            position: sticky;
            top: 0;
            z-index: 999;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            border-radius: 0 0 16px 16px;
        }
        
        .top-nav-brand {
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .top-nav-buttons {
            display: flex;
            gap: 0.75rem;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .nav-button {
            padding: 0.6rem 1.2rem;
            border: 1px solid rgba(148,163,184,0.3);
            border-radius: 8px;
            background: rgba(51,65,85,0.4);
            color: #cbd5e1;
            cursor: pointer;
            font-size: 0.95rem;
            font-weight: 500;
            transition: all 0.3s ease;
            text-decoration: none;
        }
        
        .nav-button:hover {
            background: rgba(148,163,184,0.2);
            border-color: rgba(148,163,184,0.5);
            color: #f1f5f9;
            transform: translateY(-2px);
        }
        
        .nav-button.active {
            background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
            border-color: #3b82f6;
            color: #ffffff;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        }
        
        .user-info {
            display: flex;
            align-items: center;
            gap: 1rem;
            color: #94a3b8;
            font-size: 0.9rem;
        }
        
        .badge-plan {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 0.35rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .badge-plan.premium {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        }
        
        .badge-plan.free {
            background: linear-gradient(135deg, #64748b 0%, #475569 100%);
        }
        
        /* Cards */
        .card {
            background: linear-gradient(135deg, rgba(30,41,59,0.6) 0%, rgba(15,23,42,0.4) 100%);
            border: 1px solid rgba(148,163,184,0.2);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .card:hover {
            border-color: rgba(148,163,184,0.4);
            background: linear-gradient(135deg, rgba(30,41,59,0.8) 0%, rgba(15,23,42,0.6) 100%);
            transform: translateY(-4px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        
        .card-title {
            font-size: 1.125rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 0.75rem;
        }
        
        .card-text {
            color: #cbd5e1;
            font-size: 0.95rem;
            line-height: 1.6;
        }
        
        /* Badges */
        .risk-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.95rem;
        }
        
        .risk-low {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
        }
        
        .risk-medium {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
        }
        
        .risk-high {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
        }
        
        /* Buttons */
        .stButton > button {
            width: 100%;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            border: none;
            background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
            color: white;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(59, 130, 246, 0.4);
        }
        
        /* Forms */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {
            background: rgba(51,65,85,0.5) !important;
            border: 1px solid rgba(148,163,184,0.3) !important;
            color: #f1f5f9 !important;
            border-radius: 8px !important;
            padding: 0.75rem !important;
            font-size: 0.95rem !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        }
        
        /* Metrics */
        .stMetric {
            background: linear-gradient(135deg, rgba(30,41,59,0.6) 0%, rgba(15,23,42,0.4) 100%);
            border: 1px solid rgba(148,163,184,0.2);
            border-radius: 12px;
            padding: 1.5rem;
        }
        
        /* Dividers */
        hr { border-color: rgba(148,163,184,0.2); }
        
        /* Alerts/Messages */
        .stSuccess {
            background: rgba(16,185,129,0.1) !important;
            border: 1px solid rgba(16,185,129,0.3) !important;
            border-radius: 8px !important;
        }
        
        .stError {
            background: rgba(239,68,68,0.1) !important;
            border: 1px solid rgba(239,68,68,0.3) !important;
            border-radius: 8px !important;
        }
        
        .stWarning {
            background: rgba(245,158,11,0.1) !important;
            border: 1px solid rgba(245,158,11,0.3) !important;
            border-radius: 8px !important;
        }
        
        .stInfo {
            background: rgba(59,130,246,0.1) !important;
            border: 1px solid rgba(59,130,246,0.3) !important;
            border-radius: 8px !important;
        }
        
        /* Utility Classes */
        .muted { 
            color: rgba(203,213,225,0.8);
            font-size: 0.9rem;
        }
        
        .section-header {
            color: #ffffff;
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid rgba(59,130,246,0.3);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .top-nav {
                flex-direction: column;
                gap: 1rem;
                text-align: center;
            }
            
            .top-nav-buttons {
                width: 100%;
                justify-content: center;
            }
            
            .block-container { padding: 1rem; }
            .stApp { font-size: 0.95rem; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_top_navbar(user_name: str, plan: str, role: str, pages: list, current_page: str, on_logout=None):
    """Render modern top navigation bar."""
    badge_class = "premium" if plan == "Premium" else ("standard" if plan == "Standard" else "free")
    
    nav_html = f"""
    <div class="top-nav">
        <div class="top-nav-brand">❤️ CardioPredict</div>
        
        <div class="top-nav-buttons">
    """
    
    for page in pages:
        active_class = "active" if page == current_page else ""
        page_icon = {
            "Predict": "🔍",
            "Explainability": "🧠",
            "History": "📋",
            "Admin Dashboard": "📊",
            "Model Performance": "📈",
            "Subscription & Billing": "💳",
            "About": "ℹ️"
        }.get(page, "•")
        
        nav_html += f'<span class="nav-button {active_class}">{page_icon} {page}</span>'
    
    nav_html += f"""
        </div>
        
        <div class="user-info">
            <span class="badge-plan {badge_class}">{plan}</span>
            <span>👤 {user_name}</span>
        </div>
    </div>
    """
    
    st.markdown(nav_html, unsafe_allow_html=True)


def risk_badge(label: str):
    """Render attractive risk badge with color coding."""
    if label == "Low":
        return f'<span class="risk-badge risk-low">🟢 Low Risk</span>'
    elif label == "Medium":
        return f'<span class="risk-badge risk-medium">🟠 Medium Risk</span>'
    else:
        return f'<span class="risk-badge risk-high">🔴 High Risk</span>'


def card(title: str, body_html: str):
    """Render an attractive card component."""
    st.markdown(
        f"""
        <div class="card">
          <div class="card-title">{title}</div>
          <div class="card-text">{body_html}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def metric_card(title: str, value: str, subtitle: str = ""):
    """Render a metric card with title and value."""
    st.markdown(
        f"""
        <div class="card">
          <div class="card-title" style="font-size: 0.95rem; color: #94a3b8;">{title}</div>
          <div style="font-size: 2.5rem; font-weight: 700; color: #3b82f6; margin: 0.5rem 0;">{value}</div>
          <div class="muted">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_header(text: str):
    """Render a styled section header."""
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)
