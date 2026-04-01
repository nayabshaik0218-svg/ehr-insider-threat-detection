import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

def run_detection(file="ehr_logs.csv"):

    df = pd.read_csv(file)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.dayofweek

    df["is_night"] = df["hour"].apply(lambda x: 1 if (x < 8 or x > 18) else 0)

    # Encode categorical columns
    for col in ["user_id","role","patient_id","action","department","device","location"]:
        df[col] = LabelEncoder().fit_transform(df[col])

    features = [
        "user_id","role","patient_id","action",
        "department","device","location",
        "hour","day","is_night"
    ]

    # 🔥 CRITICAL FIX (convert to NUMPY for BOTH fit & predict)
    X = df[features].values

    model = IsolationForest(
        n_estimators=200,
        contamination=0.1,
        random_state=42
    )

    # Train
    model.fit(X)

    # Predict (same format → no warning)
    df["ml_threat"] = model.predict(X)
    df["ml_threat"] = df["ml_threat"].apply(lambda x: 1 if x == -1 else 0)

    df["anomaly_score"] = model.decision_function(X)

    return df