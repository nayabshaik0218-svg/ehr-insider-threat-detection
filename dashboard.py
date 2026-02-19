import streamlit as st
import pandas as pd

st.set_page_config(page_title="Insider Threat Detection - EHR", layout="wide")
st.title("🛡️ Insider Threat Detection Dashboard (EHR)")

# Load datasets
df = pd.read_csv("ehr_logs_with_risk.csv")
alerts = pd.read_csv("high_risk_alerts.csv")

# Top metrics
col1, col2, col3 = st.columns(3)
col1.metric("📄 Total Logs", len(df))
col2.metric("🚨 High Risk Alerts", len(alerts))
col3.metric("👤 Unique Users", df["user_id"].nunique())

st.divider()

# Filter alerts by user
st.subheader("🔍 High Risk Alerts")
user_choice = st.selectbox("Filter by User", ["All"] + sorted(alerts["user_id"].unique().tolist()))

filtered = alerts if user_choice == "All" else alerts[alerts["user_id"] == user_choice]
st.dataframe(filtered.sort_values("risk_score", ascending=False), use_container_width=True)

st.divider()

# Risk distribution chart
st.subheader("📊 Risk Level Distribution")
risk_counts = df["risk_level"].value_counts()
st.bar_chart(risk_counts)

st.divider()

# Show last 50 logs
st.subheader("📌 Latest Logs (with Risk Scores)")
st.dataframe(df.tail(50), use_container_width=True)
