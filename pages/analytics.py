import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st

def run():
    st.title("📈 Analytics")
    st.write("Analytics data and insights")
# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("ehr_logs_with_risk.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# ----------------------------
# HEADER
# ----------------------------
st.markdown("## 📈 Threat Analytics Engine")
st.caption("Analyze patterns, detect anomalies, and understand system risks")

# ----------------------------
# 🔥 KPI SUMMARY
# ----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("📁 Total Events", len(df))
col2.metric("🚨 High Risk", len(df[df["risk_level"] == "High Risk"]))
col3.metric("👥 Users", df["user_id"].nunique())

st.divider()

# ----------------------------
# 🧠 1. RISK DISTRIBUTION (DONUT)
# ----------------------------
st.subheader("🧠 Risk Distribution")

risk_counts = df["risk_level"].value_counts().reset_index()
risk_counts.columns = ["Risk", "Count"]

fig1 = px.pie(
    risk_counts,
    values="Count",
    names="Risk",
    hole=0.5,
    title="Overall Risk Breakdown"
)

st.plotly_chart(fig1, use_container_width=True)

# ----------------------------
# ⏱ 2. THREAT OVER TIME
# ----------------------------
st.subheader("⏱ Threat Activity Over Time")

time_data = df.groupby(df["timestamp"].dt.hour).size().reset_index()
time_data.columns = ["Hour", "Events"]

fig2 = px.line(
    time_data,
    x="Hour",
    y="Events",
    markers=True,
    title="Hourly Threat Pattern"
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# 👤 3. USER BEHAVIOR ANALYSIS
# ----------------------------
st.subheader("👤 User Risk Behavior")

user_risk = (
    df.groupby("user_id")["risk_score"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    user_risk,
    x="user_id",
    y="risk_score",
    color="risk_score",
    title="Top Risky Users"
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# 💻 4. DEVICE-BASED THREATS
# ----------------------------
st.subheader("💻 Device Risk Analysis")

device_risk = df.groupby("device")["risk_score"].sum().reset_index()

fig4 = px.bar(
    device_risk,
    x="device",
    y="risk_score",
    color="risk_score",
    title="Risk by Device"
)

st.plotly_chart(fig4, use_container_width=True)

# ----------------------------
# 🔥 5. ANOMALY DETECTION (SIMPLE)
# ----------------------------
st.subheader("🔥 Suspicious Activity Detection")

threshold = df["risk_score"].mean() + 2 * df["risk_score"].std()
anomalies = df[df["risk_score"] > threshold]

st.warning(f"⚠ {len(anomalies)} Potential Anomalies Detected")

st.dataframe(anomalies.head(20), use_container_width=True)

# ----------------------------
# 📊 6. HEATMAP (PATTERN VIEW)
# ----------------------------
st.subheader("📊 Activity Heatmap")

df["day"] = df["timestamp"].dt.day_name()
df["hour"] = df["timestamp"].dt.hour

heatmap_data = df.groupby(["day", "hour"]).size().reset_index(name="count")

fig5 = px.density_heatmap(
    heatmap_data,
    x="hour",
    y="day",
    z="count",
    title="Activity Pattern Heatmap"
)

st.plotly_chart(fig5, use_container_width=True)

# ----------------------------
# 📜 RAW DATA (OPTIONAL)
# ----------------------------
with st.expander("📜 View Raw Data"):
    st.dataframe(df.head(100))