import streamlit as st
import pandas as pd
import time
import numpy as np

st.set_page_config(page_title="SOC AI", layout="wide")

# ------------------ CSS (CRAZY UI) ------------------
st.markdown("""
<style>
body {
    background-color: #0d1117;
    color: #e6edf3;
}
.block-container {
    padding-top: 2rem;
}
.metric-card {
    background: linear-gradient(135deg, #161b22, #0d1117);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 0 20px rgba(0,255,255,0.1);
}
.alert-high {
    background-color: #2c0b0e;
    padding: 12px;
    border-left: 5px solid red;
    border-radius: 8px;
    margin-bottom: 10px;
}
.alert-medium {
    background-color: #2c2a0b;
    padding: 12px;
    border-left: 5px solid orange;
    border-radius: 8px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("<h1 style='text-align:center;color:#ff4b4b;'>🚨 AI SOC COMMAND CENTER</h1>", unsafe_allow_html=True)

# ------------------ NAV ------------------
menu = ["🏠 Home", "📊 Dashboard", "🚨 Alerts", "📈 Analytics", "📜 Logs"]
choice = st.radio("", menu, horizontal=True)

# ------------------ DATA ------------------
@st.cache_data
def load_data():
    try:
        return pd.read_csv("high_risk_alerts.csv")
    except:
        return pd.DataFrame({
            "user_id": np.random.choice(["U101","U102","U103","U104"], 50),
            "action": np.random.choice(["Login Failure","Download","Privilege Escalation"], 50),
            "risk_score": np.random.randint(50,100,50)
        })

df = load_data()

# ------------------ HOME (POWERFUL) ------------------
if choice == "🏠 Home":
    st.markdown("## 🔥 Threat Intelligence Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f"<div class='metric-card'><h2>{len(df)}</h2><p>Total Events</p></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric-card'><h2>{len(df[df['risk_score']>80])}</h2><p>Critical Threats</p></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='metric-card'><h2>{df['user_id'].nunique()}</h2><p>Users</p></div>", unsafe_allow_html=True)
    col4.markdown(f"<div class='metric-card'><h2>{df['action'].nunique()}</h2><p>Attack Types</p></div>", unsafe_allow_html=True)

    st.divider()

    st.markdown("### 🧠 AI Threat Pulse")
    st.progress(int(df["risk_score"].mean()))

    st.markdown("### 🌍 Attack Activity Heat")
    st.line_chart(df["risk_score"])

# ------------------ DASHBOARD (FULL ANALYSIS) ------------------
elif choice == "📊 Dashboard":
    st.markdown("## 📊 Deep System Analytics")

    col1, col2 = st.columns(2)

    col1.subheader("📈 Risk Trend")
    col1.line_chart(df["risk_score"])

    col2.subheader("📊 Risk Distribution")
    col2.bar_chart(df["risk_score"])

    st.divider()

    col3, col4 = st.columns(2)

    col3.subheader("👥 User Activity")
    col3.bar_chart(df["user_id"].value_counts())

    col4.subheader("⚔️ Attack Types")
    col4.bar_chart(df["action"].value_counts())

# ------------------ ALERTS (CRAZY VISUALS) ------------------
elif choice == "🚨 Alerts":
    st.markdown("## 🚨 Real-Time Threat Alerts")

    for _, row in df.sort_values("risk_score", ascending=False).head(15).iterrows():
        if row["risk_score"] > 85:
            st.markdown(f"<div class='alert-high'>🔥 CRITICAL: {row['user_id']} → {row['action']} | Risk {row['risk_score']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='alert-medium'>⚠️ WARNING: {row['user_id']} → {row['action']} | Risk {row['risk_score']}</div>", unsafe_allow_html=True)

# ------------------ ANALYTICS (CLEAR INSIGHTS) ------------------
elif choice == "📈 Analytics":
    st.markdown("## 📈 Behavioral Analytics")

    st.subheader("📊 Risk Score Breakdown")
    st.area_chart(df["risk_score"])

    st.subheader("🧠 Anomaly Detection (Simulated)")
    df["anomaly"] = df["risk_score"] > 90
    st.dataframe(df[df["anomaly"] == True])

# ------------------ LOGS (REAL-TIME FEEL) ------------------
elif choice == "📜 Logs":
    st.markdown("## 📜 Live System Logs")

    log_box = st.empty()

    logs = [
        "🔐 User U101 login success",
        "❌ Failed password attempt",
        "📂 Sensitive file accessed",
        "⚡ Privilege escalation detected",
        "🌐 External IP connection flagged",
    ]

    for log in logs:
        log_box.markdown(f"`{log}`")
        time.sleep(0.6)