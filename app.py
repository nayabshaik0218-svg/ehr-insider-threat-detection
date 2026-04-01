import streamlit as st

st.set_page_config(
    page_title="EHR Cyber Threat Console",
    page_icon="🛡",
    layout="wide"
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.sidebar.title("🛡 SOC Console")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Security Dashboard",
        "📈 Threat Analytics",
        "🚨 Alerts Center",
        "📜 System Logs"
    ]
)

if page == "🏠 Home":
    import home

elif page == "📊 Security Dashboard":
    import dashboard

elif page == "📈 Threat Analytics":
    import analytics

elif page == "🚨 Alerts Center":
    import alerts

elif page == "📜 System Logs":
    import logs
