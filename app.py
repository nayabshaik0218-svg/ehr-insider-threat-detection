import streamlit as st

st.set_page_config(
    page_title="EHR Monitoring",
    page_icon="📊",
    layout="wide"
)

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="header">
<h1>📊 EHR Activity Monitoring System</h1>
<p>Real-time User Behavior & Risk Insights</p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    ["🏠 Home", "📊 Dashboard", "📈 Analytics", "🚨 Alerts", "📜 Logs"]
)

# ROUTING
if page == "🏠 Home":
    import home
elif page == "📊 Dashboard":
    import dashboard
elif page == "📈 Analytics":
    import analytics
elif page == "🚨 Alerts":
    import alerts
elif page == "📜 Logs":
    import logs