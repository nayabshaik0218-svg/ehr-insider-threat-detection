import streamlit as st
import pandas as pd
import streamlit as st

def run():
    st.title("🚨 Alerts")
    st.write("High-risk alerts displayed here")

# ----------------------------
# LOAD DATA
# ----------------------------
alerts = pd.read_csv("high_risk_alerts.csv")

# ----------------------------
# HEADER
# ----------------------------
st.markdown("## 🚨 Security Alerts Center")
st.caption("Monitor and investigate high-risk activities in real time")

# ----------------------------
# 🔥 TOP SUMMARY
# ----------------------------
total_alerts = len(alerts)
high_risk_users = alerts["user_id"].nunique()

col1, col2 = st.columns(2)

col1.metric("🚨 Total Alerts", total_alerts)
col2.metric("👤 Affected Users", high_risk_users)

st.divider()

# ----------------------------
# 🔍 FILTERS
# ----------------------------
st.subheader("🔍 Filter Alerts")

col1, col2 = st.columns(2)

with col1:
    user_filter = st.selectbox(
        "Select User",
        ["All"] + sorted(alerts["user_id"].unique().tolist())
    )

with col2:
    action_filter = st.selectbox(
        "Select Action",
        ["All"] + sorted(alerts["action"].unique().tolist())
    )

filtered = alerts.copy()

if user_filter != "All":
    filtered = filtered[filtered["user_id"] == user_filter]

if action_filter != "All":
    filtered = filtered[filtered["action"] == action_filter]

# ----------------------------
# 🔍 SEARCH BAR
# ----------------------------
search = st.text_input("🔎 Search alerts")

if search:
    filtered = filtered[
        filtered.astype(str).apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
    ]

# ----------------------------
# 🚨 ALERT CARDS (TOP 10)
# ----------------------------
st.subheader("🔥 Recent Critical Alerts")

for _, row in filtered.head(10).iterrows():
    st.markdown(f"""
    <div style='
        background-color:#7f1d1d;
        padding:15px;
        border-radius:10px;
        margin-bottom:10px;
        color:white;
    '>
    🚨 <b>User:</b> {row['user_id']} <br>
    ⚡ <b>Action:</b> {row['action']} <br>
    🔥 <b>Risk Score:</b> {row['risk_score']}
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ----------------------------
# 📊 ALERT INSIGHTS
# ----------------------------
st.subheader("📊 Alert Insights")

col1, col2 = st.columns(2)

with col1:
    st.write("Top Users Generating Alerts")
    st.bar_chart(filtered["user_id"].value_counts().head(5))

with col2:
    st.write("Most Common Actions")
    st.bar_chart(filtered["action"].value_counts())

st.divider()

# ----------------------------
# 📋 FULL ALERT TABLE
# ----------------------------
st.subheader("📜 All Alerts")

def highlight_alert(row):
    return ["background-color: #7f1d1d"] * len(row)

st.dataframe(
    filtered.style.apply(highlight_alert, axis=1),
    use_container_width=True
)

# ----------------------------
# 🔄 REFRESH BUTTON
# ----------------------------
if st.button("🔄 Refresh Alerts"):
    st.rerun()