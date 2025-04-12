import streamlit as st
import os
import ast
import astor
from langchain_community.llms import Ollama

# Streamlit page config
st.set_page_config(page_title="Code Documentation Assistant", layout="wide")
st.title("📘 Code Documentation Assistant")

# Initialize codellama model
llm = Ollama(model="codellama:instruct")

# Function: Extract top-level functions from Python file
def extract_functions(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
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

# Function: Generate beginner-friendly explanation
def explain_function(code):
    prompt = f"Explain this Python function to a beginner, in simple language:\n\n{code}"
    return llm.invoke(prompt).strip()

# Function: Generate docstring
def generate_docstring(code):
    prompt = f"Generate a Python docstring for the following function:\n\n{code}"
    return llm.invoke(prompt).strip()

# Function: Insert generated docstrings into the AST and save
def insert_docstrings(file_path, functions_with_docs, output_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            match = next((f for f in functions_with_docs if f["name"] == node.name), None)
            if match and not ast.get_docstring(node):
                doc_node = ast.Expr(value=ast.Str(s=match["doc"]))
                node.body.insert(0, doc_node)

    new_code = astor.to_source(tree)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_code)

# Upload section
uploaded_file = st.file_uploader("📂 Upload a Python (.py) file", type=["py"])

if uploaded_file:
    st.success(f"✅ File uploaded: {uploaded_file.name}")

    # Save uploaded file
    os.makedirs("uploaded", exist_ok=True)
    file_path = os.path.join("uploaded", uploaded_file.name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(uploaded_file.getvalue().decode("utf-8"))

    st.session_state["uploaded_path"] = file_path

    # Analyze functions
    with st.spinner("🧠 Analyzing functions and generating explanations..."):
        functions = extract_functions(file_path)

        documented_funcs = []

        for func in functions:
            st.subheader(f"🧩 Function: `{func['name']}`")
            st.code(func["code"], language="python")

            explanation = explain_function(func["code"])
            st.markdown(f"**🧠 Friendly Explanation:**\n\n{explanation}")

            docstring = generate_docstring(func["code"])
            documented_funcs.append({
                "name": func["name"],
                "doc": docstring
            })

        # Option selector
        st.markdown("### 🛠️ Choose how to apply docstrings:")
        option = st.radio("What do you want to do with the modified file?", 
                          ("Overwrite original file (Option A)", "Save as new file (Option B)"))

        if st.button("🧠 Insert Docstrings"):
            if option == "Overwrite original file (Option A)":
                insert_docstrings(file_path, documented_funcs, file_path)
                st.success("✅ Original file updated with docstrings.")
            else:
                new_path = file_path.replace(".py", "_documented.py")
                insert_docstrings(file_path, documented_funcs, new_path)
                st.success(f"✅ New file created: `{os.path.basename(new_path)}`")
