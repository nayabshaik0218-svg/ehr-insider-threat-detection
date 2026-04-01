import streamlit as st
from streamlit_lottie import st_lottie
import requests
from datetime import datetime

# ----------------------------
# LOAD LOTTIE ANIMATION
# ----------------------------
def load(url):
    return requests.get(url).json()

anim = load("https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json")

# ----------------------------
# HERO HEADER
# ----------------------------
st.markdown("""
<h1 style='color:#22d3ee;'>🛡 EHR CYBER THREAT MONITORING</h1>
<p style='font-size:18px;'>AI-powered Security Operations Center for Healthcare Systems</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
### 🚀 What This System Does

This platform continuously monitors **Electronic Health Records (EHR)** to detect:

- 🔍 Insider Threats  
- 🚨 Suspicious Access Patterns  
- 📤 Unauthorized Data Exports  
- 🧠 Abnormal User Behaviour  

👉 Designed like a **mini SOC (Security Operations Center)**.
""")

    if st.button("🚨 Simulate Threat"):
        st.error("⚠ Simulated Insider Threat Triggered!")

with col2:
    st_lottie(anim, height=260)

st.divider()

# ----------------------------
# 🔥 LIVE STATUS PANEL
# ----------------------------
st.subheader("📡 System Live Status")

col1, col2, col3, col4 = st.columns(4)

col1.success("🟢 System Active")
col2.info(f"🕒 {datetime.now().strftime('%H:%M:%S')}")
col3.warning("⚠ Threat Level: Medium")
col4.metric("⚡ Detection Speed", "0.8s", "-12%")

st.divider()

# ----------------------------
# 🔥 FEATURE CARDS
# ----------------------------
st.subheader("🧠 Core Capabilities")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
### 🔍 Insider Threat Detection  
Detects unusual user behavior patterns using risk scoring.
""")

with c2:
    st.markdown("""
### 📊 Real-Time Analytics  
Visual dashboards show system activity and anomalies instantly.
""")

with c3:
    st.markdown("""
### 🚨 Smart Alerting  
Automatically flags high-risk events for immediate response.
""")

st.divider()

# ----------------------------
# 🔥 HOW IT WORKS
# ----------------------------
st.subheader("⚙ How It Works")

st.markdown("""
1️⃣ System collects EHR access logs  
2️⃣ Risk scoring algorithm analyzes behavior  
3️⃣ Suspicious activities are flagged  
4️⃣ Alerts are generated in real-time  
5️⃣ Dashboard visualizes everything  

👉 Simple pipeline, powerful insights.
""")

st.divider()

# ----------------------------
# 🔥 MINI DASH PREVIEW
# ----------------------------
st.subheader("📊 What You Can Explore")

col1, col2 = st.columns(2)

with col1:
    st.info("""
📊 Security Dashboard  
→ Risk distribution  
→ User behavior  
→ Device usage  
""")

    st.info("""
📈 Threat Analytics  
→ Patterns over time  
→ Anomaly detection  
""")

with col2:
    st.info("""
🚨 Alerts Center  
→ High-risk alerts  
→ Insider threats  
""")

    st.info("""
📜 System Logs  
→ Raw log monitoring  
→ Debug insights  
""")

st.divider()

# ----------------------------
# 🔥 FOOTER (CYBER STYLE)
# ----------------------------
st.markdown(
    f"""
    <center style='color:#64748b'>
    🛡 EHR Security System • Powered by AI • {datetime.now().strftime('%Y')}
    </center>
    """,
    unsafe_allow_html=True
)