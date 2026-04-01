import streamlit as st
import pandas as pd

st.header("🚨 Threat Alerts")

alerts = pd.read_csv("high_risk_alerts.csv")

for _,row in alerts.head(10).iterrows():
    st.error(
        f"User {row['user_id']} performed {row['action']} | Risk Score {row['risk_score']}"
    )

st.dataframe(alerts)