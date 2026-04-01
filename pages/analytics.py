import streamlit as st
import pandas as pd
import plotly.express as px

st.header("📈 Threat Analytics")

df = pd.read_csv("ehr_logs_with_risk.csv")

risk_counts = df["risk_level"].value_counts().reset_index()
risk_counts.columns = ["risk_level", "count"]

fig = px.pie(
risk_counts,
values="count",
names="risk_level",
hole=0.5
)

st.plotly_chart(fig, width="stretch")