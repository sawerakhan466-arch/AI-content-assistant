import os
import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="📝", layout="centered")

st.title("📝 AI Content Assistant")
st.caption("Generate tailored social media posts using Groq Llama 3")

# Retrieve API Key from Streamlit Secrets or Environment Variables
groq_api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    st.warning("⚠️ Groq API key is missing. Please add `GROQ_API_KEY` to your secrets.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=groq_api_key)

# Input Controls
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        platform = st.selectbox(
            "Platform",
            ["LinkedIn", "Twitter/X", "Instagram", "Facebook", "Blog Post Intro"]
        )
        content_type = st.selectbox(
            "Content Type",
            ["Educational", "Promotional", "Storytelling", "Announcement", "Thought Leadership"]
        )

    with col2:
        tone = st.selectbox(
            "Tone",
            ["Professional", "Casual & Friendly", "Persuasive", "Inspirational", "Witty"]
        )
        target_audience = st.text_input(
            "Target Audience",
            placeholder="e.g., Software Developers, Small Business Owners"
        )

    topic = st.text_area(
        "Topic / Key Message",
        placeholder="e.g., 5 key benefits of learning Python for AI development"
    )

    submit_button = st.form_submit_button("Generate Post", use_container_width=True)

# Generate Content Logic
if submit_button:
    if not topic.strip():
        st.error("Please enter a topic before generating content.")
    else:
        with st.spinner("Generating post..."):
            prompt = f"""
            You are an expert social media copywriter. Generate a complete post based on these specs:

            - Platform: {platform}
            - Content Type: {content_type}
            - Topic: {topic}
            - Target Audience: {target_audience if target_audience else 'General Audience'}
            - Tone: {tone}

            Structure your response exactly as follows:
            1. **Hook**: Catchy first sentence.
            2. **Main Body**: The core caption formatted nicely with emojis where appropriate for the platform.
            3. **Call to Action (CTA)**: Encouraging engagement.
            4. **Hashtags**: 5 to 10 relevant hashtags.
            """

            try:
                # Using Llama 3.1 8B Instant (free & fast model on Groq)
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a creative social media manager."},
                        {"role": "user", "content": prompt}
                    ],
                    model="openai/gpt-oss-120b",
                    temperature=0.7,
                )
                
                generated_content = response.choices[0].message.content
                
                st.success("✨ Content Generated Successfully!")
                st.markdown("---")
                st.markdown(generated_content)
                st.markdown("---")
                
                # Download Button for the output
                st.download_button(
                    label="Download Post (.txt)",
                    data=generated_content,
                    file_name=f"{platform.lower()}_post.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"An error occurred while generating content: {e}")
