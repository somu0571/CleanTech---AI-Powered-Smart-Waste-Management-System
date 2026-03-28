"""
app.py – CleanTech AI  Streamlit Frontend
Run:  streamlit run app.py
Requires backend running at http://localhost:8000
"""

import streamlit as st
import requests
import json
import random
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
API = "http://localhost:8000"

st.set_page_config(
    page_title="CleanTech AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS  –  White & Green Premium Theme
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Google Fonts ───────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');

/* ── CSS Variables ─────────────────────────────────────────────────── */
:root {
    --green-900: #0a3d1f;
    --green-700: #155e32;
    --green-500: #1e8449;
    --green-400: #27ae60;
    --green-300: #52c47e;
    --green-100: #d5f5e3;
    --green-50:  #eafaf1;
    --white:     #ffffff;
    --gray-50:   #f8fafb;
    --gray-100:  #f0f4f2;
    --gray-200:  #dde7e2;
    --gray-400:  #8aab98;
    --gray-600:  #4a6657;
    --gray-900:  #1a2e24;
    --shadow-sm: 0 1px 3px rgba(21,94,50,0.08);
    --shadow-md: 0 4px 16px rgba(21,94,50,0.12);
    --shadow-lg: 0 8px 32px rgba(21,94,50,0.16);
    --radius:    14px;
    --radius-lg: 20px;
}

/* ── Base ──────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--gray-50) !important;
    color: var(--gray-900);
}

/* ── Hide Streamlit chrome ─────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Sidebar ───────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--green-900) 0%, var(--green-700) 100%) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * {
    color: #c8f5da !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: #c8f5da !important;
    font-size: 0.95rem;
    padding: 6px 0;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15) !important;
}

/* ── Main content area ─────────────────────────────────────────────── */
.main .block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1400px;
}

/* ── Page header ───────────────────────────────────────────────────── */
.page-header {
    background: linear-gradient(135deg, var(--green-500) 0%, var(--green-300) 100%);
    border-radius: var(--radius-lg);
    padding: 2.2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
}
.page-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}
.page-header::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 280px; height: 280px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.page-header h1 {
    font-family: 'Playfair Display', serif !important;
    color: white !important;
    font-size: 2.2rem !important;
    margin: 0 !important;
    text-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.page-header p {
    color: rgba(255,255,255,0.88) !important;
    font-size: 1rem;
    margin: 0.4rem 0 0 !important;
}

/* ── KPI Card ──────────────────────────────────────────────────────── */
.kpi-card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    border: 1px solid var(--gray-200);
    box-shadow: var(--shadow-sm);
    transition: box-shadow .2s, transform .2s;
    position: relative;
    overflow: hidden;
}
.kpi-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}
.kpi-card .accent-bar {
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, var(--green-400), var(--green-300));
    border-radius: 4px 0 0 4px;
}
.kpi-card .icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    display: block;
}
.kpi-card .value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--green-700);
    line-height: 1;
}
.kpi-card .label {
    font-size: 0.82rem;
    color: var(--gray-600);
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 500;
}

