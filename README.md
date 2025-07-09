#LangGraph Mistral Agent

This project demonstrates an intelligent AI agent built using **LangGraph**, **Ollama (Mistral model)**, and **Gradio**. The agent dynamically routes user input to perform either **mathematical computation**, **text summarization**, or fallback response based on the input type.

---

## 🚀 Features

- ✅ Input router using custom logic
- ➕ Performs math operations (`+`, `-`, `*`, `/`)
- 📝 Summarizes text when prompted with `summarize: ...`
- ⚠️ Provides fallback responses when no specific action matches
- 🧪 Works in terminal and web UI using **Gradio**

---

## 📁 Project Structure

langgraph-mistral-agent/
│
├── core_logic.py # Main LangGraph agent logic
├── ui_app.py # Gradio UI wrapper
├── README.md # Project documentation
└── requirements.txt # Python dependencies

yaml
Copy
Edit

---

## 🛠️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/skshanwaz/langgraph-mistral-agent.git
cd langgraph-mistral-agent
Create and activate a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Ensure Ollama is installed and running with the Mistral model:

Install Ollama from: https://ollama.com/download

Then, in terminal:

bash
Copy
Edit
ollama run mistral
📦 Requirements
Here's a sample requirements.txt:

nginx
Copy
Edit
langgraph
langchain
langchain-community
gradio
(You may add ollama or other relevant packages if needed.)

💻 Usage
▶️ CLI Mode
Run the agent from the terminal:

bash
Copy
Edit
python core_logic.py
You will be prompted to enter math expressions or summarization prompts.

🌐 Web UI Mode
Run the Gradio app:

bash
Copy
Edit
python ui_app.py
Open your browser to the provided local address (typically http://127.0.0.1:7860/).

✍️ Examples
Math Input:

Copy
Edit
12 + 7 * 3
Summarization Input:

vbnet
Copy
Edit
summarize: LangGraph is a framework for building stateful AI agents.
Fallback Input:

csharp
Copy
Edit
What is the weather?
🧠 Behind the Scenes
router_node: Routes inputs to math, summarization, or fallback.

math_node: Uses the LLM to evaluate math expressions.

summarizer_node: Summarizes input text.

fallback_node: Handles unrecognized input.

printer_node: Displays result in CLI or UI.

🙋‍♂️ Author
Shaik Shanwaz
📧 shaikshanwaz75@gmail.com
🔗 LinkedIn
💻 GitHub

📜 License
This project is licensed under the MIT License. See LICENSE file for details.

yaml
Copy
Edit

---

Let me know if you'd like to include a GIF/screenshot of the UI or deployment options like `Streamlit`, 