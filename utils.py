# utils.py
import streamlit as st
import sqlite3
from datetime import datetime
import google.generativeai as genai
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
import tempfile
import os

# --- Database Functions ---
@st.cache_resource
def init_db():
    conn = sqlite3.connect("extracted_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS extracted_text (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            file_type TEXT,
            extracted_text TEXT,
            upload_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_extracted_data(file_name, file_type, extracted_text):
    conn = sqlite3.connect("extracted_data.db")
    cursor = conn.cursor()
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO extracted_text (file_name, file_type, extracted_text, upload_time)
        VALUES (?, ?, ?, ?)
    ''', (file_name, file_type, extracted_text, upload_time))
    conn.commit()
    conn.close()

def fetch_all_documents_from_db():
    conn = sqlite3.connect("extracted_data.db")
    cursor = conn.cursor()
    cursor.execute('SELECT id, file_name, file_type, extracted_text, upload_time FROM extracted_text')
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_row_from_db(row_id):
    conn = sqlite3.connect("extracted_data.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM extracted_text WHERE id = ?', (row_id,))
    conn.commit()
    conn.close()

# --- AI and Transcription Helpers ---
@st.cache_data
def ask_gemini(context, question):
    # For security, use st.secrets for your API key in a real app
   # genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY environment variable not set. The app cannot contact the AI.")
        return "Error: API key not configured."
    genai.configure(api_key=api_key)
    #genai.configure(api_key="GEMINI_API_KEY") # Replace with your key
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = (
        "Answer the user's question based *only* on the provided context below...\n\n"
        "--- CONTEXT ---\n{context}\n--- QUESTION ---\n{question}"
    )
    try:
        response = model.generate_content(prompt.format(context=context, question=question))
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

def format_context_for_llm(documents):
    formatted_context = ""
    for doc in documents:
        formatted_context += f"DOCUMENT START\nFILE_NAME: {doc['file_name']}\nFILE_TYPE: {doc['file_type']}\nCONTENT:\n{doc['text']}\nDOCUMENT END\n\n"
    return formatted_context

def transcribe_large_audio(wav_file_path):
    st.info("Splitting audio into chunks for transcription...")
    recognizer = sr.Recognizer()
    sound = AudioSegment.from_wav(wav_file_path)

    chunk_length_ms = 45 * 1000
    chunks = make_chunks(sound, chunk_length_ms)
    full_text = ""

    if not chunks:
        st.error("Failed to create audio chunks.")
        return ""

    progress_bar = st.progress(0, text="Transcribing chunks...")
    total_chunks = len(chunks)

    with tempfile.TemporaryDirectory() as temp_dir:
        for i, audio_chunk in enumerate(chunks, start=1):
            progress_bar.progress(i / total_chunks, text=f"Transcribing chunk {i}/{total_chunks}...")
            if len(audio_chunk) < 500: continue
            
            chunk_filename = os.path.join(temp_dir, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            
            try:
                with sr.AudioFile(chunk_filename) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data)
                    full_text += text + " "
            except sr.UnknownValueError:
                st.write(f"🔹 Chunk {i} was silent.")
            except sr.RequestError as e:
                st.error(f"API request failed for chunk {i}: {e}")
                break
    
    progress_bar.empty()
    st.success("✅ Transcription complete!")
    return full_text if full_text.strip() else "Could not transcribe audio."