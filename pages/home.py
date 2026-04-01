import streamlit as st
from streamlit_lottie import st_lottie
import requests

def load(url):
    return requests.get(url).json()

anim = load("https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json")

st_lottie(anim,height=250)

st.markdown("""
### Cyber Threat Monitoring System

This platform monitors **Electronic Health Record (EHR)** systems to detect:

- Insider threats
- Suspicious access
- Data exfiltration
- Abnormal user behaviour
""")