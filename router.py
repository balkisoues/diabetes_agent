from langgraph.graph import MessagesState

def router(state: MessagesState):
    """Routes messages to either assistant or food_info node."""
    text = state["messages"][-1].content.lower()

    if "what is" in text or "tell me about" in text or "is this" in text:
        return {"next": "food_info"}

    return {"next": "assistant"}


