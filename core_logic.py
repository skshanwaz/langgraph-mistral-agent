from langgraph.graph import StateGraph
#from langchain_ollama import OllamaLLM
from langchain_community.llms import Ollama

#from langchain_community.llms import OllamaLLM
from typing import TypedDict

# 1. Define state class with plain str (no operator.or_)
class AgentState(TypedDict):
    input_text: str
    result: str

# 2. Load model
llm = Ollama(model="mistral")

# 3. Router logic
def router_node(state: AgentState) -> dict:
    prompt = state["input_text"].lower()
    if "summarize" in prompt:
        return {"next": "summarizer"}
    elif any(op in prompt for op in ["+", "-", "*", "/"]):
        return {"next": "math"}
    else:
        return {"next": "fallback"}

# 4. Math Node
def math_node(state: AgentState) -> AgentState:
    expr = state["input_text"]
    response = llm.invoke(f"Solve this: {expr}")
    return {"input_text": expr, "result": response}

# 5. Summary Node
def summarizer_node(state: AgentState) -> AgentState:
    text = state["input_text"].replace("summarize:", "").strip()
    response = llm.invoke(f"Summarize this: {text}")
    return {"input_text": state["input_text"], "result": response}

# 6. Fallback Node
def fallback_node(state: AgentState) -> AgentState:
    response = llm.invoke(f"Cannot identify action for: {state['input_text']}")
    return {"input_text": state["input_text"], "result": response}

#7. Printer Node
def printer_node(state: AgentState) -> AgentState:
    print("Output:", state["result"])
    return state

# 8. Build the LangGraph
graph = StateGraph(AgentState)

graph.add_node("router", router_node)
graph.add_node("math", math_node)
graph.add_node("summarizer", summarizer_node)
graph.add_node("fallback", fallback_node)
graph.add_node("printer", printer_node)

graph.set_entry_point("router")

graph.add_conditional_edges(
    "router",
    lambda x: x["next"],
    {
        "math": "math",
        "summarizer": "summarizer",
        "fallback": "fallback"
    }
)

graph.add_edge("math", "printer")
graph.add_edge("summarizer", "printer")
graph.add_edge("fallback", "printer")

app = graph.compile()

#9. Test runs# Dynamic Input Loop
if __name__ == "__main__":
    while True:
        user_input = input("\nEnter your request/query  (or type 'exit' to quit): ")
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Exiting...")
            break
        app.invoke({"input_text": user_input})

