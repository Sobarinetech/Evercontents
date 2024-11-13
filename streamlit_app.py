import streamlit as st
import google.generativeai as genai

# Configure the API key securely
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("Ever AI - Automated Content Creation & Repurposing")
st.write("Use generative AI to create unique articles, social media posts, and more from a single prompt.")

# Prompt input field
prompt = st.text_input("Enter your main content idea or prompt:", "Best alternatives to JavaScript?")

# Select the content type for repurposing
content_type = st.selectbox("Select content type for repurposing:", 
                            ["Article", "Blog Post", "Social Media Post", "Tweet", "Summary", "Visual"])

# Button to generate response
if st.button("Generate Content"):
    try:
        # Configure the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate response based on prompt and content type
        response = model.generate_content(prompt)
        
        # Display response based on selected content type
        st.write("Generated Content:")
        
        if content_type == "Article" or content_type == "Blog Post":
            st.write("### Full-Length Content:")
            st.write(response.text)
        
        elif content_type == "Social Media Post":
            st.write("### Social Media Caption:")
            caption = response.text[:150] + "..."  # Shorten for social media
            st.write(caption)
            st.write("#### Suggested Hashtags:")
            st.write("#AI #GenerativeAI #Automation #ContentCreation")
        
        elif content_type == "Tweet":
            tweet = response.text[:280]
            st.write(f"Tweet:\n{tweet}")
        
        elif content_type == "Summary":
            summary = response.text[:100] + "..."  # Short summary for quick read
            st.write("### Summary:")
            st.write(summary)
        
        elif content_type == "Visual":
            st.write("### Visual Content Idea:")
            st.write("Consider creating an infographic or visual representation based on the following:")
            st.write(response.text[:150] + "...")
            
    except Exception as e:
        st.error(f"Error: {e}")
