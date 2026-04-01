import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("ehr_logs_with_risk.csv")
alerts = pd.read_csv("high_risk_alerts.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])

# ----------------------------
# TITLE
# ----------------------------
st.markdown("## 📊 Security Operations Dashboard")
st.caption("Real-time monitoring of EHR system risks and activities")

# ----------------------------
# 🔥 KPI METRICS (WITH COLORS)
# ----------------------------
total_logs = len(df)
total_alerts = len(alerts)
total_users = df["user_id"].nunique()
high_risk = len(df[df["risk_level"] == "High Risk"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("📁 Total Logs", total_logs)
col2.metric("🚨 Alerts", total_alerts)
col3.metric("👥 Users", total_users)
col4.metric("🔥 High Risk Events", high_risk)

st.divider()

# ----------------------------
# 🔥 RISK DISTRIBUTION (COLORFUL)
# ----------------------------
st.subheader("🧠 Risk Distribution Overview")

risk = df["risk_level"].value_counts().reset_index()
risk.columns = ["Risk Level", "Count"]

fig = px.bar(
    risk,
    x="Risk Level",
    y="Count",
    color="Risk Level",
    text="Count",
    title="Risk Level Breakdown"
)

fig.update_traces(textposition="outside")

st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# 🔥 TIME ANALYSIS (WHEN ATTACKS HAPPEN)
# ----------------------------
st.subheader("⏱ When Activities Happen")

time_data = df.groupby(df["timestamp"].dt.hour).size().reset_index()
time_data.columns = ["Hour", "Activity Count"]

fig2 = px.line(
    time_data,
    x="Hour",
    y="Activity Count",
    markers=True,
    title="Hourly Activity Pattern"
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# 🔥 TOP RISK USERS (WHO IS DANGEROUS)
# ----------------------------
st.subheader("👤 Most Risky Users")

top_users = (
    df.groupby("user_id")["risk_score"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig3 = px.bar(
    top_users,
    x="user_id",
    y="risk_score",
    color="risk_score",
    text="risk_score",
    title="Top 5 High Risk Users"
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# 🔥 DEVICE ANALYSIS (FROM WHERE)
# ----------------------------
st.subheader("💻 Device Usage Analysis")

device_data = df["device"].value_counts().reset_index()
device_data.columns = ["Device", "Count"]

fig4 = px.pie(
    device_data,
    names="Device",
    values="Count",
    title="Device Distribution"
)

st.plotly_chart(fig4, use_container_width=True)

# ----------------------------
# 🔥 NEW: HEATMAP (DAY vs HOUR)
# ----------------------------
st.subheader("🔥 Activity Heatmap (Day vs Hour)")

df["day"] = df["timestamp"].dt.day_name()
df["hour"] = df["timestamp"].dt.hour

heatmap_data = df.groupby(["day", "hour"]).size().reset_index(name="count")

fig5 = px.density_heatmap(
    heatmap_data,
    x="hour",
    y="day",
    z="count",
    title="User Activity Heatmap"
)

st.plotly_chart(fig5, use_container_width=True)

# ----------------------------
# 🔥 NEW: RAW DATA VIEW (FOR DEBUG)
# ----------------------------
with st.expander("📜 View Raw Data"):
    st.dataframe(df.head(100))
