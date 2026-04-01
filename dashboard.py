import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("ehr_logs_with_risk.csv")
alerts = pd.read_csv("high_risk_alerts.csv")

st.title("📊 Security Operations Dashboard")

# ----------------------------
# METRICS
# ----------------------------
st.markdown("### 📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Logs", len(df))

with col2:
    st.metric("Alerts", len(alerts))

with col3:
    st.metric("Users", df["user_id"].nunique())

with col4:
    st.metric("High Risk", len(df[df["risk_level"] == "High Risk"]))

# ----------------------------
# RISK DISTRIBUTION
# ----------------------------
risk = df["risk_level"].value_counts().reset_index()
risk.columns = ["risk", "count"]

fig = px.bar(
    risk,
    x="risk",
    y="count",
    color="risk",
    title="Risk Distribution",
    template="plotly_dark"
)

st.plotly_chart(fig, width="stretch")

# ----------------------------
# TIME ANALYSIS
# ----------------------------
df["timestamp"] = pd.to_datetime(df["timestamp"])
time_data = df.groupby(df["timestamp"].dt.hour).size()

st.subheader("⏱ Activity by Hour")
st.line_chart(time_data)

# ----------------------------
# TOP USERS
# ----------------------------
top_users = df.groupby("user_id")["risk_score"].sum().sort_values(ascending=False).head(5)

st.subheader("👤 Top Risk Users")
st.bar_chart(top_users)

# ----------------------------
# DEVICE DISTRIBUTION
# ----------------------------
device_data = df["device"].value_counts()

st.subheader("💻 Device Usage")
st.bar_chart(device_data)

# ----------------------------
# ALERT SUMMARY
# ----------------------------
st.markdown("### 🚨 Alert Summary")

st.error(f"⚠ {len(alerts)} High Risk Alerts Detected")

for _, row in alerts.head(5).iterrows():
    st.markdown(f"""
    <div class="alert">
    <b>User:</b> {row['user_id']}<br>
    <b>Action:</b> {row['action']}<br>
    <b>Risk Score:</b> {row['risk_score']}
    </div>
    """, unsafe_allow_html=True)
st.markdown('<div class="card">📊 Key Metrics</div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
System Status: Active | Monitoring Enabled | Data Processing Running
</div>
""", unsafe_allow_html=True)