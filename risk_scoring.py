import pandas as pd
import streamlit as st

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# ----------------------------
# Load dataset
# ----------------------------
df = pd.read_csv("ehr_logs.csv")

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour

# ----------------------------
# NEW FEATURE: Behavior Drift Detection
# ----------------------------
# Count how many actions each user performs
user_activity = df.groupby("user_id").size()

# Average activity across users
avg_activity = user_activity.mean()

# Detect users with abnormal spike in activity
drift_users = user_activity[user_activity > avg_activity * 2]

print("⚠ Behavior Drift Users Detected:")
print(drift_users)

# Add new column
df["behavior_drift"] = df["user_id"].apply(
    lambda u: 1 if u in drift_users.index else 0
)

# ----------------------------
# Risk Scoring Function
# ----------------------------
def calculate_risk(row):

    score = 0
    reasons = []

    # 1️⃣ Night access
    if row["hour"] < 8 or row["hour"] > 18:
        score += 3
        reasons.append("Access outside working hours")

    # 2️⃣ Export action (data exfiltration)
    if row["action"] == "export":
        score += 6
        reasons.append("Export action (possible data leakage)")

    # 3️⃣ Suspicious location
    if row["location"] == "home":
        score += 3
        reasons.append("Access from home location")

    # 4️⃣ Mobile device access
    if row["device"] == "mobile":
        score += 1
        reasons.append("Access from mobile device")

    # 5️⃣ NEW FEATURE — Behavior Drift
    if row["behavior_drift"] == 1:
        score += 4
        reasons.append("Unusual spike in user activity")

    return score, ", ".join(reasons)

# ----------------------------
# Apply Risk Scoring
# ----------------------------
df[["risk_score", "reasons"]] = df.apply(
    lambda r: pd.Series(calculate_risk(r)), axis=1
)

# ----------------------------
# Risk Level Classification
# ----------------------------
def risk_level(score):

    if score <= 3:
        return "Normal"

    elif score <= 7:
        return "Suspicious"

    else:
        return "High Risk"

df["risk_level"] = df["risk_score"].apply(risk_level)

# ----------------------------
# Save Dataset with Risk
# ----------------------------
df.to_csv("ehr_logs_with_risk.csv", index=False)

# ----------------------------
# Save High Risk Alerts
# ----------------------------
high_risk = df[df["risk_level"] == "High Risk"].copy()

high_risk.to_csv("high_risk_alerts.csv", index=False)

# ----------------------------
# Output
# ----------------------------
print("✅ Risk scoring completed!")
print("✅ File saved: ehr_logs_with_risk.csv")
print("✅ High risk alerts saved: high_risk_alerts.csv")

print("\nTop 10 High Risk Alerts:")
print(high_risk.sort_values("risk_score", ascending=False).head(10))