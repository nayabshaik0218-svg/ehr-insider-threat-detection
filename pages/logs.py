import streamlit as st
import pandas as pd
import streamlit as st

def run():
    st.title("📜 Logs")
    st.write("System logs and activity tracking")
# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("ehr_logs_with_risk.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# ----------------------------
# HEADER
# ----------------------------
st.markdown("## 📜 System Logs Explorer")
st.caption("Monitor real-time EHR access logs and detect suspicious activities")

# ----------------------------
# 🔥 TOP METRICS
# ----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("📁 Total Logs", len(df))
col2.metric("👥 Unique Users", df["user_id"].nunique())
col3.metric("🔥 High Risk Logs", len(df[df["risk_level"] == "High Risk"]))

st.divider()

# ----------------------------
# 🔍 FILTERS (VERY IMPORTANT)
# ----------------------------
st.subheader("🔍 Filter Logs")

col1, col2, col3 = st.columns(3)

with col1:
    user_filter = st.selectbox(
        "Select User",
        ["All"] + sorted(df["user_id"].unique().tolist())
    )

with col2:
    risk_filter = st.selectbox(
        "Risk Level",
        ["All"] + sorted(df["risk_level"].unique().tolist())
    )

with col3:
    device_filter = st.selectbox(
        "Device",
        ["All"] + sorted(df["device"].unique().tolist())
    )

# ----------------------------
# APPLY FILTERS
# ----------------------------
filtered = df.copy()

if user_filter != "All":
    filtered = filtered[filtered["user_id"] == user_filter]

if risk_filter != "All":
    filtered = filtered[filtered["risk_level"] == risk_filter]

if device_filter != "All":
    filtered = filtered[filtered["device"] == device_filter]

# ----------------------------
# 🔍 SEARCH BAR
# ----------------------------
search = st.text_input("🔎 Search logs (user / device / action)")

if search:
    filtered = filtered[
        filtered.astype(str).apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
    ]

# ----------------------------
# SORT LATEST
# ----------------------------
filtered = filtered.sort_values("timestamp", ascending=False)

# ----------------------------
# 🚨 HIGH RISK ALERT SECTION
# ----------------------------
high_risk_logs = filtered[filtered["risk_level"] == "High Risk"]

if not high_risk_logs.empty:
    st.error(f"🚨 {len(high_risk_logs)} HIGH RISK EVENTS DETECTED!")

    with st.expander("⚠ View High Risk Logs"):
        st.dataframe(high_risk_logs.head(20), use_container_width=True)

st.divider()

# ----------------------------
# 🎨 COLOR FUNCTION
# ----------------------------
def highlight_risk(row):
    if row["risk_level"] == "High Risk":
        return ["background-color: #7f1d1d"] * len(row)
    elif row["risk_level"] == "Medium Risk":
        return ["background-color: #78350f"] * len(row)
    else:
        return ["background-color: #064e3b"] * len(row)

# ----------------------------
# 📊 MAIN LOG TABLE
# ----------------------------
st.subheader("📋 Log Stream")

st.dataframe(
    filtered.head(200).style.apply(highlight_risk, axis=1),
    use_container_width=True
)

# ----------------------------
# 🔥 QUICK INSIGHTS
# ----------------------------
st.subheader("📊 Quick Insights")

col1, col2 = st.columns(2)

with col1:
    st.write("Top Users by Activity")
    st.bar_chart(filtered["user_id"].value_counts().head(5))

with col2:
    st.write("Top Devices Used")
    st.bar_chart(filtered["device"].value_counts())

# ----------------------------
# 🔄 AUTO REFRESH BUTTON
# ----------------------------
if st.button("🔄 Refresh Logs"):
    st.rerun()