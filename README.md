# 🧠 Multimodal Q&A Assistant

This is a multi-page Streamlit application that allows you to build a persistent knowledge base by uploading various media types or adding YouTube links. You can then ask questions about the ingested content using Google's Gemini AI.

![Streamlit App Screenshot](https://i.imgur.com/example.png) ---

## ✨ Features

* **Multi-Page Interface:** A clean, navigable UI with separate pages for uploading content and viewing your database.
* **Persistent Storage:** Uses **SQLite** to store all extracted text, creating a long-term knowledge base.
* **Multimodal File Support:** Extract text and data from:
    * PDFs (`.pdf`)
    * Word Documents (`.docx`)
    * Excel Files (`.xls`, `.xlsx`)
    * Images (OCR) (`.png`, `.jpg`, `.jpeg`)
    * Audio Files (`.mp3`, `.wav`, `.m4a`)
    * Video Files (`.mp4`, `.mov`, `.avi`)
* **YouTube Integration:** Automatically downloads and transcribes audio from any YouTube URL.
* **AI-Powered Q&A:** Uses **Google's Gemini** model to answer questions based *only* on the context you've provided.
* **Robust Audio Transcription:** Handles long audio files by intelligently chunking the audio to fit API limits.
* **Data Management:** A "View Data" page to see, preview, and delete individual entries from your knowledge base.

---

## 💻 Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **AI Model:** Google Gemini (`gemini-2.5-flash`)
* **Database:** SQLite 3
* **Audio/Video Processing:** `yt-dlp`, `moviepy`, `pydub`
* **Text Extraction (OCR):** `pytesseract`
* **Audio Transcription:** `SpeechRecognition` (Google Web Speech API)
* **File Handling:** `PyPDF2`, `python-docx`, `pandas`, `Pillow`

---

## 🚀 Setup and Installation

Follow these steps precisely to get the application running on your local machine.

### **Prerequisites (Crucial!)**

This application relies on two external command-line tools that **must be installed on your system** and added to your system's PATH.

1.  **Tesseract-OCR:** Required for extracting text from images.
    * **Install:** Download and install from the [official Windows installer](https://github.com/UB-Mannheim/tesseract/wiki).
    * **Set Path:**
        * After installation (e.g., to `C:\Program Files\Tesseract-OCR`), you must add this folder to your system's **Environment Variables PATH**. 
        * You must also update the path in `file_processing.py` to point to your `tesseract.exe`:
            ```python
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            ```

2.  **FFmpeg:** Required by `pydub` and `moviepy` for processing all audio and video files (MP3, MP4, etc.).
    * **Install:** Download the latest "essentials" build from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
    * **Set Path:**
        * Create a folder like `C:\ffmpeg` and extract the contents there.
        * Add the `bin` folder (e.g., `C:\ffmpeg\bin`) to your system's **Environment Variables PATH**.
    * **Verify:** Open a new command prompt and type `ffmpeg -version`. You should see the version information, not an error.

---

### **Installation Steps**

**1. Clone the Repository**
```bash
git clone [https://github.com/your-username/multimodal-project.git](https://github.com/your-username/multimodal-project.git)
cd multimodal-project
```bash
2. Create and Activate a Virtual Environment It's highly recommended to use a virtual environment.

Bash

# Create the environment
python -m venv vir

# Activate it (on Windows)
.\vir\Scripts\activate
3. Install Python Packages Create a requirements.txt file with the contents below, then run pip install -r requirements.txt.

<details> <summary>Click to see <strong>requirements.txt</strong></summary>

Plaintext

streamlit
google-generativeai
pytesseract
PyPDF2
python-docx
Pillow
SpeechRecognition
pydub
pandas
openpyxl
xlrd
moviepy
yt-dlp
</details>

Bash

# Install all packages
pip install -r requirements.txt
4. Set Up Your API Key This project uses Streamlit's built-in secrets management.

Create a folder named .streamlit in the main project directory.

Inside that folder, create a file named secrets.toml.

Add your Google Gemini API key to this file:

Ini, TOML

# .streamlit/secrets.toml
GEMINI_API_KEY = "your_actual_key_here"
5. Update Your .gitignore Create a .gitignore file in your main project folder to protect your secrets and avoid uploading unnecessary files.

Plaintext

# .gitignore

# Virtual Environment
vir/

# Python cache
__pycache__/

# Streamlit secrets
.streamlit/secrets.toml

# Database
extracted_data.db
🏃‍♀️ How to Run the App
With your virtual environment activated, run the following command in your terminal:

Bash

streamlit run app.py
Streamlit will open the application in your default web browser.

Usage
Main Page (app.py): This is the landing page. Use the sidebar to navigate.

Upload and Q&A:

Add from YouTube: Paste a YouTube URL and click "Process" to transcribe the audio and add it to the database.

Add from File Upload: Upload one or more supported files. Click "Process" to extract their content and save it to the database.

Ask a Question: Once you have documents in your knowledge base (visible in the sidebar), type a question and get an AI-generated answer based only on that content.

View Data:

See a list of all documents in your database.

Preview the first 100 characters of extracted text.

Expand any entry to view the full text.

Click the "Delete" button to permanently remove any entry from the knowledge base.