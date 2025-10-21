# Start from a slim, modern Python base image
FROM python:3.11-slim

# Set a working directory inside the container
WORKDIR /app

# Install the system dependencies (FFmpeg and Tesseract)
# This is the key step that Streamlit Community Cloud's packages.txt also does
RUN apt-get update && apt-get install -y \
    ffmpeg \
    tesseract-ocr \
    build-essential \
    libjpeg-dev \
    && apt-get clean

# Copy your requirements file first to leverage Docker cache
COPY requirements.txt .

# Install your Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 8501

# The command to run your app
# We use 0.0.0.0 so it's accessible from outside the container
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]