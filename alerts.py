import streamlit as st
import pandas as pd

st.title("🚨 Security Alerts")

alerts = pd.read_csv("high_risk_alerts.csv")

st.warning(f"{len(alerts)} high-risk alerts detected")

for _,row in alerts.head(10).iterrows():
    st.error(f"User {row['user_id']} executed {row['action']} | Risk Score {row['risk_score']}")

st.dataframe(alerts, width="stretch")
