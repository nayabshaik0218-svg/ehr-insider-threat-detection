import streamlit as st
import pandas as pd

df = pd.read_csv("ehr_logs_with_risk.csv")

st.title("📈 Analytics")

# Risk Distribution
st.subheader("Risk Distribution")
st.bar_chart(df["risk_level"].value_counts())

# Activity by Hour
df["timestamp"] = pd.to_datetime(df["timestamp"])
hour_data = df.groupby(df["timestamp"].dt.hour).size()

st.subheader("Activity by Hour")
st.line_chart(hour_data)