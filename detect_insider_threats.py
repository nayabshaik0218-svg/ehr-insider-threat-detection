import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

# ----------------------------
# 1) Load Dataset
# ----------------------------
df = pd.read_csv("ehr_logs.csv")

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek

# Feature: Night access (suspicious)
df["is_night_access"] = df["hour"].apply(lambda x: 1 if (x < 8 or x > 18) else 0)

# ----------------------------
# 2) Encode Categorical Features
# ----------------------------
encoders = {}
for col in ["user_id", "role", "patient_id", "action", "department", "device", "location"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# ----------------------------
# 3) Prepare Features for ML
# ----------------------------
features = ["user_id", "role", "patient_id", "action", "department", "device",
            "location", "hour", "day_of_week", "is_night_access"]

X = df[features]

# ----------------------------
# 4) Train Isolation Forest
# ----------------------------
model = IsolationForest(
    n_estimators=200,
    contamination=0.10,  # assumes 10% anomalies
    random_state=42
)

model.fit(X)

# Predict anomalies (-1 = anomaly, 1 = normal)
df["anomaly"] = model.predict(X)

# Anomaly score (lower = more suspicious)
df["anomaly_score"] = model.decision_function(X)

# Convert anomaly to label
df["prediction"] = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)

# ----------------------------
# 5) Generate Alerts (only suspicious logs)
# ----------------------------
alerts = df[df["prediction"] == 1].copy()

# Decode back useful readable info (optional)
# (Since we encoded values, we will reload original CSV for readable output)
original = pd.read_csv("ehr_logs.csv")
alerts_readable = original.loc[alerts.index].copy()
alerts_readable["anomaly_score"] = alerts["anomaly_score"].values

alerts_readable = alerts_readable.sort_values("anomaly_score")

alerts_readable.to_csv("alerts.csv", index=False)

print("✅ Threat detection completed!")
print(f"Total logs: {len(df)}")
print(f"Suspicious logs detected: {len(alerts_readable)}")
print("✅ Alerts saved as: alerts.csv")
print("\nTop 10 suspicious entries:")
print(alerts_readable.head(10))
