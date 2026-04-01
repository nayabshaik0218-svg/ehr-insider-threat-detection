import streamlit as st
import pandas as pd

st.title("📜 System Logs")

df = pd.read_csv("ehr_logs_with_risk.csv")

latest = df.sort_values("timestamp",ascending=False).head(100)

st.dataframe(latest, width="stretch")
