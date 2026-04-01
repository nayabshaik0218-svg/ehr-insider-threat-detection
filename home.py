import streamlit as st
from streamlit_lottie import st_lottie
import requests

def load(url):
    return requests.get(url).json()

anim = load("https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json")

st.title("🛡 EHR Cyber Threat Monitoring")

st_lottie(anim, height=250)

st.write("""
This **Security Operations Dashboard** monitors Electronic Health Records to detect:

• Insider threats  
• Suspicious access patterns  
• Data export attempts  
• Abnormal user behaviour
""")
