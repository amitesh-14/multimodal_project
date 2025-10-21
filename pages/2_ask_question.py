# pages/2_Ask_Questions.py
import streamlit as st
from utils import (
    fetch_all_documents_from_db,
    format_context_for_llm,
    ask_gemini
)

st.set_page_config(page_title="Ask Questions", page_icon="❓")
st.title("❓ Ask Questions")
st.info("Ask a question based on all the content you have uploaded to the knowledge base.")

# --- Q&A Section ---
st.markdown("---")

# Fetch all documents from the database
# This function is cached in utils.py, so it's fast
db_rows = fetch_all_documents_from_db()

if db_rows:
    all_documents = [{"file_name": row[1], "file_type": row[2], "text": row[3]} for row in db_rows]

    # Display available files in the sidebar
    with st.sidebar:
        st.subheader("Available Files in Context")
        displayed_files = set(doc['file_name'] for doc in all_documents)
        for file_name in displayed_files:
            st.info(f"📄 {file_name}")

    question = st.text_input("Ask a question about the content of your knowledge base:")
    if st.button("Get Answer"):
        if question:
            with st.spinner("🤔 Searching for the answer..."):
                full_context = format_context_for_llm(all_documents)
                answer = ask_gemini(full_context, question)
                st.subheader("💬 Answer:")
                st.write(answer)
        else:
            st.warning("Please enter a question.")
else:
    st.warning("Your knowledge base is empty. Please go to the 'Upload Data' page to add files.")