import streamlit as st
import os

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="EHR Cyber Threat Console",
    page_icon="🛡",
    layout="wide"
)

# ----------------------------
# AUTO DATA GENERATION (CLOUD SAFE)
# ----------------------------
if not os.path.exists("ehr_logs.csv"):
    st.warning("⚠ Generating dataset... Please wait")

    try:
        import logs
        import detect_insider_threats
        import risk_scoring

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
# HEADER
# ----------------------------
st.markdown("""
<h1 style='text-align:center; color:#38bdf8;'>
🛡 EHR Insider Threat Detection System
</h1>
<p style='text-align:center; color:gray;'>
Real-time Security Monitoring Dashboard
</p>
""", unsafe_allow_html=True)

# ----------------------------
# SIDEBAR
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

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("""
<hr>
<p style='text-align:center; color:gray;'>
Developed by Nayab | Cyber Security Project
</p>
""", unsafe_allow_html=True)