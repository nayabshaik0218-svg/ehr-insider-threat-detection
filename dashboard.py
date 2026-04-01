import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("ehr_logs_with_risk.csv")
alerts = pd.read_csv("high_risk_alerts.csv")

st.title("📊 Security Operations Dashboard")

# ----------------------------
# METRICS
# ----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Logs", len(df))
col2.metric("Alerts", len(alerts))
col3.metric("Users", df["user_id"].nunique())
col4.metric("High Risk", len(df[df["risk_level"] == "High Risk"]))

# ----------------------------
# RISK DISTRIBUTION
# ----------------------------
risk = df["risk_level"].value_counts().reset_index()
risk.columns = ["risk", "count"]

fig = px.bar(risk, x="risk", y="count", color="risk")
st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# 🔥 NEW: TIME-BASED ANALYSIS
# ----------------------------
df["timestamp"] = pd.to_datetime(df["timestamp"])

time_data = df.groupby(df["timestamp"].dt.hour).size()

st.subheader("⏱ Activity by Hour")
st.line_chart(time_data)

# ----------------------------
# 🔥 NEW: TOP RISK USERS
# ----------------------------
top_users = df.groupby("user_id")["risk_score"].sum().sort_values(ascending=False).head(5)

st.subheader("👤 Top Risk Users")
st.bar_chart(top_users)

# ----------------------------
# 🔥 NEW: DEVICE DISTRIBUTION
# ----------------------------
device_data = df["device"].value_counts()

st.subheader("💻 Device Usage")
st.bar_chart(device_data)