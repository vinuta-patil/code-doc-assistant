
# Code Documentation Assistant

A **Streamlit-based AI assistant** that reads your Python code, explains each function in beginner-friendly language, and automatically inserts professional **docstrings** — powered by a local **CodeLlama model via Ollama**.


## Features

- Upload any `.py` file
- Extracts all top-level functions using `ast`
- Generates **natural language explanations** (great for beginners)
- Creates **docstrings** using `codellama:instruct`
- Choose to:
  -  Overwrite original file (Option A)
  -  Save to new file with docstrings (Option B)
-  Built with **LangChain + Ollama + Streamlit**
-  100% local and private – no OpenAI needed


## 📦 Tech Stack

| Tool         | Purpose                          |
|--------------|----------------------------------|
| `Streamlit`  | Web UI                           |
| `Ollama`     | Local LLM engine                 |
| `CodeLlama`  | Code understanding + generation  |
| `LangChain`  | LLM pipeline and prompting       |
| `ast`, `astor` | Code parsing + rewriting        |


##  How to Run Locally

### 1. Clone this repo

```bash
git clone https://github.com/vinuta-patil/code-doc-assistant.git
cd code-doc-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit langchain langchain-community astor python-dotenv
```

### 4. Install and run Ollama + CodeLlama

```bash
# Install Ollama (if not installed)
curl -fsSL https://ollama.com/install.sh | sh

# Pull the model
ollama pull codellama:instruct
```


### 5. Run the app

```bash
streamlit run app.py
```


## 📁 Folder Structure

```
code-doc-assistant/
├── app.py               ← Streamlit frontend
├── doc_agent.py         ← Core logic (optional CLI use)
├── test_code.py         ← Sample test file
├── uploaded/            ← Uploaded files (ignored in Git)
├── .gitignore
└── README.md
```


## ✨ Future Ideas

- Before/After diff view
-  Download modified file button
-  Multi-user version with history
-  VS Code plugin integration

## Developed by [@vinuta-patil](https://github.com/vinuta-patil)


