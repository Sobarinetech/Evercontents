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
        audio *= 32767 / np.max(np.abs(audio))
        audio = audio.astype(np.int16)
        output_file_path = os.path.join(tmp_dir, 'cloned_output.wav')
        sf.write(output_file_path, audio, sr)
        return output_file_path

# Function to convert audio format
def convert_audio(input_file):
    with tempfile.NamedTemporaryFile(suffix='.mp3') as tmp_file:
        tmp_file.write(input_file.getbuffer())
        audio = AudioSegment.from_mp3(tmp_file.name)
        converted_file_path = "converted_audio.wav"
        audio.export(converted_file_path, format="wav")
        return converted_file_path

# Streamlit application
st.title("Audio Cloner")

# File uploader
input_file = st.file_uploader("Upload Audio File", type=['wav', 'mp3', 'ogg'])

if input_file:
    try:
        # Convert uploaded audio to WAV format
        if input_file.type == 'audio/mpeg':
            converted_file_path = convert_audio(input_file)
            input_file_path = converted_file_path
        else:
            with tempfile.NamedTemporaryFile(suffix='.wav') as tmp_file:
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
