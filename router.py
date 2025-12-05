# router.py
from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import MessagesState

def food_info(state: MessagesState):
    """Provides general nutritional info about a food item."""
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
    """Routes messages to either assistant or food_info node."""
    text = state["messages"][-1].content.lower()

    if any(kw in text for kw in ["what is", "tell me about", "is this"]):
        return {"next": "food_info"}
    return {"next": "assistant"}

