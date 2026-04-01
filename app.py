import streamlit as st
import os
import time
from datetime import datetime

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="🛡 EHR Cyber Threat Console",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# CUSTOM CSS (INLINE - CRAZY UI)
# ----------------------------
st.markdown("""
<style>
/* Background */
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: #e2e8f0;
}

/* Glass Card */
.glass {
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(0,255,255,0.2);
}

/* Neon Text */
.neon {
    color: #22d3ee;
    text-shadow: 0 0 10px #22d3ee, 0 0 20px #0ea5e9;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #020617;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
    border: none;
    border-radius: 10px;
    color: white;
    font-weight: bold;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #0ea5e9;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
st.markdown("""
<h1 class='neon'>🛡 EHR CYBER THREAT CONSOLE</h1>
<p>Real-Time Threat Monitoring • AI Detection • Insider Risk Analysis</p>
""", unsafe_allow_html=True)

# ----------------------------
# SYSTEM STATUS BAR
# ----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.success("🟢 System Active")

with col2:
    st.info(f"🕒 {datetime.now().strftime('%H:%M:%S')}")

with col3:
    st.warning("⚠ Threat Level: Medium")

with col4:
    st.metric("📡 Requests/sec", "128", "+12%")

st.divider()

# ----------------------------
# AUTO DATA GENERATION
# ----------------------------
if not os.path.exists("ehr_logs.csv"):
    with st.spinner("⚡ Generating synthetic EHR logs..."):
        progress = st.progress(0)

        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        try:
            import logs
            import detect_insider_threats
            import risk_scoring

            st.success("✅ Dataset Ready!")

        except Exception as e:
            st.error(f"❌ Error: {e}")

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.markdown("## 🛡 SOC Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "🏠 Home",
        "📊 Security Dashboard",
        "📈 Threat Analytics",
        "🚨 Alerts Center",
        "📜 System Logs"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙ Controls")

if st.sidebar.button("🔄 Refresh System"):
    st.rerun()

if st.sidebar.button("🚨 Simulate Attack"):
    st.sidebar.error("Simulated breach triggered!")

st.sidebar.markdown("---")
st.sidebar.caption("👨‍💻 Developed by Cyber AI System")

# ----------------------------
# ROUTING (SAFE IMPORT + RUN)
# ----------------------------
def load_module(module_name):
    try:
        module = __import__(module_name)

        if hasattr(module, "run"):
            module.run()
        else:
            st.error(f"❌ `{module_name}.py` missing run() function")

    except Exception as e:
        st.error(f"🔥 Error loading {module_name}: {e}")

# ----------------------------
# PAGE LOAD
# ----------------------------
if page == "🏠 Home":
    load_module("home")

elif page == "📊 Security Dashboard":
    load_module("dashboard")

elif page == "📈 Threat Analytics":
    load_module("analytics")

elif page == "🚨 Alerts Center":
    load_module("alerts")

elif page == "📜 System Logs":
    load_module("logs")

# ----------------------------
# FOOTER (TERMINAL STYLE)
# ----------------------------
st.markdown("---")
st.markdown(
    f"<center style='color:#64748b'>SYSTEM STATUS: RUNNING | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</center>",
    unsafe_allow_html=True
)