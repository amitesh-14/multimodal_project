# pages/1_Upload_Data.py
import streamlit as st
from utils import store_extracted_data
from file_processing import extract_text, extract_text_from_youtube

st.set_page_config(page_title="Upload Data", page_icon="📁")
st.title("📁 Upload New Knowledge")
st.info("Add new content to the knowledge base here. The data will be processed, stored, and made available for Q&A.")

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
                    st.success("✅ YouTube video processed and saved!")
                    # Clear cache for other pages to see the new data
                    st.cache_data.clear()

# --- File Upload Section ---
with st.expander("📁 Add from File Upload", expanded=True):
    uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)
    if st.button("Process Uploaded Files"):
        if uploaded_files:
            with st.spinner("Processing files..."):
                for uploaded_file in uploaded_files:
                    st.write(f"Processing: {uploaded_file.name}...")
                    text = extract_text(uploaded_file)
                    if text:
                        store_extracted_data(uploaded_file.name, uploaded_file.type, text)
            st.success("✅ All files processed and saved!")
            # Clear cache for other pages to see the new data
            st.cache_data.clear()