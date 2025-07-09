# ui_app.py

import gradio as gr
from core_logic import app

def handle_user_input(user_input):
    result = app.invoke({"input_text": user_input})
    return result["result"]

ui = gr.Interface(
    fn=handle_user_input,
    inputs=gr.Textbox(lines=3, placeholder="Enter math or 'summarize: ...'"),
    outputs=gr.Textbox(label="Result"),
    title="LangGraph AI Agent",
    description="AI router using LangGraph and Mistral Via Ollama for math & summarization."
)

if __name__ == "__main__":
    ui.launch()
