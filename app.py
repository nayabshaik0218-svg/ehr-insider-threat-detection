import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="🚨 SOC Dashboard", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
body {
    background-color: #0d1117;
    color: white;
}
.navbar {
    display: flex;
    justify-content: center;
    gap: 40px;
    padding: 15px;
    background: #161b22;
    border-radius: 10px;
    margin-bottom: 20px;
}
.nav-btn {
    font-size: 18px;
    font-weight: bold;
    color: #58a6ff;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("""
<h1 style='text-align:center;color:red;'>🚨 CYBER SECURITY SOC</h1>
""", unsafe_allow_html=True)

# ------------------ NAVIGATION ------------------
menu = ["🏠 Home", "📊 Dashboard", "🚨 Alerts", "📈 Analytics", "📜 Logs"]
choice = st.radio("", menu, horizontal=True)

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    try:
        return pd.read_csv("high_risk_alerts.csv")
    except:
        return pd.DataFrame({
            "user_id": ["U101", "U102", "U103"],
            "action": ["Login Failure", "Data Download", "Privilege Escalation"],
            "risk_score": [85, 92, 78]
        })

df = load_data()

# ------------------ HOME ------------------
if choice == "🏠 Home":
    st.markdown("## 🏠 Welcome to SOC AI System")
    st.write("Monitor threats, detect anomalies, and secure systems in real-time.")
    st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b", use_container_width=True)

# ------------------ DASHBOARD ------------------
elif choice == "📊 Dashboard":
    st.markdown("## 📊 System Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("🚨 Total Alerts", len(df))
    col2.metric("⚠️ High Risk", len(df[df["risk_score"] > 80]))
    col3.metric("👥 Users", df["user_id"].nunique())

    st.bar_chart(df["risk_score"])

# ------------------ ALERTS ------------------
elif choice == "🚨 Alerts":
    st.markdown("## 🚨 High Risk Alerts")

    for _, row in df.iterrows():
        if row["risk_score"] > 80:
            st.error(f"🔥 {row['user_id']} → {row['action']} (Risk {row['risk_score']})")
        else:
            st.warning(f"⚠️ {row['user_id']} → {row['action']}")

# ------------------ ANALYTICS ------------------
elif choice == "📈 Analytics":
    st.markdown("## 📈 Analytics Insights")

    st.line_chart(df["risk_score"])
    st.area_chart(df["risk_score"])

# ------------------ LOGS ------------------
elif choice == "📜 Logs":
    st.markdown("## 📜 Live Logs")

    log_box = st.empty()
    logs = [
        "User login success",
        "Failed password attempt",
        "Sensitive file accessed",
        "Admin privilege escalation",
    ]

    for log in logs:
        log_box.text(log)
        time.sleep(0.5)