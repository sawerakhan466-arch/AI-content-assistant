import os
import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="⚡", layout="centered")

# Inject Custom Styling
st.markdown("""
    <style>
    /* Main Background & Font */
    .stApp {
        background-color: #FFB6C1 !important;
        color: #1e1e1e !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Form Wrapper Background */
    div[data-testid="stForm"] {
        background-color: #ffffff !important;
        border: 3px solid #ff007f !important;
        border-radius: 20px !important;
        padding: 25px !important;
        box-shadow: 6px 6px 0px #7928ca !important;
    }
    
    /* Neon Title Styling */
    .genz-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #ff007f, #7928ca, #00dfd8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
    }
    
    .genz-subtitle {
        text-align: center;
        color: #ff007f;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 30px;
    }

    /* All Input Labels */
    label, p {
        color: #1e1e1e !important;
        font-weight: 700 !important;
    }

    /* Input Boxes & Dropdowns Style */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #fff0f5 !important;
        border: 2px solid #7928ca !important;
        border-radius: 12px !important;
        color: #1e1e1e !important;
    }
    
    /* TEXT AREA BOX FIX (WHITE/LIGHT PINK BACKGROUND) */
    textarea {
        background-color: #ffffff !important;
        color: #1e1e1e !important;
        border: 2px solid #ff007f !important;
        border-radius: 12px !important;
        box-shadow: none !important;
        font-weight: 500 !important;
    }

    textarea::placeholder {
        color: #888888 !important;
    }
    
    /* SUBMIT BUTTON FIX (DARK GRADIENT WITH VISIBLE WHITE TEXT) */
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #ff007f 0%, #7928ca 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        border: 2px solid #7928ca !important;
        border-radius: 14px !important;
        padding: 12px 24px !important;
        box-shadow: 4px 4px 0px #00dfd8 !important;
        width: 100% !important;
    }
    
    div[data-testid="stFormSubmitButton"] > button p {
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
    }

    div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translate(-2px, -2px) !important;
        box-shadow: 6px 6px 0px #00dfd8 !important;
    }

    /* Content Card Output Box */
    .generated-card {
        background: #ffffff;
        border: 3px solid #00dfd8;
        border-radius: 16px;
        padding: 24px;
        color: #1e1e1e;
        box-shadow: 6px 6px 0px #ff007f;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<div class="genz-title">✨ CONTENT SLAYER ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="genz-subtitle">AI-POWERED POST GENERATOR • NO CAP 🧢</div>', unsafe_allow_html=True)

# Retrieve API Key
groq_api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    st.warning("⚠️ Groq API key is missing. Add `GROQ_API_KEY` to your Streamlit secrets!")
    st.stop()

client = Groq(api_key=groq_api_key)

# Input Controls Form
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        platform = st.selectbox(
            "🚀 Platform",
            ["LinkedIn", "Twitter/X", "Instagram", "Facebook", "TikTok Script"]
        )
        content_type = st.selectbox(
            "🔥 Vibe / Content Type",
            ["Educational", "Promotional", "Storytelling", "Hot Take", "Thought Leadership"]
        )

    with col2:
        tone = st.selectbox(
            "🎭 Tone",
            ["Casual & Gen-Z", "Professional", "Persuasive", "Inspirational", "Witty & Sarcastic"]
        )
        target_audience = st.text_input(
            "🎯 Audience",
            placeholder="e.g., Tech Founders, Gen Z Coders, Designers"
        )

    topic = st.text_area(
        "💡 Topic / Core Message",
        placeholder="e.g., Why learning Python in 2026 is an absolute cheat code"
    )

    submit_button = st.form_submit_button("⚡ GENERATE POST", use_container_width=True)

# Generation Logic
if submit_button:
    if not topic.strip():
        st.error("Hold up! Please drop a topic first.")
    else:
        with st.spinner("Cooking up the post... 👨‍🍳"):
            prompt = f"""
            You are an expert social media strategist and content creator. Generate a viral, high-converting post with these specs:

            - Platform: {platform}
            - Type: {content_type}
            - Topic: {topic}
            - Target Audience: {target_audience if target_audience else 'General Audience'}
            - Tone: {tone}

            Structure the response clearly:
            1. **Hook**: Catchy, scroll-stopping first sentence.
            2. **Main Body**: Formatting tailored for {platform} with emojis and line breaks for high readability.
            3. **Call to Action (CTA)**: Strong engagement prompt.
            4. **Hashtags**: 5 to 8 trending, relevant hashtags.
            """

            try:
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a trendy, expert social media copywriter."},
                        {"role": "user", "content": prompt}
                    ],
                    model="openai/gpt-oss-120b",
                    temperature=0.8,
                )
                
                generated_content = response.choices[0].message.content
                
                st.success("🎉 Post is ready!")
                
                # Styled Card Container
                st.markdown(f'<div class="generated-card">{generated_content}</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.download_button(
                    label="💾 Download Post (.txt)",
                    data=generated_content,
                    file_name=f"{platform.lower()}_post.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")
