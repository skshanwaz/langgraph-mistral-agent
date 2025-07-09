###  LangGraph Mistral Agent with Web UI

This project demonstrates a modular AI agent using **LangGraph** and **Ollama's `mistral` model**. The agent processes user input and either solves math expressions, summarizes text, or provides a fallback response. A **Gradio UI** is provided for a simple web interface.

---

## 📁 Files Overview

| File         | Purpose                                      |
|--------------|----------------------------------------------|
| `core_logic.py` | Main logic for routing and LLM processing   |
| `ui_app.py`     | Web interface using Gradio                 |

---

## 📘 `core_logic.py` - Code Explanation

```python
from langgraph.graph import StateGraph
from langchain_community.llms import Ollama
from typing import TypedDict
StateGraph: Main component to define the agent's logic flow.

Ollama: Interface to connect to local LLMs (like mistral).

TypedDict: Used to define a structured "state" for each graph node.

1. Define the Agent State
python
Copy
Edit
class AgentState(TypedDict):
    input_text: str
    result: str
This defines what each step of the LangGraph will receive and return:

input_text: The user's original input.

result: The processed result (math/summarization/fallback).

2. Load the Mistral Model
python
Copy
Edit
llm = Ollama(model="mistral")
Connects to the mistral model served by Ollama.

Make sure mistral is pulled and running:
ollama run mistral

3. Router Node
python
Copy
Edit
def router_node(state: AgentState) -> dict:
    prompt = state["input_text"].lower()
    if "summarize" in prompt:
        return {"next": "summarizer"}
    elif any(op in prompt for op in ["+", "-", "*", "/"]):
        return {"next": "math"}
    else:
        return {"next": "fallback"}
This node decides where to send the input:

If it includes "summarize" → send to summarizer.

If it includes math symbols → send to math node.

Otherwise → fallback node.

4. Math Node
python
Copy
Edit
def math_node(state: AgentState) -> AgentState:
    expr = state["input_text"]
    response = llm.invoke(f"Solve this: {expr}")
    return {"input_text": expr, "result": response}
Sends math expression to the model using the prompt "Solve this: ...".

5. Summarizer Node
python
Copy
Edit
def summarizer_node(state: AgentState) -> AgentState:
    text = state["input_text"].replace("summarize:", "").strip()
    response = llm.invoke(f"Summarize this: {text}")
    return {"input_text": state["input_text"], "result": response}
Removes the "summarize:" prefix.

Asks the model to summarize the remaining text.

6. Fallback Node
python
Copy
Edit
def fallback_node(state: AgentState) -> AgentState:
    response = llm.invoke(f"Cannot identify action for: {state['input_text']}")
    return {"input_text": state["input_text"], "result": response}
Catches unrecognized input and replies generically.

7. Printer Node
python
Copy
Edit
def printer_node(state: AgentState) -> AgentState:
    print("Output:", state["result"])
    return state
Simply prints the output in the terminal.

8. Create LangGraph
python
Copy
Edit
graph = StateGraph(AgentState)

graph.add_node("router", router_node)
graph.add_node("math", math_node)
graph.add_node("summarizer", summarizer_node)
graph.add_node("fallback", fallback_node)
graph.add_node("printer", printer_node)
Adds all nodes to the graph with unique names.

9. Define Flow Control
python
Copy
Edit
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
Starts the flow at router.

Routes to the next node based on the router's output.

All end nodes pass through printer.

10. Run in CLI Loop
python
Copy
Edit
app = graph.compile()

if __name__ == "__main__":
    while True:
        user_input = input("\nEnter your request/query (or type 'exit' to quit): ")
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Exiting...")
            break
        app.invoke({"input_text": user_input})
Launches an infinite loop that reads from the terminal.

Exits on exit or quit.

🌐 ui_app.py - Web UI Code Explanation
python
Copy
Edit
import gradio as gr
from core_logic import app
Gradio creates a simple web interface.

Imports the compiled LangGraph app from core_logic.

Handle User Input
python
Copy
Edit
def handle_user_input(user_input):
    result = app.invoke({"input_text": user_input})
    return result["result"]
This function will be triggered when the user submits text in the UI.

It runs the agent and returns the result string.

Build the Gradio Interface
python
Copy
Edit
ui = gr.Interface(
    fn=handle_user_input,
    inputs=gr.Textbox(lines=3, placeholder="Enter math or 'summarize: ...'"),
    outputs=gr.Textbox(label="Result"),
    title="LangGraph AI Agent",
    description="AI router using LangGraph and Mistral Via Ollama for math & summarization."
)
fn: The function to call when input is submitted.

inputs: A textbox for user input.

outputs: A textbox for showing model output.

title and description: UI header content.

Launch the Web App
python
Copy
Edit
if __name__ == "__main__":
    ui.launch()
Starts the Gradio server (usually on http://localhost:7860).

✅ Run Instructions
1. Install Requirements
bash
Copy
Edit
pip install langgraph langchain-community gradio
2. Make Sure Ollama Is Running
bash
Copy
Edit
ollama run mistral
3. Run Web UI
bash
Copy
Edit
python ui_app.py
4. Or Run Terminal CLI Version
bash
Copy
Edit
python core_logic.py
🧪 Example Inputs
Input	Action
5 + 3 * 2	Math Solver
Summarize: AI is changing the world.	Text Summarization
Tell me a joke	Fallback

