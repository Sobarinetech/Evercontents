import streamlit as st
import random
import os
from moviepy.editor import *
from moviepy.video.fx.all import fadein, fadeout, speedx
import fitz  # PyMuPDF
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import emoji
import google.generativeai as genai
import textwrap

# Ensure the static directory exists
if not os.path.exists('static'):
    os.makedirs('static')

# Constants
CHARACTER_LIMIT = 2000

# Utility Functions
def pdf_to_text(pdf_file):
    """Extract text from a PDF file with a character limit."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
        if len(text) >= CHARACTER_LIMIT:
            break
    return text[:CHARACTER_LIMIT]

def create_audio_from_text(text, lang='en'):
    """Create audio from text using gTTS."""
    tts = gTTS(text=text, lang=lang, slow=False)
    audio_path = "output_audio.mp3"
    tts.save(audio_path)
    return audio_path

def create_custom_text_image(text, size=(640, 480)):
    """Create an image with custom text."""
    image = Image.new("RGB", size, (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    wrapped_text = textwrap.fill(text, width=30)
    draw.text((10, 10), wrapped_text, fill="black", font=font)
    return image

def create_video_with_transitions(thumbnails, audio_path, durations, text_overlays):
    """Create a video with transitions and audio."""
    clips = []
    audio_clip = AudioFileClip(audio_path)

    for idx, thumbnail in enumerate(thumbnails):
        duration = durations[idx]
        image = ImageClip(thumbnail).set_duration(duration).fx(fadein, 1).fx(fadeout, 1)

        if text_overlays and idx < len(text_overlays):
            text_image = create_custom_text_image(text_overlays[idx], size=image.size)
            text_clip = ImageClip(text_image).set_duration(duration).set_position('bottom')
            clips.append(text_clip)

        clips.append(image)

    video = concatenate_videoclips(clips, method="compose").set_audio(audio_clip)
    return video

# Streamlit UI
st.set_page_config(page_title="🎬 Create Youtube Videos Effortlessly", layout="wide")
st.title("🎬 Sobarine Content Technologies 🌊")
st.markdown("<h2 style='color: #66ccff; text-align: center;'>Create Stunning Videos Effortlessly!</h2>", unsafe_allow_html=True)

# Main content
st.header("Upload Your Content")
pdf_file = st.file_uploader("Upload your PDF 📄 (max 2000 characters)", type="pdf")
thumbnails = st.file_uploader("Upload images 🖼️", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
background_music = st.file_uploader("Upload background music 🎶 (optional)", type=["mp3", "wav"], accept_multiple_files=True)

# Text input with character limit
text_input = st.text_area("Paste your content (max 2000 characters)", max_chars=CHARACTER_LIMIT)
st.write(f"Characters used: {len(text_input)}")

# Video customization options
st.header("Customize Your Video")
text_overlays = st.text_area("Enter custom text for overlays (one per thumbnail)").splitlines()
language_option = st.selectbox("Select TTS language:", ['en', 'es', 'fr', 'de', 'it'])

# Generative AI prompt
prompt = st.text_input("Enter a prompt for AI to generate content:", "Write a compelling script for a YouTube video about the best free TTS")

# Configure Google Generative AI API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Button to generate response from AI
if st.button("Generate AI Response"):
    try:
        # Load and configure the model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Generate response from the model
        response = model.generate_content(prompt)

        # Display AI response
        st.write("AI Response:")
        st.write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")

# Generate content
if st.button("Generate Video"):
    if pdf_file is not None:
        text = pdf_to_text(pdf_file)
        audio_path = create_audio_from_text(text, lang=language_option)
        video = create_video_with_transitions(thumbnails, audio_path, [5] * len(thumbnails), text_overlays)

        # Save the video
        video.write_videofile("output_video.mp4", codec='libx264')
        st.video("output_video.mp4")
        st.success("Video created successfully!")
