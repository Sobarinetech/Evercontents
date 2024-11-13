import streamlit as st
import google.generativeai as genai
import random
from datetime import datetime
import os

# Ensure to configure the API key securely
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
generate_related_questions = st.checkbox("Generate Related Questions")
suggest_headlines = st.checkbox("Suggest Catchy Headlines")
generate_statistics = st.checkbox("Generate Random Statistics")
create_short_form = st.checkbox("Create Short-form Content (e.g., 50 words)")
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
        
        # Generate response based on prompt
        response = model.generate_content(prompt)
        
        # Base response
        st.write("Generated Content:")
        generated_text = response.text
        st.write(generated_text)
        
        # Advanced Feature: Summarize Content
        if include_summary:
            summary = model.generate_content(f"Summarize this: {generated_text}")
            st.write("### Summary:")
            st.write(summary.text)

        # Advanced Feature: Generate Hashtags
        if generate_hashtags:
            hashtags = ["#" + word for word in random.sample(prompt.split(), min(3, len(prompt.split())))]
            st.write("### Suggested Hashtags:")
            st.write(" ".join(hashtags))

        # Advanced Feature: Create Visual Representation (placeholder)
        if create_visual:
            st.write("### Suggested Visual Representation:")
            st.image("https://placekitten.com/400/200", caption="Example Visual (Placeholder)")

        # Advanced Feature: Rewrite Content
        if content_rewrite:
            rewrite = model.generate_content(f"Rewrite this content: {generated_text}")
            st.write("### Rewritten Content:")
            st.write(rewrite.text)
        
        # Advanced Feature: Generate Related Questions
        if generate_related_questions:
            related_questions = model.generate_content(f"Generate questions related to: {prompt}")
            st.write("### Related Questions:")
            st.write(related_questions.text)
        
        # Advanced Feature: Suggest Catchy Headlines
        if suggest_headlines:
            headlines = model.generate_content(f"Suggest catchy headlines for: {prompt}")
            st.write("### Suggested Headlines:")
            st.write(headlines.text)

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
        
        # Advanced Feature: Generate Call-to-Action
        if generate_call_to_action:
            cta = f"Explore more about {prompt} today!"
            st.write("### Call-to-Action:")
            st.write(cta)
        
        # Advanced Feature: Presentation Outline
        if create_presentation_outline:
            outline = model.generate_content(f"Generate an outline for a presentation on: {prompt}")
            st.write("### Presentation Outline:")
            st.write(outline.text)

        # Advanced Feature: Repurpose for Different Platforms
        if repurpose_for_different_platforms:
            st.write("### Repurposed Content for Platforms:")
            st.write(f"LinkedIn: {generated_text[:200]}...")
            st.write(f"Instagram Caption: {generated_text[:150]}...")

        # Advanced Feature: Marketing Email
        if generate_marketing_email:
            email_content = model.generate_content(f"Generate a marketing email for: {generated_text}")
            st.write("### Marketing Email:")
            st.write(email_content.text)

        # Advanced Feature: Video Script
        if generate_video_script:
            video_script = model.generate_content(f"Generate a video script for: {generated_text}")
            st.write("### Video Script:")
            st.write(video_script.text)

        # Advanced Feature: Infographic Content
        if create_infographic_content:
            infographic_content = model.generate_content(f"Generate content for an infographic on: {generated_text}")
            st.write("### Infographic Content:")
            st.write(infographic_content.text)
        
        # Advanced Feature: Quiz Questions
        if generate_quiz_questions:
            quiz_questions = model.generate_content(f"Generate quiz questions for: {prompt}")
            st.write("### Quiz Questions:")
            st.write(quiz_questions.text)

        # Advanced Feature: Engagement Metrics
        if track_engagement_metrics:
            st.write("### Suggested Engagement Metrics:")
            st.write("Views, Click-Through Rate, Conversions, Bounce Rate")

        # Advanced Feature: Personalize Content
        if personalize_content:
            audience_segments = ["Young Professionals", "Tech Enthusiasts", "Freelancers"]
            for segment in audience_segments:
                st.write(f"### Content for {segment}:")
                st.write(f"Personalized content tailored for {segment}.")

        # File download option
        if download_as_file:
            file_name = "generated_content.txt"
            with open(file_name, "w") as f:
                f.write(generated_text)
            st.download_button(label="Download Content", data=file_name)

        # Scheduling content
        if schedule_post:
            post_time = st.time_input("Select time to post:", datetime.now().time())
            st.write(f"Scheduled post at {post_time} on {datetime.now().date()}")

    except Exception as e:
        st.error(f"Error: {e}")

