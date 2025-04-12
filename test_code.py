import streamlit as st
import os
import ast
from langchain_community.llms import Ollama

# Streamlit page config
st.set_page_config(page_title="Code Documentation Assistant", layout="wide")
st.title("📘 Code Documentation Assistant")

# Initialize Ollama with codellama
llm = Ollama(model="codellama:instruct")

# Function: Extract top-level functions using AST
def extract_functions(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    parsed = ast.parse(content)
    functions = []
    for node in parsed.body:
        if isinstance(node, ast.FunctionDef):
            code = ast.get_source_segment(content, node)
            functions.append({
                "name": node.name,
                "code": code
            })
    return functions

# Function: Generate friendly explanation using codellama
def explain_function(code):
    prompt = f"Explain this Python function to a beginner, in simple language:\n\n{code}"
    return llm.invoke(prompt).strip()

# Upload section
uploaded_file = st.file_uploader("📂 Upload a Python (.py) file", type=["py"])

if uploaded_file:
    st.success(f"✅ File uploaded: {uploaded_file.name}")

    # Save uploaded file
    os.makedirs("uploaded", exist_ok=True)
    file_path = os.path.join("uploaded", uploaded_file.name)
    with open(file_path, "w") as f:
        f.write(uploaded_file.getvalue().decode("utf-8"))
    st.session_state["uploaded_path"] = file_path

    # Extract and explain
    with st.spinner("🧠 Analyzing functions and generating explanations..."):
        functions = extract_functions(file_path)

        for func in functions:
            st.subheader(f"🧩 Function: `{func['name']}`")
            st.code(func["code"], language="python")

            explanation = explain_function(func["code"])
            st.markdown(f"**🧠 Friendly Explanation:**\n\n{explanation}")
