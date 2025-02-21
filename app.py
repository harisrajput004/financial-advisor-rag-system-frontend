# streamlit_app.py
import streamlit as st
import requests
import json
from typing import List
import os

# API endpoint configuration
API_BASE_URL = "https://fa-rag-backend.devcustomprojects.com"

st.set_page_config(
    page_title="RAG System Interface",
    page_icon="🤖",
    layout="wide"
)

def query_rag_system(question: str) -> dict:
    """Send a query to the RAG system API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={"question": question}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error querying RAG system: {str(e)}")
        return None

def initialize_system(chapter_files: List[str]) -> bool:
    """Initialize the RAG system with provided chapter files."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/initialize",
            json=chapter_files
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error initializing RAG system: {str(e)}")
        return False

# Streamlit UI
st.title("📚 RAG System Interface")

# Sidebar for system initialization
with st.sidebar:
    st.header("System Configuration")
    
    # File uploader for chapter files
    uploaded_files = st.file_uploader(
        "Upload Chapter Files (JSON)",
        type=['json'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("Initialize System"):
            chapter_files = [file.name for file in uploaded_files]
            
            # Save uploaded files temporarily
            for file in uploaded_files:
                with open(file.name, 'wb') as f:
                    f.write(file.getvalue())
            
            # Initialize system
            if initialize_system(chapter_files):
                st.success("System initialized successfully!")
            
            # Clean up temporary files
            for file in uploaded_files:
                os.remove(file.name)

# Main query interface
st.header("Query System")

# Query input
query = st.text_area("Enter your question:", height=100)

if st.button("Submit Query"):
    if query:
        with st.spinner("Processing query..."):
            result = query_rag_system(query)
            
            if result:
                # Display answer
                st.subheader("Answer")
                st.write(result["answer"])
                
                # Display sources
                st.subheader("Sources")
                for idx, source in enumerate(result["sources"], 1):
                    with st.expander(f"Source {idx}"):
                        st.write(f"**Chapter:** {source['metadata']['chapter']}")
                        st.write(f"**Section:** {source['metadata']['section']}")
                        st.write(f"**Content Preview:**")
                        st.write(source['content'])
    else:
        st.warning("Please enter a question.")

# Add some helpful information
st.sidebar.markdown("""
---
### How to Use
1. Upload your chapter files (JSON format) using the sidebar
2. Initialize the system
3. Enter your question in the main panel
4. Click Submit Query to get answers

### Note
Make sure the API server is running at {}
""".format(API_BASE_URL))