# agent.py
from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

from tools import log_food, log_water, log_sleep, log_activity, get_summary
from router import router, food_info

# -------------------------------
# LLM SETUP
# -------------------------------

llm = ChatOllama(
    model="qwen3:8b",
    validate_model_on_init=True,
    temperature=0.4,
    num_predict=512,
    top_p=0.9
)

tools = [log_food, log_water, log_sleep, log_activity, get_summary]
llm_with_tools = llm.bind_tools(tools)

sys_msg = SystemMessage(
    content=(
        "You are a helpful lifestyle-tracking assistant. "
        "You help the user log meals, water intake, sleep, and physical activity. "
        "You can also show their summary of logs. "
        "Never give medical or health advice. "
        "Your job is ONLY to help them track their habits and stay organized."
    )
)

# -------------------------------
# ASSISTANT NODE
# -------------------------------

def assistant(state: MessagesState):
    last_msg = state["messages"][-1].content.lower()
    if "summary" in last_msg:
        return {"messages": [get_summary()]}
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# -------------------------------
# GRAPH
# -------------------------------

builder = StateGraph(MessagesState)

builder.add_node("router", router)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_node("food_info", food_info)

# START → router
builder.add_edge(START, "router")

# Conditional routing from router
builder.add_conditional_edges(
    "router",
    lambda out: out["next"],
    {
        "assistant": "assistant",
        "food_info": "food_info"
    }
)

# assistant → tools (if tool called)
builder.add_conditional_edges("assistant", tools_condition)

# tools → assistant
builder.add_edge("tools", "assistant")

graph = builder.compile()

