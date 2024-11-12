import streamlit as st
import librosa
import soundfile as sf
import numpy as np
import tempfile
import os
from pydub import AudioSegment

# Function to calculate similarity
def calculate_similarity(original_file_path, cloned_file_path):
    original_audio, _ = librosa.load(original_file_path)
    cloned_audio, _ = librosa.load(cloned_file_path)
    correlation = np.corrcoef(original_audio, cloned_audio)[0, 1]
    similarity = correlation * 100
    return similarity

# Function to clone audio
def clone_audio(input_file_path):
    with tempfile.TemporaryDirectory() as tmp_dir:
        audio, sr = librosa.load(input_file_path)
        audio *= 32767 / np.max(np.abs(audio))  # Normalize audio
        audio = audio.astype(np.int16)
        output_file_path = os.path.join(tmp_dir, 'cloned_output.wav')
        sf.write(output_file_path, audio, sr)
        
        # Retry mechanism to ensure the file is created
        for attempt in range(5):
            if os.path.exists(output_file_path):
                return output_file_path
            else:
                time.sleep(1)  # Wait a second before retrying
        
        raise FileNotFoundError(f"Cloned audio file not found after retries: {output_file_path}")

# Function to convert audio format
def convert_audio(input_file):
    with tempfile.NamedTemporaryFile(suffix='.mp3') as tmp_file:
        tmp_file.write(input_file.getbuffer())
        audio = AudioSegment.from_mp3(tmp_file.name)
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_wav:
            audio.export(tmp_wav.name, format="wav")
            return tmp_wav.name

# Streamlit application
st.title("Audio Cloner")

# File uploader
input_file = st.file_uploader("Upload Audio File", type=['wav', 'mp3', 'ogg'])

if input_file:
    try:
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

        # Display download button
        with open(cloned_file_path, 'rb') as file:
            st.download_button("Download Cloned Audio", data=file, file_name='cloned_audio.wav')

    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
