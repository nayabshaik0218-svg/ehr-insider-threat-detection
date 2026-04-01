import streamlit as st
import pandas as pd

st.title("📜 System Logs")

df = pd.read_csv("ehr_logs_with_risk.csv")

st.dataframe(df.head(100))