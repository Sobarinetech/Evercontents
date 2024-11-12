import streamlit as st
import librosa
import soundfile as sf
import numpy as np
import tempfile
import os
from pydub import AudioSegment
import PyPDF2  # For PDF text extraction
from gtts import gTTS  # Google Text-to-Speech

# Function to calculate similarity
def calculate_similarity(original_file_path, cloned_file_path):
    original_audio, _ = librosa.load(original_file_path)
    cloned_audio, _ = librosa.load(cloned_file_path)
    correlation = np.corrcoef(original_audio, cloned_audio)[0, 1]
    similarity = correlation * 100
    return similarity

# Function to clone audio
def clone_audio(input_file_path):
    cloned_output_path = tempfile.NamedTemporaryFile(suffix='.wav', delete=False).name
    audio, sr = librosa.load(input_file_path)
    audio *= 32767 / np.max(np.abs(audio))  # Normalize audio
    audio = audio.astype(np.int16)
    sf.write(cloned_output_path, audio, sr)
    return cloned_output_path

# Function to convert audio format
def convert_audio(input_file):
    with tempfile.NamedTemporaryFile(suffix='.mp3') as tmp_file:
        tmp_file.write(input_file.getbuffer())
        audio = AudioSegment.from_mp3(tmp_file.name)
        converted_file_path = tempfile.NamedTemporaryFile(suffix='.wav', delete=False).name
        audio.export(converted_file_path, format="wav")
        return converted_file_path

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to convert text to speech (using gTTS for simplicity)
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    speech_file_path = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name
    tts.save(speech_file_path)
    return speech_file_path

# Streamlit application
st.title("Audio Cloner with PDF Reading")

# File upload for PDF and Audio
pdf_file = st.file_uploader("Upload PDF File", type=["pdf"])
input_file = st.file_uploader("Upload Audio File", type=['wav', 'mp3', 'ogg'])

if pdf_file and input_file:
    try:
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_file)

        # Convert uploaded audio to WAV format if needed
        if input_file.type == 'audio/mpeg':
            input_file_path = convert_audio(input_file)
        else:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                tmp_file.write(input_file.getbuffer())
                input_file_path = tmp_file.name

        # Clone audio
        cloned_file_path = clone_audio(input_file_path)

        # Calculate similarity
        similarity = calculate_similarity(input_file_path, cloned_file_path)

        # Display similarity
        st.write(f"Similarity: {similarity:.2f}%")

        # Generate speech from the PDF text
        st.write("Now reading the PDF text using the cloned voice:")

        # Convert the extracted text to speech (using Google TTS for now)
        speech_file_path = text_to_speech(text)

        # Display the speech download button
        with open(speech_file_path, 'rb') as file:
            st.download_button("Download Speech", data=file, file_name='pdf_reading.mp3')

        # Optionally, play the generated speech directly in the app
        st.audio(speech_file_path)

    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
    finally:
        # Cleanup temporary files
        if 'input_file_path' in locals() and os.path.exists(input_file_path):
            os.remove(input_file_path)
        if 'cloned_file_path' in locals() and os.path.exists(cloned_file_path):
            os.remove(cloned_file_path)
        if 'speech_file_path' in locals() and os.path.exists(speech_file_path):
            os.remove(speech_file_path)
