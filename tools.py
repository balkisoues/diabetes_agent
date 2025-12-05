from langchain.tools import tool

LOGS = {
    "food": [],
    "water": [],
    "sleep": [],
    "activity": []
}

@tool
def log_food(item: str) -> str:
    """Log a meal or food item."""
    LOGS["food"].append(item)
    return f"Logged meal: {item}"

@tool
def log_water(amount: str) -> str:
    """Log water intake."""
    LOGS["water"].append(amount)
    return f"Logged water intake: {amount}"

@tool
def log_sleep(hours: str) -> str:
    """Log sleep duration in hours."""
    LOGS["sleep"].append(hours)
    return f"Logged sleep: {hours} hours"

@tool
def log_activity(activity: str) -> str:
    """Log physical activity."""
    LOGS["activity"].append(activity)
    return f"Logged activity: {activity}"

@tool
def get_summary() -> str:
    """Return a summary of logged lifestyle data."""
    summary = "Here is your activity summary:\n"

    summary += "\nFood:\n" + ("\n".join("- " + f for f in LOGS["food"]) if LOGS["food"] else "No food logged yet.")
    summary += "\n\nWater:\n" + ("\n".join("- " + w for w in LOGS["water"]) if LOGS["water"] else "No water logged yet.")
    summary += "\n\nSleep:\n" + ("\n".join("- " + s + " hours" for s in LOGS["sleep"]) if LOGS["sleep"] else "No sleep logged yet.")
    summary += "\n\nActivity:\n" + ("\n".join("- " + a for a in LOGS["activity"]) if LOGS["activity"] else "No activity logged yet.")

    return summary

tools = [log_food, log_water, log_sleep, log_activity, get_summary]

