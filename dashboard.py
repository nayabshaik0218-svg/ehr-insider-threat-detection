import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("ehr_logs_with_risk.csv")
alerts = pd.read_csv("high_risk_alerts.csv")

st.title("📊 Security Operations Dashboard")

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Logs", len(df))
col2.metric("Alerts", len(alerts))
col3.metric("Users", df["user_id"].nunique())
col4.metric("High Risk", len(df[df["risk_level"]=="High Risk"]))

risk = df["risk_level"].value_counts().reset_index()
risk.columns=["risk","count"]

fig = px.bar(risk, x="risk", y="count", color="risk")

st.plotly_chart(fig, width="stretch")
