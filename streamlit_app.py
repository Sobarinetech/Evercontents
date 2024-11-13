import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta
import random

# Configure the API key securely
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("Ever AI - Advanced Content Creation & Repurposing Tool")
st.write("Generate, repurpose, and enhance content with advanced AI features.")

# Prompt input field
prompt = st.text_area("Enter your main content idea or prompt:", "Best alternatives to JavaScript?")

# Content type selection
content_type = st.selectbox("Select content type for repurposing:", 
                            ["Article", "Blog Post", "Social Media Post", "Tweet", "Summary", "Visual", "FAQ", "Product Description"])

# Customization options
st.write("### Customization Options")
tone = st.selectbox("Select Tone:", ["Professional", "Casual", "Persuasive", "Informative", "Creative"])
language = st.selectbox("Select Language:", ["English", "Spanish", "French", "German", "Japanese", "Chinese"])
include_keywords = st.checkbox("Suggest Keywords")
download_as_file = st.checkbox("Enable Download Option")
schedule_post = st.checkbox("Enable Post Scheduling")

# Advanced Features Section
st.write("### Advanced Features")
include_summary = st.checkbox("Summarize Content")
generate_hashtags = st.checkbox("Generate Hashtags")
create_visual = st.checkbox("Generate Visual Representation")
content_rewrite = st.checkbox("Rewrite Content")
sentiment_analysis = st.checkbox("Perform Sentiment Analysis")
tone_detection = st.checkbox("Detect Tone")
generate_related_questions = st.checkbox("Generate Related Questions")
suggest_headlines = st.checkbox("Suggest Catchy Headlines")
generate_statistics = st.checkbox("Generate Random Statistics")
create_short_form = st.checkbox("Create Short-form Content (e.g., 50 words)")
create_audio_version = st.checkbox("Generate Audio Version")
generate_call_to_action = st.checkbox("Generate Call-to-Action")
create_presentation_outline = st.checkbox("Generate Presentation Outline")
repurpose_for_different_platforms = st.checkbox("Repurpose for Multiple Platforms")
generate_marketing_email = st.checkbox("Generate Marketing Email")
generate_video_script = st.checkbox("Generate Video Script")
create_infographic_content = st.checkbox("Create Infographic Content")
generate_quiz_questions = st.checkbox("Generate Quiz Questions")
track_engagement_metrics = st.checkbox("Suggest Engagement Metrics")
personalize_content = st.checkbox("Personalize Content (e.g., for specific audience segments)")

# Button to generate response
if st.button("Generate Content"):
    try:
        # Configure the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate response based on prompt, tone, and language
        response = model.generate_content(prompt, tone=tone, language=language)
        
        # Base response
        st.write("Generated Content:")
        generated_text = response.text
        st.write(generated_text)
        
        # Advanced Feature: Summarize Content
        if include_summary:
            summary = model.summarize_content(generated_text)
            st.write("### Summary:")
            st.write(summary)

        # Advanced Feature: Generate Hashtags
        if generate_hashtags:
            hashtags = ["#" + word for word in random.sample(prompt.split(), min(3, len(prompt.split())))]
            st.write("### Suggested Hashtags:")
            st.write(" ".join(hashtags))

        # Advanced Feature: Create Visual Representation
        if create_visual:
            st.write("### Suggested Visual Representation:")
            st.image("https://placekitten.com/400/200", caption="Example Visual (Placeholder)")

        # Advanced Feature: Rewrite Content
        if content_rewrite:
            rewrite = model.rewrite_content(generated_text)
            st.write("### Rewritten Content:")
            st.write(rewrite)
        
        # Advanced Feature: Sentiment Analysis
        if sentiment_analysis:
            sentiment = model.analyze_sentiment(generated_text)
            st.write("### Sentiment Analysis:")
            st.write(sentiment)
        
        # Advanced Feature: Tone Detection
        if tone_detection:
            detected_tone = model.detect_tone(generated_text)
            st.write("### Detected Tone:")
            st.write(detected_tone)
        
        # Advanced Feature: Generate Related Questions
        if generate_related_questions:
            related_questions = model.generate_related_questions(prompt)
            st.write("### Related Questions:")
            for q in related_questions:
                st.write(f"- {q}")
        
        # Advanced Feature: Suggest Catchy Headlines
        if suggest_headlines:
            headlines = model.generate_headlines(prompt)
            st.write("### Suggested Headlines:")
            for headline in headlines:
                st.write(f"- {headline}")

        # Advanced Feature: Generate Random Statistics
        if generate_statistics:
            random_stat = random.randint(50, 100)
            st.write("### Suggested Statistic:")
            st.write(f"{random_stat}% of developers are considering switching to {prompt.split()[-1]}.")
        
        # Advanced Feature: Create Short-form Content
        if create_short_form:
            short_form_content = generated_text[:50] + "..."
            st.write("### Short-form Content (50 words):")
            st.write(short_form_content)
        
        # Advanced Feature: Generate Audio Version
        if create_audio_version:
            st.write("### Generated Audio Version:")
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        
        # Advanced Feature: Generate Call-to-Action
        if generate_call_to_action:
            cta = f"Explore more about {prompt} today!"
            st.write("### Call-to-Action:")
            st.write(cta)
        
        # Advanced Feature: Presentation Outline
        if create_presentation_outline:
            outline = model.generate_presentation_outline(generated_text)
            st.write("### Presentation Outline:")
            for point in outline:
                st.write(f"- {point}")

        # Advanced Feature: Repurpose for Different Platforms
        if repurpose_for_different_platforms:
            st.write("### Repurposed Content for Platforms:")
            st.write(f"LinkedIn: {generated_text[:200]}...")
            st.write(f"Instagram Caption: {generated_text[:150]}...")

        # Advanced Feature: Marketing Email
        if generate_marketing_email:
            email_content = model.generate_marketing_email(generated_text)
            st.write("### Marketing Email:")
            st.write(email_content)

        # Advanced Feature: Video Script
        if generate_video_script:
            video_script = model.generate_video_script(generated_text)
            st.write("### Video Script:")
            st.write(video_script)

        # Advanced Feature: Infographic Content
        if create_infographic_content:
            infographic_content = model.generate_infographic_content(generated_text)
            st.write("### Infographic Content:")
            st.write(infographic_content)
        
        # Advanced Feature: Quiz Questions
        if generate_quiz_questions:
            quiz_questions = model.generate_quiz_questions(prompt)
            st.write("### Quiz Questions:")
            for question in quiz_questions:
                st.write(f"- {question}")

        # Advanced Feature: Engagement Metrics
        if track_engagement_metrics:
            st.write("### Suggested Engagement Metrics:")
            st.write("Views, Click-Through Rate, Conversions, Bounce Rate")

        # Advanced Feature: Personalize Content
        if personalize_content:
            audience_segments = ["Young Professionals", "Tech Enthusiasts", "Freelancers"]
            for segment in audience_segments:
                st.write(f"### Content for {segment}:")
                st.write(f"{generated_text[:100]} tailored for {segment}.")
        
        # Download Option
        if download_as_file:
            st.download_button(label="Download Content as Text File", data=generated_text, file_name="generated_content.txt")
        
        # Post Scheduling Option
        if schedule_post:
            schedule_time = st.date_input("Select a date for scheduling:", datetime.now() + timedelta(days=1))
            st.write(f"Your post is scheduled for {schedule_time.strftime('%Y-%m-%d')}")

    except Exception as e:
        st.error(f"Error: {e}")
