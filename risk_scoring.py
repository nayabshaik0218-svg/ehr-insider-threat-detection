import pandas as pd

def process_data(file="ehr_logs.csv"):

    df = pd.read_csv(file)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour

    # Behavior Drift
    user_activity = df.groupby("user_id").size()
    avg_activity = user_activity.mean()
    drift_users = user_activity[user_activity > avg_activity * 2]

    df["behavior_drift"] = df["user_id"].apply(
        lambda u: 1 if u in drift_users.index else 0
    )

    # Risk scoring
    def calculate_risk(row):
        score = 0
        reasons = []

        if row["hour"] < 8 or row["hour"] > 18:
            score += 3
            reasons.append("Access outside working hours")

        if row["action"] == "export":
            score += 6
            reasons.append("Sensitive data export")

        if row["location"] == "home":
            score += 3
            reasons.append("Remote access")

        if row["device"] == "mobile":
            score += 1
            reasons.append("Mobile usage")

        if row["behavior_drift"] == 1:
            score += 4
            reasons.append("Unusual activity spike")

        return score, ", ".join(reasons)

    df[["risk_score", "reasons"]] = df.apply(
        lambda r: pd.Series(calculate_risk(r)), axis=1
    )

    def risk_level(score):
        if score <= 3:
            return "Normal"
        elif score <= 7:
            return "Suspicious"
        else:
            return "High Risk"

    df["risk_level"] = df["risk_score"].apply(risk_level)

    return df