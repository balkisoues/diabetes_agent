# storage.py
import json

LOGS_FILE = "logs.json"

def save_logs(logs):
    with open(LOGS_FILE, "w") as f:
        json.dump(logs, f)

def load_logs():
    try:
        with open(LOGS_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"food": [], "water": [], "sleep": [], "activity": []}

