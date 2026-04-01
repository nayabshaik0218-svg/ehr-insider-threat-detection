import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("ehr_logs.csv")

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek

# Feature: Night access
df["is_night_access"] = df["hour"].apply(lambda x: 1 if (x < 8 or x > 18) else 0)

# ----------------------------
# ENCODE CATEGORICAL DATA
# ----------------------------
encoders = {}
for col in ["user_id", "role", "patient_id", "action", "department", "device", "location"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# ----------------------------
# FEATURES
# ----------------------------
features = [
    "user_id", "role", "patient_id", "action",
    "department", "device", "location",
    "hour", "day_of_week", "is_night_access"
]

X = df[features]

# ----------------------------
# TRAIN MODEL
# ----------------------------
model = IsolationForest(
    n_estimators=200,
    contamination=0.10,
    random_state=42
)

model.fit(X)

# ----------------------------
# PREDICTION
# ----------------------------
df["anomaly"] = model.predict(X)
df["prediction"] = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)

# ----------------------------
# EVALUATION (NEW 🔥)
# ----------------------------
if "label" in df.columns:
    print("\n📊 MODEL EVALUATION")
    print("-" * 40)

    print("Accuracy:", accuracy_score(df["label"], df["prediction"]))
    print("\nConfusion Matrix:")
    print(confusion_matrix(df["label"], df["prediction"]))

    print("\nClassification Report:")
    print(classification_report(df["label"], df["prediction"]))

# ----------------------------
# ANOMALY SCORE
# ----------------------------
df["anomaly_score"] = model.decision_function(X)

# ----------------------------
# SAVE ALERTS
# ----------------------------
alerts = df[df["prediction"] == 1].copy()

original = pd.read_csv("ehr_logs.csv")
alerts_readable = original.loc[alerts.index].copy()
alerts_readable["anomaly_score"] = alerts["anomaly_score"].values

alerts_readable = alerts_readable.sort_values("anomaly_score")

alerts_readable.to_csv("alerts.csv", index=False)

print("\n✅ Threat detection completed!")
print(f"Total logs: {len(df)}")
print(f"Suspicious logs detected: {len(alerts_readable)}")