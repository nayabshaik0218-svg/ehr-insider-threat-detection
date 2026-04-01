import streamlit as st
import pandas as pd

st.title("🚨 Alerts Center")

alerts = pd.read_csv("high_risk_alerts.csv")

st.error(f"{len(alerts)} High Risk Alerts Detected")

for _, row in alerts.head(10).iterrows():
    st.markdown(f"""
    <div class="card">
    🔴 <b>User:</b> {row['user_id']} <br>
    ⚡ <b>Action:</b> {row['action']} <br>
    🔥 <b>Risk Score:</b> {row['risk_score']}
    </div>
    """, unsafe_allow_html=True)