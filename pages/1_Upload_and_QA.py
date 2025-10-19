# pages/1_Upload_and_QA.py
import streamlit as st
from utils import (
    store_extracted_data,
    fetch_all_documents_from_db,
    format_context_for_llm,
    ask_gemini
)
from file_processing import extract_text, extract_text_from_youtube

st.set_page_config(page_title="Upload & Q&A", page_icon="📄")
st.title("📄 Upload, Extract, and Ask Questions")

# --- Logic ---
if 'new_documents' not in st.session_state:
    st.session_state.new_documents = []

# --- YouTube Section ---
with st.expander("🔗 Add from YouTube"):
    youtube_url = st.text_input("Enter a YouTube URL:")
    if st.button("Process YouTube Video"):
        if youtube_url:
            with st.spinner("Processing YouTube video..."):
                text = extract_text_from_youtube(youtube_url)
                if text:
                    video_id = youtube_url.split('v=')[-1].split('&')[0]
                    file_name = f"youtube_{video_id}.txt"
                    store_extracted_data(file_name, "YouTube Video", text)
                    st.session_state.new_documents.append({"file_name": file_name, "file_type": "YouTube Video", "text": text})
                    st.success("✅ YouTube video processed!")
                    st.rerun()

# --- File Upload Section ---
with st.expander("📁 Add from File Upload", expanded=True):
    uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)
    if st.button("Process Uploaded Files"):
        if uploaded_files:
            with st.spinner("Processing files..."):
                for uploaded_file in uploaded_files:
                    text = extract_text(uploaded_file)
                    if text:
                        store_extracted_data(uploaded_file.name, uploaded_file.type, text)
                        st.session_state.new_documents.append({"file_name": uploaded_file.name, "file_type": uploaded_file.type, "text": text})
            st.success("✅ Files processed!")
            st.rerun()

# --- Q&A Section ---
st.markdown("---")
st.header("❓ Ask a Question")

# Fetch all docs from DB once
db_rows = fetch_all_documents_from_db()
db_documents = [{"file_name": row[1], "file_type": row[2], "text": row[3]} for row in db_rows]

all_documents = db_documents + st.session_state.new_documents

if all_documents:
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
    st.warning("Your knowledge base is empty. Please add files or a YouTube URL to begin.")