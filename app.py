import streamlit as st
import os
import subprocess

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="EHR Cyber Threat Console",
    page_icon="🛡",
    layout="wide"
)

# ----------------------------
# AUTO DATA GENERATION (IMPORTANT)
# ----------------------------
if not os.path.exists("ehr_logs.csv"):
    st.warning("⚠ Generating dataset... Please wait")

    try:
        subprocess.run(["python", "logs.py"], check=True)
        subprocess.run(["python", "detect_insider_threats.py"], check=True)
        subprocess.run(["python", "risk_scoring.py"], check=True)

        st.success("✅ Data generated successfully!")

    except Exception as e:
        st.error(f"❌ Error generating data: {e}")

# ----------------------------
# LOAD STYLES
# ----------------------------
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    st.warning("⚠ Style file not found")

# ----------------------------
# SIDEBAR NAVIGATION
# ----------------------------
st.sidebar.title("🛡 SOC Console")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Security Dashboard",
        "📈 Threat Analytics",
        "🚨 Alerts Center",
        "📜 System Logs"
    ]
)

# ----------------------------
# PAGE ROUTING
# ----------------------------
if page == "🏠 Home":
    import home

elif page == "📊 Security Dashboard":
    import dashboard

elif page == "📈 Threat Analytics":
    import analytics

elif page == "🚨 Alerts Center":
    import alerts

elif page == "📜 System Logs":
    import logs