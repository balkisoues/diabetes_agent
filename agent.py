from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage

from tools import tools
from router import router
from config import llm_with_tools, sys_msg
from langchain_ollama import ChatOllama


def food_info(state: MessagesState):
    """Provide general nutritional information."""
    query = state["messages"][-1]

    llm_food = ChatOllama(model="qwen3:8b", temperature=0.3)
    system = SystemMessage(
        content="Provide general nutritional information about foods (carbs, protein, fats). Never give medical or health advice."
    )

    response = llm_food.invoke([system, query])
    return {"messages": [response]}


def assistant(state: MessagesState):
    """Main assistant node."""
    response = llm_with_tools.invoke([sys_msg] + state["messages"])
    return {"messages": [response]}


# ---------------------------
# Build graph
# ---------------------------

builder = StateGraph(MessagesState)

builder.add_node("router", router)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_node("food_info", food_info)

builder.add_edge(START, "router")
builder.add_conditional_edges(
    "router",
    lambda out: out["next"],
    {
        "assistant": "assistant",
        "food_info": "food_info"
    }
)


builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

graph = builder.compile()

