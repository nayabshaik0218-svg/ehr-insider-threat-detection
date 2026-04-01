import streamlit as st
import pandas as pd
import time
import risk_scoring
import detect_insider_threats

st.set_page_config(page_title="⚡ SOC WAR ROOM", layout="wide")

# ------------------ CSS ------------------
st.markdown("""
<style>
body {background-color:#05070d;color:#00ffe1;}
.metric {
    background:#0f172a;
    padding:20px;
    border-radius:12px;
    text-align:center;
    box-shadow:0 0 20px rgba(0,255,255,0.2);
}
.alert-critical {
    background:#2b0000;
    border-left:5px solid red;
    padding:10px;
    margin-bottom:8px;
}
.alert-warning {
    background:#2b2200;
    border-left:5px solid orange;
    padding:10px;
    margin-bottom:8px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ NAV ------------------
menu = ["🏠 Home","📊 Dashboard","🚨 Alerts","📈 Analytics","📜 Logs"]
tab = st.radio("", menu, horizontal=True)

# ------------------ LOAD DATA ------------------
df_rule = risk_scoring.process_data("ehr_logs.csv")
df_ml = detect_insider_threats.run_detection("ehr_logs.csv")

df = df_rule.copy()
df["ml_threat"] = df_ml["ml_threat"]
df["anomaly_score"] = df_ml["anomaly_score"]

df["final_threat"] = (
    (df["risk_level"] == "High Risk") |
    (df["ml_threat"] == 1)
)

# ------------------ HOME ------------------
if tab == "🏠 Home":
    st.markdown("## 🔥 Threat Command Center")

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f"<div class='metric'><h2>{len(df)}</h2><p>Events</p></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric'><h2>{len(df[df['final_threat']])}</h2><p>Threats</p></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='metric'><h2>{df['user_id'].nunique()}</h2><p>Users</p></div>", unsafe_allow_html=True)
    col4.markdown(f"<div class='metric'><h2>{round(df['risk_score'].mean(),1)}</h2><p>Avg Risk</p></div>", unsafe_allow_html=True)

    st.line_chart(df["risk_score"])

# ------------------ DASHBOARD ------------------
elif tab == "📊 Dashboard":
    st.markdown("## 📊 Deep Analysis")

    col1, col2 = st.columns(2)
    col1.bar_chart(df["action"].value_counts())
    col2.bar_chart(df.groupby("user_id")["risk_score"].mean())

# ------------------ ALERTS ------------------
elif tab == "🚨 Alerts":
    st.markdown("## 🚨 AI Threat Feed")

    alerts = df[df["final_threat"]]

    for _, row in alerts.sort_values("risk_score", ascending=False).head(20).iterrows():
        st.markdown(f"""
        <div class='alert-critical'>
        🔥 {row['user_id']} | {row['action']} | Risk {row['risk_score']}<br>
        ML: {row['ml_threat']} | Score: {round(row['anomaly_score'],3)}
        </div>
        """, unsafe_allow_html=True)

# ------------------ ANALYTICS ------------------
elif tab == "📈 Analytics":
    st.markdown("## 📈 AI Insights")

    st.scatter_chart(df[["risk_score","anomaly_score"]])
    st.dataframe(df[df["ml_threat"] == 1].head(20))

# ------------------ LOGS ------------------
elif tab == "📜 Logs":
    st.markdown("## 📜 Live Logs")

    log_box = st.empty()

    for _, row in df.sample(30).iterrows():
        log_box.text(f"{row['timestamp']} | {row['user_id']} | {row['action']} | Risk {row['risk_score']}")
        time.sleep(0.2)