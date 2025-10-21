# app.py
import streamlit as st
from utils import init_db

# Set the page configuration for the entire app
st.set_page_config(
    page_title="Multimodal Q&A Assistant",
    page_icon="🧠",
    layout="wide"
)

# --- Main Page Content ---
st.title("Welcome to the Multimodal Q&A Assistant! 🧠")

st.markdown("""
This application allows you to build a knowledge base from various sources and ask questions about it.

**Navigate using the sidebar on the left to:**
1.  **Upload :** Add new files (PDFs, documents, audio, video) or YouTube links to the knowledge base.
2. **Ask Questions:** Query the knowledge base using natural language questions.            
3.  **View Data:** See all the documents currently stored in your knowledge base and manage them.

Select a page from the sidebar to get started!
""")

# Initialize the database when the app starts
if __name__ == "__main__":
    init_db()