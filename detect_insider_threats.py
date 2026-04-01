import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

def run_detection(file="ehr_logs.csv"):

    df = pd.read_csv(file)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek

    df["is_night_access"] = df["hour"].apply(
        lambda x: 1 if (x < 8 or x > 18) else 0
    )

    encoders = {}
    for col in ["user_id","role","patient_id","action","department","device","location"]:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    features = [
        "user_id","role","patient_id","action",
        "department","device","location",
        "hour","day_of_week","is_night_access"
    ]

    X = df[features]

    model = IsolationForest(
        n_estimators=200,
        contamination=0.1,
        random_state=42
    )

    model.fit(X)

    df["anomaly"] = model.predict(X)
    df["ml_threat"] = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)
    df["anomaly_score"] = model.decision_function(X)

    return df