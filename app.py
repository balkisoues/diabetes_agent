import streamlit as st
import json
from pathlib import Path
from tools import log_food, log_water, log_sleep, log_activity, get_summary

# -----------------------------
# Setup: Persistent storage
# -----------------------------
LOG_FILE = Path("logs.json")

if LOG_FILE.exists():
    with open(LOG_FILE, "r") as f:
        LOGS = json.load(f)
else:
    LOGS = {"food": [], "water": [], "sleep": [], "activity": []}

# Helper to save logs
def save_logs():
    with open(LOG_FILE, "w") as f:
        json.dump(LOGS, f, indent=2)

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Diabetes Lifestyle Tracker")

action = st.selectbox(
    "What would you like to do?",
    ["Log Food", "Log Water", "Log Sleep", "Log Activity", "Show Summary"]
)

if action == "Log Food":
    food = st.text_input("Enter the food item")
    if st.button("Submit Food"):
        LOGS["food"].append(food)
        save_logs()
        st.success(f"Logged meal: {food}")

elif action == "Log Water":
    water = st.text_input("Enter water amount (e.g., 2 cups)")
    if st.button("Submit Water"):
        LOGS["water"].append(water)
        save_logs()
        st.success(f"Logged water: {water}")

elif action == "Log Sleep":
    hours = st.number_input("Hours slept", min_value=0, max_value=24)
    if st.button("Submit Sleep"):
        LOGS["sleep"].append(hours)
        save_logs()
        st.success(f"Logged sleep: {hours} hours")

elif action == "Log Activity":
    activity = st.text_input("Enter activity (e.g., running, walking)")
    if st.button("Submit Activity"):
        LOGS["activity"].append(activity)
        save_logs()
        st.success(f"Logged activity: {activity}")

elif action == "Show Summary":
    summary = "Here is your activity summary:\n"
    summary += "\nFood:\n" + ("\n".join("- " + f for f in LOGS["food"]) if LOGS["food"] else "No food logged yet.")
    summary += "\n\nWater:\n" + ("\n".join("- " + w for w in LOGS["water"]) if LOGS["water"] else "No water logged yet.")
    summary += "\n\nSleep:\n" + ("\n".join("- " + str(s) + " hours" for s in LOGS["sleep"]) if LOGS["sleep"] else "No sleep logged yet.")
    summary += "\n\nActivity:\n" + ("\n".join("- " + a for a in LOGS["activity"]) if LOGS["activity"] else "No activity logged yet.")

    st.text(summary)

