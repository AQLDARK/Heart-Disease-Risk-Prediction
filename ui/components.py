import streamlit as st

def inject_dark_css():
    st.markdown(
        """
        <style>
        .stApp { background: #0b0f19; color: #e6e8ee; }
        h1,h2,h3,h4 { color: #ffffff; }
        .block-container { padding-top: 1.2rem; }
        .card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 16px;
        }
        .muted { color: rgba(230,232,238,0.75); font-size: 0.9rem; }
        </style>
        """,
        unsafe_allow_html=True
    )

def risk_badge(label: str):
    # simple text badge
    if label == "Low":
        return "🟢 Low Risk"
    if label == "Medium":
        return "🟠 Medium Risk"
    return "🔴 High Risk"

def card(title: str, body_html: str):
    st.markdown(
        f"""
        <div class="card">
          <h4 style="margin:0 0 8px 0;">{title}</h4>
          <div class="muted">{body_html}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
