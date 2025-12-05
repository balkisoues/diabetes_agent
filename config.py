from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from tools import tools

llm = ChatOllama(
    model="qwen3:8b",
    validate_model_on_init=True,
    temperature=0.4,
    num_predict=512,
    top_p=0.9
)

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

