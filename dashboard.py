import streamlit as st
import pandas as pd

df = pd.read_csv("ehr_logs_with_risk.csv")
alerts = pd.read_csv("high_risk_alerts.csv")

st.markdown("## 📊 System Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Logs", len(df))

with col2:
    st.metric("Alerts", len(alerts))

with col3:
    st.metric("Users", df["user_id"].nunique())

with col4:
    st.metric("High Risk", len(df[df["risk_level"] == "High Risk"]))

st.markdown("---")

# Top users
st.markdown("### 🔥 Top Risk Users")

top_users = df.groupby("user_id")["risk_score"].sum().sort_values(ascending=False).head(5)

st.bar_chart(top_users)