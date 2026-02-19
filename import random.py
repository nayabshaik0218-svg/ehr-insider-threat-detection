import random
import pandas as pd
from datetime import datetime, timedelta

# ----------------------------
# CONFIG
# ----------------------------
random.seed(42)

NUM_NORMAL_LOGS = 900
NUM_ATTACK_LOGS = 100

users = [
    {"user_id": "U101", "role": "doctor", "department": "cardiology"},
    {"user_id": "U102", "role": "doctor", "department": "neurology"},
    {"user_id": "U201", "role": "nurse", "department": "cardiology"},
    {"user_id": "U202", "role": "nurse", "department": "orthopedics"},
    {"user_id": "U301", "role": "admin", "department": "admin"},
]

departments = ["cardiology", "neurology", "orthopedics", "admin"]
devices = ["desktop", "mobile"]
locations = ["ward", "ICU", "office", "home"]

patient_ids = [f"P{str(i).zfill(3)}" for i in range(1, 201)]  # 200 patients

# Role-based allowed actions (normal behavior)
role_actions = {
    "doctor": ["view", "update"],
    "nurse": ["view"],
    "admin": ["view", "export"]
}

# Normal working hours (mostly)
WORK_START = 8
WORK_END = 18

start_time = datetime(2026, 2, 1, 8, 0, 0)

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------
def random_timestamp_normal():
    """Generate timestamp mostly inside working hours"""
    day_offset = random.randint(0, 4)  # 5 days logs
    base = start_time + timedelta(days=day_offset)

    # 85% inside work hours, 15% outside
    if random.random() < 0.85:
        hour = random.randint(WORK_START, WORK_END)
    else:
        hour = random.choice(list(range(0, WORK_START)) + list(range(WORK_END + 1, 24)))

    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return base.replace(hour=hour, minute=minute, second=second)

def random_timestamp_attack():
    """Attack logs mostly at late night"""
    day_offset = random.randint(0, 4)
    base = start_time + timedelta(days=day_offset)
    hour = random.choice([22, 23, 0, 1, 2, 3])
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return base.replace(hour=hour, minute=minute, second=second)

def pick_patient_for_user(user):
    """Normal: user tends to access limited patients"""
    # Each user usually accesses only 20 patients frequently
    common_patients = random.sample(patient_ids, 20)
    return random.choice(common_patients)

def create_normal_log():
    user = random.choice(users)
    ts = random_timestamp_normal()

    action = random.choice(role_actions[user["role"]])

    # Usually same department
    department = user["department"]
    device = random.choice(devices)

    # Location normal based on role
    if user["role"] == "doctor":
        location = random.choice(["ward", "ICU"])
    elif user["role"] == "nurse":
        location = random.choice(["ward", "ICU"])
    else:
        location = "office"

    patient_id = pick_patient_for_user(user)

    return {
        "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user["user_id"],
        "role": user["role"],
        "patient_id": patient_id,
        "action": action,
        "department": department,
        "device": device,
        "location": location,
        "label": 0  # normal
    }

def create_attack_log():
    """
    Insider threat patterns:
    1) Access many new patients quickly
    2) Access different department patients
    3) Export at night (admin abuse)
    """
    user = random.choice(users)
    ts = random_timestamp_attack()

    # Attack behavior: suspicious actions
    if user["role"] == "admin":
        action = "export"  # admin exporting at night
        department = "admin"
    else:
        action = "view"
        # Access different department (unusual)
        department = random.choice([d for d in departments if d != user["department"]])

    device = random.choice(devices)
    location = random.choice(["home", "office"])  # suspicious remote

    # New/unseen patient
    patient_id = random.choice(patient_ids)

    return {
        "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user["user_id"],
        "role": user["role"],
        "patient_id": patient_id,
        "action": action,
        "department": department,
        "device": device,
        "location": location,
        "label": 1  # attack
    }

# ----------------------------
# GENERATE DATASET
# ----------------------------
logs = []
for _ in range(NUM_NORMAL_LOGS):
    logs.append(create_normal_log())

for _ in range(NUM_ATTACK_LOGS):
    logs.append(create_attack_log())

# Shuffle logs
random.shuffle(logs)

df = pd.DataFrame(logs)

# Save to CSV
df.to_csv("ehr_logs.csv", index=False)

print("✅ Dataset generated successfully!")
print("File saved as: ehr_logs.csv")
print(df.head(10))
