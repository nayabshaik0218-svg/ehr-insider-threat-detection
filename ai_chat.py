import streamlit as st
from openai import OpenAI
import pandas as pd
import os

def run():
    st.header("🤖 AI Assistant")

    if "OPENAI_API_KEY" not in os.environ:
        st.error("❌ Please set OPENAI_API_KEY in terminal")
        return

    client = OpenAI()

    df = pd.read_csv("ehr_logs_with_risk.csv")

    user_input = st.text_input("Ask something about logs")

    if user_input:

        context = f"""
        You are analyzing system logs.

        Total logs: {len(df)}
        Users: {df['user_id'].nunique()}
        Risk levels: {df['risk_level'].value_counts().to_dict()}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": user_input}
            ]
        )

        answer = response.choices[0].message.content

        st.success(answer)