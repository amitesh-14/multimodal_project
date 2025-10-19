# file_processing.py
import streamlit as st
import os
import tempfile
import pytesseract
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pandas as pd
from moviepy import VideoFileClip, AudioFileClip
from pydub import AudioSegment
import yt_dlp
from utils import transcribe_large_audio

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@st.cache_data
def extract_text(uploaded_file):
    # ... (code is the same, this is the main dispatcher) ...
    file_name = uploaded_file.name
    
    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif file_name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    elif file_name.endswith((".png", ".jpg", ".jpeg")):
        return extract_text_from_image(uploaded_file)
    elif file_name.endswith((".mp3", ".wav", ".flac", ".m4a")):
        return extract_text_from_audio(uploaded_file)
    elif file_name.endswith((".mp4", ".mov", ".avi", ".mkv")):
        return extract_text_from_video(uploaded_file)
    elif file_name.endswith((".xls", ".xlsx")):
        return extract_text_from_excel(uploaded_file)
    else:
        st.warning(f"Unsupported file type: {file_name}")
        return ""

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text: text += page_text + "\n"
    return text

def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_image(uploaded_file):
    image = Image.open(uploaded_file)
    return pytesseract.image_to_string(image)

def extract_text_from_excel(uploaded_file):
    try:
        xls = pd.ExcelFile(uploaded_file)
        full_text = ""
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            if not df.empty:
                full_text += f"--- Excel Sheet: {sheet_name} ---\n\n{df.to_string(index=False)}\n\n"
        return full_text
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return ""

def extract_text_from_audio(uploaded_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            temp_audio_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_audio_path, "wb") as f: f.write(uploaded_file.getbuffer())
            
            converted_wav_path = os.path.join(temp_dir, "converted.wav")
            sound = AudioSegment.from_file(temp_audio_path)
            sound.export(converted_wav_path, format="wav")
            
            return transcribe_large_audio(converted_wav_path)
        except Exception as e:
            st.error(f"Error during audio processing: {e}")
            return ""

def extract_text_from_video(uploaded_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            temp_video_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_video_path, "wb") as f: f.write(uploaded_file.getbuffer())
            
            converted_wav_path = os.path.join(temp_dir, "video_audio.wav")
            video_clip = VideoFileClip(temp_video_path)
            video_clip.audio.write_audiofile(converted_wav_path)
            video_clip.close()
            
            return transcribe_large_audio(converted_wav_path)
        except Exception as e:
            st.error(f"Error during video processing: {e}")
            return ""

@st.cache_data
def extract_text_from_youtube(youtube_url):
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            ydl_opts = {'format': 'bestaudio[ext=m4a]/bestaudio/best', 'outtmpl': os.path.join(temp_dir, 'download.%(ext)s'), 'noplaylist': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                downloaded_path = ydl.prepare_filename(info)
            
            if not downloaded_path or os.path.getsize(downloaded_path) == 0:
                st.error("Failed to download valid audio."); return ""
            
            converted_wav_path = os.path.join(temp_dir, "converted.wav")
            audio_clip = AudioFileClip(downloaded_path)
            audio_clip.write_audiofile(converted_wav_path)
            audio_clip.close()
            
            return transcribe_large_audio(converted_wav_path)
        except Exception as e:
            st.error(f"Error during YouTube processing: {e}")
            return ""