import streamlit as st
import pandas as pd

st.header("📜 System Logs")

df = pd.read_csv("ehr_logs_with_risk.csv")

latest = df.sort_values("timestamp",ascending=False).head(50)

st.dataframe(latest)