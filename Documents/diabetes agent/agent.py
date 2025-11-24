from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

# ------------------------------------
# STORAGE
# ------------------------------------

LOGS = {
    "food": [],
    "water": [],
    "sleep": [],
    "activity": []
}

# ------------------------------------
# TOOLS
# ------------------------------------

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

def food_info(state: MessagesState):
    """Provides general info about food."""
    query = state["messages"][-1].content

    llm_food = ChatOllama(
        model="qwen3:8b",
        temperature=0.3
    )

    system = SystemMessage(
        content=(
            "Provide **general nutritional information** about foods (carbs, protein, fats). "
            "Never give health or medical advice."
        )
    )

    response = llm_food.invoke([system, state["messages"][-1]])

    return {"messages": [response]}



def router(state: MessagesState):
    """Routes messages to assistant or food_info node."""
    text = state["messages"][-1].content.lower()
    next_node = "food_info" if "what is" in text or "tell me about" in text or "is this" in text else "assistant"
    return {"next_node": next_node, "messages": []}  # empty messages


@tool
def log_activity(activity: str) -> str:
    """Log physical activity or exercise."""
    LOGS["activity"].append(activity)
    return f"Logged activity: {activity}"


@tool
def get_summary() -> str:
    """Return a summary of all logged lifestyle data."""
    summary = "Here is your activity summary:\n"

    summary += "\nFood:\n" + ("\n".join("- " + f for f in LOGS["food"]) if LOGS["food"] else "No food logged yet.")
    summary += "\n\nWater:\n" + ("\n".join("- " + w for w in LOGS["water"]) if LOGS["water"] else "No water logged yet.")
    summary += "\n\nSleep:\n" + ("\n".join("- " + s + " hours" for s in LOGS["sleep"]) if LOGS["sleep"] else "No sleep logged yet.")
    summary += "\n\nActivity:\n" + ("\n".join("- " + a for a in LOGS["activity"]) if LOGS["activity"] else "No activity logged yet.")

    return summary


tools = [log_food, log_water, log_sleep, log_activity, get_summary]

# ------------------------------------
# LLM SETUP
# ------------------------------------

llm = ChatOllama(
    model="qwen3:8b",
    validate_model_on_init=True,
    temperature=0.4,
    num_predict=512,
    top_p=0.9
)

llm_with_tools = llm.bind_tools(tools)

sys_msg = SystemMessage(content=
    "You are a helpful lifestyle-tracking assistant. "
    "You help the user log meals, water intake, sleep, and physical activity. "
    "You can also show their summary of logs. "
    "Never give medical or health advice. "
    "Your job is ONLY to help them track their habits and stay organized."
)

# ------------------------------------
# ASSISTANT NODE
# ------------------------------------
def assistant(state: MessagesState):
    return {
        "messages": [
            llm_with_tools.invoke([sys_msg] + state["messages"])
        ]
    }

# ------------------------------------
# GRAPH
# ------------------------------------

builder = StateGraph(MessagesState)
builder.add_node("router", router)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_node("food_info", food_info)

# START → router
builder.add_edge(START, "router")

builder.add_conditional_edges("router", lambda result: result["next_node"])

# assistant → tools (if assistant calls a tool)
builder.add_conditional_edges("assistant", tools_condition)

# tools → assistant (return after tool runs)
builder.add_edge("tools", "assistant")

graph = builder.compile()