/* ── Section card ──────────────────────────────────────────────────── */
.section-card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 1.8rem;
    border: 1px solid var(--gray-200);
    box-shadow: var(--shadow-sm);
    margin-bottom: 1.5rem;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--green-700);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Tag badges ────────────────────────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
}
.badge-green   { background: var(--green-100); color: var(--green-700); }
.badge-yellow  { background: #fef9c3; color: #854d0e; }
.badge-red     { background: #fee2e2; color: #991b1b; }
.badge-blue    { background: #dbeafe; color: #1e40af; }
.badge-gray    { background: var(--gray-100); color: var(--gray-600); }

/* ── Auth container ────────────────────────────────────────────────── */
.auth-wrapper {
    max-width: 480px;
    margin: 3rem auto;
    background: var(--white);
    border-radius: var(--radius-lg);
    padding: 2.8rem;
    box-shadow: var(--shadow-lg);
    border: 1px solid var(--gray-200);
}
.auth-logo {
    text-align: center;
    margin-bottom: 1.5rem;
}
.auth-logo .brand {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: var(--green-700);
    display: block;
}
.auth-logo .tagline {
    font-size: 0.85rem;
    color: var(--gray-400);
}

/* ── Inputs override ───────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea textarea {
    border-radius: 10px !important;
    border: 1.5px solid var(--gray-200) !important;
    background: var(--gray-50) !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color .2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: var(--green-400) !important;
    box-shadow: 0 0 0 3px rgba(39,174,96,0.12) !important;
}

/* ── Primary button ────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--green-500), var(--green-400)) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.8rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all .2s !important;
    box-shadow: 0 2px 8px rgba(30,132,73,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(30,132,73,0.35) !important;
}

/* ── Tab styling ───────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--gray-100) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important;
    font-weight: 500 !important;
    color: var(--gray-600) !important;
}
.stTabs [aria-selected="true"] {
    background: var(--white) !important;
    color: var(--green-700) !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ── Alert boxes ───────────────────────────────────────────────────── */
.stSuccess { border-left: 4px solid var(--green-400) !important; }
.stError   { border-left: 4px solid #ef4444 !important; }
.stInfo    { border-left: 4px solid #3b82f6 !important; }
.stWarning { border-left: 4px solid #f59e0b !important; }

/* ── File uploader ─────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--green-300) !important;
    border-radius: var(--radius) !important;
    background: var(--green-50) !important;
}

/* ── Metric cards (native) ─────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: var(--white) !important;
    border: 1px solid var(--gray-200) !important;
    border-radius: var(--radius) !important;
    padding: 1rem 1.2rem !important;
    box-shadow: var(--shadow-sm) !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--green-700) !important;
    font-weight: 700 !important;
}

/* ── Progress bars ─────────────────────────────────────────────────── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--green-400), var(--green-300)) !important;
}

/* ── Leaderboard row ───────────────────────────────────────────────── */
.lb-row {
    display: flex;
    align-items: center;
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.6rem;
    transition: box-shadow .15s;
}
.lb-row:hover { box-shadow: var(--shadow-md); }
.lb-rank {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--green-400);
    width: 40px;
}
.lb-name  { flex: 1; font-weight: 500; }
.lb-pts   { font-weight: 700; color: var(--green-700); }

/* ── Toast-style notification ──────────────────────────────────────── */
.toast {
    background: var(--green-500);
    color: white;
    border-radius: 12px;
    padding: 1rem 1.4rem;
    font-weight: 600;
    box-shadow: var(--shadow-lg);
    animation: slideIn .4s ease;
}
@keyframes slideIn {
    from { transform: translateY(-20px); opacity: 0; }
    to   { transform: translateY(0);     opacity: 1; }
}

/* ── Complaint table ───────────────────────────────────────────────── */
.complaint-row {
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: var(--radius);
    padding: 1.1rem 1.4rem;
    margin-bottom: 0.75rem;
    box-shadow: var(--shadow-sm);
}

/* ── Sidebar brand ─────────────────────────────────────────────────── */
.sidebar-brand {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: white !important;
    text-align: center;
    padding: 1rem 0 0.5rem;
    display: block;
}
.sidebar-sub {
    font-size: 0.78rem;
    color: rgba(200,245,218,0.7) !important;
    text-align: center;
    display: block;
    margin-bottom: 1rem;
}

/* ── Route stop card ───────────────────────────────────────────────── */
.route-stop {
    background: var(--white);
    border-left: 4px solid var(--green-400);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.6rem;
    box-shadow: var(--shadow-sm);
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.route-num {
    background: var(--green-500);
    color: white;
    border-radius: 50%;
    width: 28px; height: 28px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.85rem;
    flex-shrink: 0;
}

/* ── Waste class result card ───────────────────────────────────────── */
.result-card {
    background: linear-gradient(135deg, var(--green-50), var(--white));
    border: 2px solid var(--green-300);
    border-radius: var(--radius-lg);
    padding: 2rem;
    text-align: center;
}
.result-class {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    color: var(--green-700);
    margin: 0;
}
.result-conf {
    font-size: 1.1rem;
    color: var(--gray-600);
    margin: 0.3rem 0 1rem;
}

/* ── Eco points ring ───────────────────────────────────────────────── */
.eco-ring {
    width: 130px; height: 130px;
    border-radius: 50%;
    background: conic-gradient(var(--green-400) 0%, var(--green-400) 72%, var(--gray-100) 72%);
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 1rem;
    box-shadow: var(--shadow-md);
    position: relative;
}
.eco-ring-inner {
    width: 95px; height: 95px;
    background: white;
    border-radius: 50%;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
}
.eco-ring-pts {
    font-size: 1.5rem; font-weight: 700;
    color: var(--green-700); line-height: 1;
}
.eco-ring-lbl {
    font-size: 0.65rem; color: var(--gray-400);
    text-transform: uppercase; letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════════════
def _init_state():
    defaults = {
        "logged_in":   False,
        "token":       None,
        "role":        None,
        "username":    None,
        "eco_points":  0,
        "auth_page":   "Login",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def api(method: str, path: str, **kwargs):
    """API call wrapper with automatic auth header."""
    headers = kwargs.pop("headers", {})
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    try:
        r = getattr(requests, method)(f"{API}{path}", headers=headers,
                                      timeout=15, **kwargs)
        return r
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend. Start with: `uvicorn main:app --reload`")
        return None


def kpi(col, icon, value, label, delta=None):
    with col:
        d = f"<div style='font-size:0.78rem;color:#27ae60;margin-top:0.2rem'>{delta}</div>" if delta else ""
        st.markdown(f"""
        <div class="kpi-card">
          <div class="accent-bar"></div>
          <span class="icon">{icon}</span>
          <div class="value">{value}</div>
          <div class="label">{label}</div>
          {d}
        </div>""", unsafe_allow_html=True)


def badge(text, color="green"):
    return f'<span class="badge badge-{color}">{text}</span>'


def section(title_with_icon):
    st.markdown(f'<div class="section-title">{title_with_icon}</div>',
                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# AUTH PAGES
# ══════════════════════════════════════════════════════════════════════════════

def render_auth():
    # Center column trick
    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        st.markdown("""
        <div class="auth-logo">
          <span class="brand">🌿 CleanTech AI</span>
          <span class="tagline">Smart Waste Management for Smart Cities</span>
        </div>""", unsafe_allow_html=True)

        tab_login, tab_reg = st.tabs(["🔑 Login", "📝 Register"])

        # ── Login ──────────────────────────────────────────────────────────
        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            role   = st.selectbox("Role", ["citizen", "admin"], key="l_role",
                                  format_func=lambda x: "👤 Citizen" if x == "citizen" else "🧑‍💼 Admin")
            uname  = st.text_input("Username", placeholder="your_username", key="l_user")
            passwd = st.text_input("Password", type="password", placeholder="••••••••", key="l_pass")

            if st.button("Login →", use_container_width=True):
                if not uname or not passwd:
                    st.error("Please fill all fields.")
                else:
                    with st.spinner("Authenticating..."):
                        r = api("post", "/login",
                                json={"username": uname, "password": passwd, "role": role})
                    if r and r.status_code == 200:
                        d = r.json()
                        st.session_state.update({
                            "logged_in":  True,
                            "token":      d["access_token"],
                            "role":       d["role"],
                            "username":   d["username"],
                            "eco_points": d.get("eco_points", 0),
                        })
                        st.success(f"Welcome back, {d['username']}! 🌿")
                        time.sleep(0.6)
                        st.rerun()
                    elif r:
                        st.error(r.json().get("detail", "Login failed"))

        # ── Register ───────────────────────────────────────────────────────
        with tab_reg:
            st.markdown("<br>", unsafe_allow_html=True)
            r_role  = st.selectbox("Register as", ["citizen", "admin"], key="r_role",
                                   format_func=lambda x: "👤 Citizen" if x == "citizen" else "🧑‍💼 Admin")
            r_user  = st.text_input("Username", key="r_user")
            r_pass  = st.text_input("Password", type="password", key="r_pass")
            r_conf  = st.text_input("Confirm Password", type="password", key="r_conf")

            r_admin_id = r_org = None
            if r_role == "admin":
                st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
                st.info("🔐 Admin verification required")
                r_admin_id = st.text_input("Official Admin ID",
                                           placeholder="e.g. ADMIN001 / CLEANTECH_DEMO",
                                           key="r_aid")
                r_org      = st.text_input("Organisation Name", key="r_org")
                st.caption("Demo IDs: ADMIN001, ADMIN002, ADMIN003, CLEANTECH_DEMO")

            if st.button("Create Account →", use_container_width=True):
                payload = {
                    "username": r_user, "password": r_pass,
                    "confirm_pass": r_conf, "role": r_role,
                    "admin_id": r_admin_id, "organization": r_org,
                }
                with st.spinner("Creating account..."):
                    r = api("post", "/register", json=payload)
                if r and r.status_code == 200:
                    st.success("✅ Account created! Please log in.")
                elif r:
                    st.error(r.json().get("detail", "Registration failed"))


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <span class="sidebar-brand">🌿 CleanTech AI</span>
        <span class="sidebar-sub">Smart Waste Management</span>
        """, unsafe_allow_html=True)
        st.markdown("---")

        role_icon = "🧑‍💼" if st.session_state.role == "admin" else "👤"
        st.markdown(f"""
        <div style="text-align:center;padding:0.5rem 0;">
          <div style="font-size:2rem">{role_icon}</div>
          <div style="font-weight:600;font-size:1rem">{st.session_state.username}</div>
          <div style="font-size:0.8rem;opacity:0.7">{st.session_state.role.capitalize()}</div>
          <div style="margin-top:0.4rem;font-size:0.85rem;color:#52c47e">
            🌱 {st.session_state.eco_points} eco-points
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        if st.session_state.role == "admin":
            pages = {
                "🏠 Dashboard":         "admin_home",
                "🗺️  Waste Heatmap":    "heatmap",
                "📈 Predictive Analytics": "analytics",
                "🚛 Route Optimiser":   "route",
                "📋 Complaint Manager": "complaints",
                "🏆 Leaderboard":       "leaderboard",
            }
        else:
            pages = {
                "🏠 My Dashboard":      "citizen_home",
                "🔬 Classify Waste":    "classify",
                "📣 Report Issue":      "report",
                "🌱 Eco-Points":        "ecopoints",
                "🏆 Leaderboard":       "leaderboard",
            }

        selected = st.radio("Navigation", list(pages.keys()),
                            label_visibility="collapsed")
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            for k in ["logged_in","token","role","username","eco_points"]:
                st.session_state[k] = None if k != "logged_in" else False
            st.rerun()

        return pages[selected]


# ══════════════════════════════════════════════════════════════════════════════
# CITIZEN PAGES
# ══════════════════════════════════════════════════════════════════════════════

def page_citizen_home():
    st.markdown("""
    <div class="page-header">
      <h1>Welcome back 🌿</h1>
      <p>Your personal waste management dashboard</p>
    </div>""", unsafe_allow_html=True)

    r = api("get", "/my-activities")
    acts  = []
    pts   = st.session_state.eco_points
    if r and r.status_code == 200:
        d   = r.json()
        pts = d.get("eco_points", pts)
        acts = d.get("activities", [])
        st.session_state.eco_points = pts

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "🌱", pts, "Eco-Points", "🏆 Keep growing!")
    kpi(c2, "🔬", len([a for a in acts if "Classified" in a.get("activity","")]), "Classifications")
    kpi(c3, "📣", len([a for a in acts if "complaint" in a.get("activity","").lower()]), "Reports Filed")
    kpi(c4, "💚", f"{min(100, pts//5)}%", "Green Score")

    st.markdown("<br>", unsafe_allow_html=True)

    # Recent activities
    col1, col2 = st.columns([1.6, 1])
    with col1:
        section("📋 Recent Activities")
        if acts:
            for a in acts[:6]:
                pts_badge = badge(f"+{a['points']} pts", "green")
                st.markdown(f"""
                <div class="complaint-row" style="display:flex;align-items:center;gap:1rem">
                  <div style="flex:1">
                    <div style="font-weight:500">{a['activity']}</div>
                    <div style="font-size:0.8rem;color:#8aab98">{a['date']}</div>
                  </div>
                  {pts_badge}
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No activities yet. Start by classifying waste or filing a report!")

    with col2:
        section("🌍 Quick Actions")
        if st.button("🔬 Classify Waste", use_container_width=True):
            st.session_state["_nav"] = "classify"
            st.rerun()
        if st.button("📣 Report Dirty Area", use_container_width=True):
            st.session_state["_nav"] = "report"
            st.rerun()
        if st.button("🏆 View Leaderboard", use_container_width=True):
            st.session_state["_nav"] = "leaderboard"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        # Eco tips
        tips = [
            "♻️ Always separate wet & dry waste",
            "🛍️ Carry a reusable bag when shopping",
            "💧 Composting reduces landfill by 30%",
            "🔋 Recycle e-waste at authorised centres",
            "🥗 Food waste can become organic fertiliser",
        ]
        tip = random.choice(tips)
        st.markdown(f"""
        <div style="background:var(--green-50);border:1px solid var(--green-100);
             border-radius:12px;padding:1rem;margin-top:0.5rem">
          <div style="font-size:0.78rem;color:var(--green-500);font-weight:600;
               text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.3rem">
            💡 Eco Tip
          </div>
          <div style="font-size:0.9rem;color:var(--gray-700)">{tip}</div>
        </div>""", unsafe_allow_html=True)


def page_classify():
    st.markdown("""
    <div class="page-header">
      <h1>🔬 AI Waste Classification</h1>
      <p>Upload an image and let our AI identify the waste type instantly</p>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        section("📤 Upload Waste Image")
        uploaded = st.file_uploader("Choose an image", type=["jpg","jpeg","png","webp"],
                                    label_visibility="collapsed")
        if uploaded:
            st.image(uploaded, use_column_width=True, caption="Uploaded image")

        if uploaded and st.button("🚀 Classify Now", use_container_width=True):
            with st.spinner("Analysing with AI..."):
                r = api("post", "/classify",
                        files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)})
            if r and r.status_code == 200:
                d = r.json()
                st.session_state["_classify_result"] = d
                st.session_state.eco_points += d.get("eco_points_earned", 0)
            elif r:
                st.error(r.json().get("detail","Classification failed"))

    with col2:
        section("📊 Classification Result")
        res = st.session_state.get("_classify_result")
        if res:
            cls_colors = {
                "Organic":   "#27ae60", "Plastic":   "#3498db",
                "Metal":     "#95a5a6", "E-waste":   "#e74c3c",
                "Hazardous": "#c0392b",
            }
            color = cls_colors.get(res["class"], "#27ae60")
            conf_pct = int(res["confidence"] * 100)
            st.markdown(f"""
            <div class="result-card">
              <div style="font-size:3rem;margin-bottom:0.5rem">
                {"🌱" if res["class"]=="Organic" else
                 "♻️" if res["class"]=="Plastic" else
                 "🔩" if res["class"]=="Metal" else
                 "💻" if res["class"]=="E-waste" else "⚠️"}
              </div>
              <p class="result-class" style="color:{color}">{res["class"]}</p>
              <p class="result-conf">{conf_pct}% confidence · {res["method"]}</p>
            </div>""", unsafe_allow_html=True)

            st.progress(res["confidence"])
            st.markdown("<br>", unsafe_allow_html=True)

            # Confidence bar chart
            classes  = ["Organic","Plastic","Metal","E-waste","Hazardous"]
            idx      = classes.index(res["class"]) if res["class"] in classes else 0
            probs    = [0.05] * 5
            probs[idx] = res["confidence"]
            remain   = 1 - res["confidence"]
            others   = [i for i in range(5) if i != idx]
            for i, o in enumerate(others):
                probs[o] = remain * (0.35 if i == 0 else 0.25 if i == 1 else 0.2 if i == 2 else 0.1) / 0.9

            fig = go.Figure(go.Bar(
                x=probs, y=classes, orientation="h",
                marker_color=[color if c == res["class"] else "#d5f5e3" for c in classes],
                marker_line_width=0,
            ))
            fig.update_layout(
                height=200, margin=dict(l=0,r=0,t=10,b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans"),
                xaxis=dict(range=[0,1], showgrid=False, showticklabels=False),
                yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig, use_container_width=True)

            st.info(f"**Disposal Tip:** {res['disposal']}")
            pts = res.get("eco_points_earned", 0)
            if pts:
                st.success(f"🌱 +{pts} eco-points earned!")
        else:
            st.markdown("""
            <div style="text-align:center;padding:3rem;color:#8aab98">
              <div style="font-size:3rem">🖼️</div>
              <div style="margin-top:0.5rem">Upload an image to see results</div>
            </div>""", unsafe_allow_html=True)

        # Waste guide
        st.markdown("<br>", unsafe_allow_html=True)
        section("📖 Quick Disposal Guide")
        guide = {
            "🌱 Organic":   "Green bin / Compost",
            "♻️ Plastic":   "Blue bin (clean first)",
            "🔩 Metal":     "Scrap dealer / Recycler",
            "💻 E-waste":   "Authorised e-waste point",
            "⚠️ Hazardous": "Municipal hazardous team",
        }
        for k, v in guide.items():
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;
                 padding:0.5rem 0;border-bottom:1px solid var(--gray-100)">
              <span style="font-weight:500">{k}</span>
              <span style="color:var(--gray-600);font-size:0.88rem">{v}</span>
            </div>""", unsafe_allow_html=True)


def page_report():
    st.markdown("""
    <div class="page-header">
      <h1>📣 Report a Dirty Area</h1>
      <p>Help keep your city clean by reporting waste hotspots</p>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])
    with col1:
        section("📝 Complaint Details")
        location = st.text_input("Location", placeholder="e.g. MG Road near Bus Stop 3")
        desc     = st.text_area("Description", placeholder="Describe the waste / issue...", height=120)
        img      = st.file_uploader("Attach Photo (optional)", type=["jpg","jpeg","png"])

        if st.button("📤 Submit Report", use_container_width=True):
            if not location or not desc:
                st.warning("Please provide location and description.")
            else:
                files   = {"image": (img.name, img.getvalue(), img.type)} if img else {}
                payload = {"location": location, "description": desc}
                with st.spinner("Submitting..."):
                    r = api("post", "/complaint", data=payload,
                            files=files if files else None)
                if r and r.status_code == 200:
                    pts = r.json().get("eco_points_earned", 20)
                    st.session_state.eco_points += pts
                    st.markdown(f"""
                    <div class="toast">✅ Report submitted! +{pts} eco-points earned.</div>
                    """, unsafe_allow_html=True)
                    time.sleep(1.5)
                    st.rerun()
                elif r:
                    st.error(r.json().get("detail","Submission failed"))

    with col2:
        section("ℹ️ Reporting Tips")
        tips = [
            ("📍", "Be specific about location", "Include landmarks or street numbers"),
            ("📸", "Add a photo", "Visual evidence speeds up resolution"),
            ("📝", "Describe clearly", "Mention waste type and quantity"),
            ("🌱", "Earn points", "Each report gives you 20 eco-points"),
        ]
        for icon, title, sub in tips:
            st.markdown(f"""
            <div style="display:flex;gap:0.8rem;padding:0.8rem 0;
                 border-bottom:1px solid var(--gray-100)">
              <span style="font-size:1.5rem">{icon}</span>
              <div>
                <div style="font-weight:600;font-size:0.92rem">{title}</div>
                <div style="font-size:0.82rem;color:var(--gray-400)">{sub}</div>
              </div>
            </div>""", unsafe_allow_html=True)


def page_ecopoints():
    st.markdown("""
    <div class="page-header">
      <h1>🌱 Eco-Points Tracker</h1>
      <p>Track your environmental impact and earn rewards</p>
    </div>""", unsafe_allow_html=True)

    r = api("get", "/my-activities")
    pts, acts = st.session_state.eco_points, []
    if r and r.status_code == 200:
        d    = r.json()
        pts  = d.get("eco_points", pts)
        acts = d.get("activities", [])

    col1, col2 = st.columns([1, 1.5])
    with col1:
        level  = "Eco Warrior" if pts >= 500 else "Green Champion" if pts >= 200 else "Earth Saver" if pts >= 50 else "Beginner"
        next_l = 500 if pts < 500 else 1000
        prog   = min(1.0, pts / next_l)
        st.markdown(f"""
        <div style="text-align:center;padding:1.5rem;background:white;
             border-radius:16px;border:1px solid var(--gray-200);
             box-shadow:var(--shadow-sm)">
          <div style="font-size:3.5rem">{"🏆" if pts>=500 else "🥇" if pts>=200 else "🌱"}</div>
          <div style="font-family:'Playfair Display',serif;font-size:1.5rem;
               color:var(--green-700);font-weight:700;margin:0.5rem 0">{pts}</div>
          <div style="font-size:0.8rem;color:var(--gray-400);text-transform:uppercase;
               letter-spacing:0.05em">Eco-Points</div>
          <div style="margin-top:0.8rem;background:var(--green-50);border-radius:8px;
               padding:0.4rem 0.8rem;display:inline-block">
            <span style="font-size:0.85rem;color:var(--green-700);font-weight:600">{level}</span>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.caption(f"Progress to next level: {pts}/{next_l}")
        st.progress(prog)

        # Rewards
        section("🎁 Rewards")
        rewards = [
            ("50 pts",  "Eco-Warrior Badge", pts >= 50),
            ("100 pts", "Priority Complaint", pts >= 100),
            ("200 pts", "Green Champion",     pts >= 200),
            ("500 pts", "City Hero Trophy",   pts >= 500),
        ]
        for req, name, unlocked in rewards:
            icon = "✅" if unlocked else "🔒"
            col_s = "var(--green-400)" if unlocked else "var(--gray-400)"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.8rem;padding:0.6rem 0;
                 border-bottom:1px solid var(--gray-100)">
              <span>{icon}</span>
              <div style="flex:1">
                <div style="font-weight:500;color:{col_s}">{name}</div>
                <div style="font-size:0.78rem;color:var(--gray-400)">{req}</div>
              </div>
            </div>""", unsafe_allow_html=True)

    with col2:
        section("📊 Points History")
        if acts:
            dates  = [a["date"] for a in reversed(acts)]
            cumpts = []
            total  = 0
            for a in reversed(acts):
                total += a["points"]
                cumpts.append(total)

            fig = go.Figure(go.Scatter(
                x=dates, y=cumpts,
                fill="tozeroy",
                line=dict(color="#27ae60", width=2.5),
                fillcolor="rgba(39,174,96,0.1)",
                mode="lines+markers",
                marker=dict(color="#27ae60", size=6),
            ))
            fig.update_layout(
                height=250, margin=dict(l=0,r=0,t=10,b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, color="#8aab98"),
                yaxis=dict(showgrid=True, gridcolor="#f0f4f2", color="#8aab98"),
                font=dict(family="DM Sans"),
            )
            st.plotly_chart(fig, use_container_width=True)

            section("🗒️ Activity Log")
            for a in acts[:8]:
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                     padding:0.6rem 0;border-bottom:1px solid var(--gray-100)">
                  <div>
                    <div style="font-size:0.9rem">{a['activity']}</div>
                    <div style="font-size:0.75rem;color:#8aab98">{a['date']}</div>
                  </div>
                  <span class="badge badge-green">+{a['points']}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Complete activities to earn eco-points and see your history here!")


# ══════════════════════════════════════════════════════════════════════════════
# ADMIN PAGES
# ══════════════════════════════════════════════════════════════════════════════

def page_admin_home():
    st.markdown("""
    <div class="page-header">
      <h1>🏙️ Municipality Dashboard</h1>
      <p>Real-time overview of city waste management operations</p>
    </div>""", unsafe_allow_html=True)

    r = api("get", "/admin/stats")
    stats = {}
    if r and r.status_code == 200:
        stats = r.json()

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "👥", stats.get("total_users", "–"), "Total Citizens")
    kpi(c2, "📋", stats.get("total_complaints", "–"), "Total Complaints")
    kpi(c3, "✅", stats.get("resolved", "–"), "Resolved",
        f"⏳ {stats.get('pending','–')} pending")
    kpi(c4, "🌍", f"{stats.get('carbon_saved_kg', '–')} kg", "CO₂ Saved")

    st.markdown("<br>", unsafe_allow_html=True)
    c5, c6, c7 = st.columns(3)
    kpi(c5, "♻️", f"{stats.get('total_waste_kg','–')} kg", "Waste Tracked (7d)")
    kpi(c6, "📊", f"{stats.get('segregation_score','–')}%", "Segregation Score")
    kpi(c7, "🚛", "5", "Active Routes")

    # Quick charts
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        section("📈 Weekly Waste Trend (All Zones)")
        rp = api("get", "/predict?steps=7")
        if rp and rp.status_code == 200:
            d   = rp.json()
            df  = pd.DataFrame(d["historical"][-14:])
            fig = go.Figure(go.Scatter(
                x=df["date"], y=df["waste_kg"],
                mode="lines+markers",
                line=dict(color="#27ae60", width=2.5),
                fill="tozeroy", fillcolor="rgba(39,174,96,0.08)",
                marker=dict(color="#27ae60", size=5),
            ))
            fig.update_layout(
                height=230, margin=dict(l=0,r=0,t=10,b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, color="#8aab98"),
                yaxis=dict(showgrid=True, gridcolor="#f0f4f2", color="#8aab98",
                           title="Waste (kg)"),
                font=dict(family="DM Sans"),
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("🗺️ Zone Waste Distribution")
        rh = api("get", "/heatmap")
        if rh and rh.status_code == 200:
            hm  = rh.json()
            zones  = [z["zone"].split("–")[-1].strip() for z in hm]
            vals   = [z["waste_kg"] for z in hm]
            greens = ["#0a3d1f","#1e8449","#27ae60","#52c47e","#d5f5e3"]
            fig = go.Figure(go.Bar(
                x=zones, y=vals,
                marker_color=greens,
                marker_line_width=0,
                text=[f"{v:.0f} kg" for v in vals],
                textposition="outside",
            ))
            fig.update_layout(
                height=230, margin=dict(l=0,r=0,t=10,b=30),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, color="#8aab98"),
                yaxis=dict(showgrid=True, gridcolor="#f0f4f2", color="#8aab98"),
                font=dict(family="DM Sans"),
            )
            st.plotly_chart(fig, use_container_width=True)

    # Carbon savings calculator
    st.markdown("<br>", unsafe_allow_html=True)
    section("🌍 Carbon Savings Calculator")
    col3, col4 = st.columns([1, 2])
    with col3:
        waste_input = st.number_input("Enter waste collected (kg)", min_value=0, value=500, step=50)
        recycled    = st.slider("Recycling rate (%)", 0, 100, 60)
    with col4:
        co2_saved = round(waste_input * (recycled / 100) * 0.0023, 2)
        trees_eq  = round(co2_saved / 21.7, 1)
        fuel_eq   = round(co2_saved / 2.31, 1)

        c_a, c_b, c_c = st.columns(3)
        kpi(c_a, "🌿", f"{co2_saved} kg", "CO₂ Saved")
        kpi(c_b, "🌳", f"{trees_eq}", "Tree Equivalent")
        kpi(c_c, "⛽", f"{fuel_eq} L", "Fuel Offset")


def page_heatmap():
    st.markdown("""
    <div class="page-header">
      <h1>🗺️ Waste Heatmap</h1>
      <p>Real-time waste distribution across city zones</p>
    </div>""", unsafe_allow_html=True)

    r = api("get", "/heatmap")
    if r and r.status_code == 200:
        hm = r.json()

        # Map
        import folium
        from streamlit_folium import st_folium

        avg_lat = sum(z["lat"] for z in hm) / len(hm)
        avg_lon = sum(z["lon"] for z in hm) / len(hm)
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=11,
                       tiles="CartoDB positron")

        max_w = max(z["waste_kg"] for z in hm)
        for z in hm:
            intensity = z["waste_kg"] / max_w
            color = f"#{int(10+intensity*200):02x}{int(130-intensity*80):02x}{int(50-intensity*20):02x}"
            folium.CircleMarker(
                location=[z["lat"], z["lon"]],
                radius=12 + intensity * 20,
                color=color, fill=True, fill_color=color, fill_opacity=0.7,
                popup=folium.Popup(
                    f"<b>{z['zone']}</b><br>Waste: {z['waste_kg']:.1f} kg",
                    max_width=200),
                tooltip=z["zone"],
            ).add_to(m)

        col1, col2 = st.columns([1.8, 1])
        with col1:
            st_folium(m, width="100%", height=450)

        with col2:
            section("📊 Zone Rankings")
            sorted_hm = sorted(hm, key=lambda x: x["waste_kg"], reverse=True)
            for i, z in enumerate(sorted_hm):
                pct = z["waste_kg"] / max_w
                bar_color = "#e74c3c" if pct > 0.8 else "#f39c12" if pct > 0.5 else "#27ae60"
                st.markdown(f"""
                <div style="margin-bottom:0.8rem">
                  <div style="display:flex;justify-content:space-between;
                       font-size:0.88rem;margin-bottom:0.3rem">
                    <span style="font-weight:500">{z['zone'].split('–')[-1].strip()}</span>
                    <span style="color:var(--gray-600)">{z['waste_kg']:.1f} kg</span>
                  </div>
                  <div style="background:var(--gray-100);border-radius:4px;height:8px">
                    <div style="width:{pct*100:.0f}%;background:{bar_color};
                         height:8px;border-radius:4px;transition:width 0.5s"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

            # High waste zones
            st.markdown("<br>", unsafe_allow_html=True)
            section("⚠️ Alert Zones")
            for z in sorted_hm[:2]:
                st.markdown(f"""
                <div style="background:#fff7ed;border:1px solid #fed7aa;border-radius:10px;
                     padding:0.8rem 1rem;margin-bottom:0.5rem">
                  <span style="font-weight:600;color:#9a3412">🔴 {z['zone']}</span>
                  <div style="font-size:0.82rem;color:#c2410c;margin-top:0.2rem">
                    {z['waste_kg']:.1f} kg – Immediate attention required
                  </div>
                </div>""", unsafe_allow_html=True)


def page_analytics():
    st.markdown("""
    <div class="page-header">
      <h1>📈 Predictive Analytics</h1>
      <p>AI-powered waste forecasting and trend analysis</p>
    </div>""", unsafe_allow_html=True)

    r = api("get", "/heatmap")
    zones = ["Zone A – North","Zone B – East","Zone C – South","Zone D – West","Zone E – Central"]
    if r and r.status_code == 200:
        zones = [z["zone"] for z in r.json()]

    col_ctrl, _ = st.columns([1, 2])
    with col_ctrl:
        sel_zone = st.selectbox("Select Zone", zones)
        steps    = st.slider("Forecast Days", 7, 60, 30)

    rp = api("get", f"/predict?zone={sel_zone}&steps={steps}")
    if rp and rp.status_code == 200:
        d       = rp.json()
        hist_df = pd.DataFrame(d["historical"])
        fcast_df= pd.DataFrame(d["forecast"])

        # Main chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist_df["date"], y=hist_df["waste_kg"],
            name="Historical", mode="lines",
            line=dict(color="#155e32", width=2.5),
            fill="tozeroy", fillcolor="rgba(21,94,50,0.07)",
        ))
        fig.add_trace(go.Scatter(
            x=fcast_df["date"], y=fcast_df["waste_kg"],
            name="Forecast", mode="lines",
            line=dict(color="#27ae60", width=2.5, dash="dash"),
            fill="tozeroy", fillcolor="rgba(39,174,96,0.07)",
        ))
        # Peak annotation
        peak_idx  = fcast_df["waste_kg"].idxmax()
        peak_date = fcast_df.loc[peak_idx, "date"]
        peak_val  = fcast_df.loc[peak_idx, "waste_kg"]
        fig.add_annotation(
            x=peak_date, y=peak_val,
            text=f"📈 Peak: {peak_val:.0f} kg",
            showarrow=True, arrowhead=2,
            bgcolor="white", bordercolor="#27ae60",
            font=dict(color="#155e32", size=12),
        )
        fig.update_layout(
            height=380, margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, color="#8aab98"),
            yaxis=dict(showgrid=True, gridcolor="#f0f4f2", color="#8aab98",
                       title="Waste (kg)"),
            font=dict(family="DM Sans"),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig, use_container_width=True)

        # KPIs
        c1,c2,c3,c4 = st.columns(4)
        kpi(c1, "📅", d["peak_day"], "Predicted Peak Day")
        kpi(c2, "📦", f"{fcast_df['waste_kg'].mean():.1f} kg", "Avg Forecast/Day")
        kpi(c3, "📉", d["method"], "Model Used")
        kpi(c4, "🔴", ", ".join(z.split("–")[-1].strip() for z in d["high_zones"][:2]),
            "High-Waste Zones")

        # Heatmap by day-of-week (simulated)
        st.markdown("<br>", unsafe_allow_html=True)
        section("📅 Weekly Pattern (simulated)")
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        vals = [random.uniform(60,120) for _ in days]
        fig2 = go.Figure(go.Bar(
            x=days, y=vals,
            marker_color=["#27ae60" if v < 90 else "#f39c12" if v < 105 else "#e74c3c"
                          for v in vals],
            marker_line_width=0,
        ))
        fig2.update_layout(
            height=220, margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, color="#8aab98"),
            yaxis=dict(showgrid=True, gridcolor="#f0f4f2", color="#8aab98"),
            font=dict(family="DM Sans"),
        )
        st.plotly_chart(fig2, use_container_width=True)


def page_route():
    st.markdown("""
    <div class="page-header">
      <h1>🚛 Route Optimisation Engine</h1>
      <p>AI-powered collection routes that save fuel and reduce emissions</p>
    </div>""", unsafe_allow_html=True)

    if st.button("🔄 Generate Optimised Route", use_container_width=False):
        with st.spinner("Running Nearest-Neighbour VRP algorithm..."):
            r = api("get", "/route")
        if r and r.status_code == 200:
            st.session_state["_route"] = r.json()
        elif r:
            st.error(r.json().get("detail","Route optimisation failed"))

    route_data = st.session_state.get("_route")
    if route_data:
        c1,c2,c3,c4 = st.columns(4)
        kpi(c1, "📍", route_data["stops"], "Collection Stops")
        kpi(c2, "🛣️", f"{route_data['total_km']} km", "Optimised Distance")
        kpi(c3, "⛽", f"{route_data['fuel_saved_L']} L", "Fuel Saved")
        kpi(c4, "🌿", f"{route_data['carbon_saved_kg']} kg", "CO₂ Reduced")

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1.4, 1])

        with col1:
            section("🗺️ Route Map")
            import folium
            from streamlit_folium import st_folium

            depot = route_data["depot"]
            stops = route_data["route"]
            all_lats = [depot["lat"]] + [s["lat"] for s in stops]
            all_lons = [depot["lon"]] + [s["lon"] for s in stops]
            m = folium.Map(location=[sum(all_lats)/len(all_lats),
                                      sum(all_lons)/len(all_lons)],
                           zoom_start=12, tiles="CartoDB positron")

            # Depot
            folium.Marker(
                [depot["lat"], depot["lon"]],
                popup="🏭 Municipal Depot",
                icon=folium.Icon(color="green", icon="home"),
            ).add_to(m)

            # Stops + route line
            coords = [[depot["lat"], depot["lon"]]]
            for i, s in enumerate(stops):
                folium.Marker(
                    [s["lat"], s["lon"]],
                    popup=f"Stop {i+1}: {s['zone']}<br>{s['waste_kg']:.1f} kg",
                    icon=folium.Icon(color="blue", icon="trash"),
                ).add_to(m)
                coords.append([s["lat"], s["lon"]])
            coords.append([depot["lat"], depot["lon"]])
            folium.PolyLine(coords, color="#27ae60", weight=3,
                            opacity=0.8, dash_array="8").add_to(m)

            st_folium(m, width="100%", height=400)

        with col2:
            section("📋 Route Stops")
            stops_ordered = route_data["route"]
            st.markdown(f"""
            <div class="route-stop" style="background:var(--green-50)">
              <div class="route-num" style="background:var(--green-700)">🏭</div>
              <div><div style="font-weight:600">Municipal Depot</div>
                <div style="font-size:0.8rem;color:var(--gray-400)">Starting point</div>
              </div>
            </div>""", unsafe_allow_html=True)

            for i, s in enumerate(stops_ordered):
                st.markdown(f"""
                <div class="route-stop">
                  <div class="route-num">{i+1}</div>
                  <div>
                    <div style="font-weight:600">{s['zone']}</div>
                    <div style="font-size:0.8rem;color:var(--gray-400)">{s['waste_kg']:.1f} kg to collect</div>
                  </div>
                </div>""", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="route-stop" style="background:var(--green-50)">
              <div class="route-num" style="background:var(--green-700)">🏭</div>
              <div><div style="font-weight:600">Return to Depot</div>
                <div style="font-size:0.8rem;color:var(--gray-400)">Route complete</div>
              </div>
            </div>""", unsafe_allow_html=True)

            # Savings summary
            saved_pct = round((route_data["saved_km"] / max(route_data["naive_km"], 0.1)) * 100, 1)
            st.markdown(f"""
            <div style="background:var(--green-50);border:1px solid var(--green-100);
                 border-radius:12px;padding:1rem;margin-top:1rem">
              <div style="font-weight:600;color:var(--green-700);margin-bottom:0.5rem">
                ✅ Optimisation Savings
              </div>
              <div style="font-size:0.88rem">
                Original route: <b>{route_data['naive_km']} km</b><br>
                Optimised: <b>{route_data['total_km']} km</b><br>
                Saved: <b style="color:var(--green-500)">{route_data['saved_km']} km ({saved_pct}%)</b>
              </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:4rem;color:#8aab98">
          <div style="font-size:3rem">🚛</div>
          <div style="margin-top:0.5rem;font-size:1rem">
            Click "Generate Optimised Route" to begin
          </div>
        </div>""", unsafe_allow_html=True)


def page_complaints():
    st.markdown("""
    <div class="page-header">
      <h1>📋 Complaint Manager</h1>
      <p>Review and manage citizen-filed waste complaints</p>
    </div>""", unsafe_allow_html=True)

    filter_status = st.selectbox("Filter by status",
                                 ["all","pending","in_progress","resolved"])
    url = "/complaints"
    if filter_status != "all":
        url += f"?status_filter={filter_status}"

    r = api("get", url)
    if r and r.status_code == 200:
        complaints = r.json()

        # KPIs
        total    = len(complaints)
        pending  = sum(1 for c in complaints if c["status"]=="pending")
        progress = sum(1 for c in complaints if c["status"]=="in_progress")
        resolved = sum(1 for c in complaints if c["status"]=="resolved")
        c1,c2,c3,c4 = st.columns(4)
        kpi(c1, "📋", total, "Total")
        kpi(c2, "⏳", pending, "Pending")
        kpi(c3, "🔄", progress, "In Progress")
        kpi(c4, "✅", resolved, "Resolved")

        st.markdown("<br>", unsafe_allow_html=True)

        if not complaints:
            st.info("No complaints found.")
        for c in complaints:
            color_map = {"pending":"yellow","in_progress":"blue","resolved":"green"}
            b = badge(c["status"].replace("_"," ").title(),
                      color_map.get(c["status"],"gray"))
            with st.container():
                st.markdown(f"""
                <div class="complaint-row">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start">
                    <div>
                      <span style="font-weight:600">#{c['id']} · {c['location']}</span>
                      {b}
                      <div style="font-size:0.88rem;color:var(--gray-600);margin-top:0.3rem">
                        {c['description']}
                      </div>
                      <div style="font-size:0.78rem;color:#8aab98;margin-top:0.2rem">
                        👤 {c['username']} · 🕐 {c['timestamp'][:16]}
                      </div>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)

                col_s, col_b, _ = st.columns([1.2, 0.8, 3])
                new_status = col_s.selectbox(
                    "Update", ["pending","in_progress","resolved"],
                    index=["pending","in_progress","resolved"].index(c["status"]),
                    key=f"st_{c['id']}", label_visibility="collapsed",
                )
                if col_b.button("Update", key=f"btn_{c['id']}"):
                    ur = api("put", f"/update-status/{c['id']}",
                             json={"status": new_status})
                    if ur and ur.status_code == 200:
                        st.success(f"Complaint #{c['id']} updated to {new_status}")
                        st.rerun()
    elif r:
        st.error(r.json().get("detail","Failed to load complaints"))


def page_leaderboard():
    st.markdown("""
    <div class="page-header">
      <h1>🏆 Eco Leaderboard</h1>
      <p>Top environmental contributors in your city</p>
    </div>""", unsafe_allow_html=True)

    r = api("get", "/leaderboard")
    if r and r.status_code == 200:
        board = r.json()
        medals = ["🥇","🥈","🥉"] + ["🏅"] * 7

        col1, col2 = st.columns([1.5, 1])
        with col1:
            for entry in board:
                rank  = entry["rank"] - 1
                medal = medals[rank] if rank < len(medals) else "🌱"
                is_me = entry["username"] == st.session_state.username
                bg    = "var(--green-50)" if is_me else "var(--white)"
                border= "2px solid var(--green-300)" if is_me else "1px solid var(--gray-200)"
                st.markdown(f"""
                <div class="lb-row" style="background:{bg};border:{border}">
                  <div class="lb-rank">{medal}</div>
                  <div class="lb-name">
                    {entry['username']}
                    {'<span style="font-size:0.75rem;color:var(--green-500);margin-left:0.4rem">← You</span>' if is_me else ""}
                  </div>
                  <span class="badge badge-green">{entry['eco_points']} pts</span>
                </div>""", unsafe_allow_html=True)

        with col2:
            section("📊 Points Distribution")
            if board:
                names = [e["username"] for e in board[:5]]
                pts   = [e["eco_points"] for e in board[:5]]
                greens= ["#0a3d1f","#1e8449","#27ae60","#52c47e","#a8dfc3"]
                fig = go.Figure(go.Bar(
                    y=names[::-1], x=pts[::-1],
                    orientation="h",
                    marker_color=greens[::-1],
                    marker_line_width=0,
                    text=[f"{p} pts" for p in pts[::-1]],
                    textposition="outside",
                ))
                fig.update_layout(
                    height=280, margin=dict(l=0,r=60,t=10,b=0),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(showgrid=False, showticklabels=False),
                    yaxis=dict(showgrid=False),
                    font=dict(family="DM Sans"),
                )
                st.plotly_chart(fig, use_container_width=True)

            section("🌱 How to Earn Points")
            actions = [
                ("🔬 Classify Waste", "+10 pts"),
                ("📣 File Complaint", "+20 pts"),
                ("✅ Report Resolved", "+5 pts (bonus)"),
                ("📅 Daily Login",    "+2 pts"),
            ]
            for act, pts in actions:
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;
                     padding:0.5rem 0;border-bottom:1px solid var(--gray-100)">
                  <span>{act}</span>
                  <span class="badge badge-green">{pts}</span>
                </div>""", unsafe_allow_html=True)
    elif r:
        st.error("Failed to load leaderboard")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ══════════════════════════════════════════════════════════════════════════════

def main():
    if not st.session_state.logged_in:
        render_auth()
        return

    page_key = render_sidebar()

    # Override from quick-action buttons
    if "_nav" in st.session_state:
        page_key = st.session_state.pop("_nav")

    page_map = {
        # Admin
        "admin_home": page_admin_home,
        "heatmap":    page_heatmap,
        "analytics":  page_analytics,
        "route":      page_route,
        "complaints": page_complaints,
        # Citizen
        "citizen_home": page_citizen_home,
        "classify":     page_classify,
        "report":       page_report,
        "ecopoints":    page_ecopoints,
        # Shared
        "leaderboard":  page_leaderboard,
    }

    fn = page_map.get(page_key)
    if fn:
        fn()
    else:
        st.error(f"Page '{page_key}' not found")


main()