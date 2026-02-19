import pandas as pd

# Load alerts and full logs
df = pd.read_csv("ehr_logs.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour

def calculate_risk(row):
    score = 0
    reasons = []

    # 1) Night access
    if row["hour"] < 8 or row["hour"] > 18:
        score += 3
        reasons.append("Access outside working hours")

    # 2) Export action (high risk)
    if row["action"] == "export":
        score += 6
        reasons.append("Export action (data leakage risk)")

    # 3) Location = home (suspicious)
    if row["location"] == "home":
        score += 3
        reasons.append("Access from home location")

    # 4) Device = mobile (optional)
    if row["device"] == "mobile":
        score += 1
        reasons.append("Access from mobile device")

    return score, ", ".join(reasons)

# Apply scoring
df[["risk_score", "reasons"]] = df.apply(lambda r: pd.Series(calculate_risk(r)), axis=1)

# Risk level
def risk_level(score):
    if score <= 3:
        return "Normal"
    elif score <= 7:
        return "Suspicious"
    else:
        return "High Risk"

df["risk_level"] = df["risk_score"].apply(risk_level)

# Save new dataset with score
df.to_csv("ehr_logs_with_risk.csv", index=False)

# Save only high risk alerts
high_risk = df[df["risk_level"] == "High Risk"].copy()
high_risk.to_csv("high_risk_alerts.csv", index=False)

print("✅ Risk scoring completed!")
print("✅ Saved: ehr_logs_with_risk.csv")
print("✅ Saved: high_risk_alerts.csv")
print("\nTop 10 High Risk Alerts:")
print(high_risk.sort_values("risk_score", ascending=False).head(10))
