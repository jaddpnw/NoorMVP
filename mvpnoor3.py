import streamlit as st
import os
import random
from openai import OpenAI
from streamlit_autorefresh import st_autorefresh

# =======================
# Page config
# =======================
st.set_page_config(
    page_title="NoorMVP",
    page_icon="🌙",
    layout="centered",
)

# =======================
# Auto-refresh for rotating prompts/verses (every 10s)
# =======================
st_autorefresh(interval=10_000, key="auto_refresh")

# =======================
# Custom CSS for layout and fonts
# =======================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    body, .main, .block-container {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Roboto', sans-serif;
    }

    .stButton>button {
        background-color: #FFD700;
        color: black;
        font-weight: bold;
    }

    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }

    .spinning-moon {
        font-size: 50px;
        display: inline-block;
        animation: spin 5s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .noor-text {
        font-weight: bold;
        font-size: 48px;
        color: #FFD700;
        margin: 0;
    }

    .mvp-text {
        font-weight: bold;
        font-size: 48px;
        color: #C0C0C0;
        margin: 0;
    }

    .caption-text {
        font-size: 14px;
        color: #FFFF00;
        text-align: center;
        letter-spacing: 1px;
        margin-top: -5px;
    }

    .description-text {
        font-size: 18px;
        color: #C0C0C0;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =======================
# Header
# =======================
st.markdown(
    """
    <div class="header-container">
        <div class="spinning-moon">🌙</div>
        <h1 class="noor-text">Noor</h1><h1 class="mvp-text">MVP</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Small caption space preserved, color as requested
st.markdown('<div class="caption-text">REMEMBRANCE, YOUR MOST VALUABLE PRAYER</div>', unsafe_allow_html=True)

# =======================
# Description below header
# =======================
st.markdown(
    '<div class="description-text"><b>Noor</b> is your AI guide, bringing <b>LIGHT</b> to your inquiries through the Quran.</div>',
    unsafe_allow_html=True
)

# =======================
# API key setup
# =======================
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("API key not configured. Please set OPENAI_API_KEY in your environment.")
    st.stop()

client = OpenAI(api_key=api_key)

# =======================
# Rotating placeholder prompts
# =======================
placeholders = [
    "e.g. What is a fascinating verse?",
    "e.g. Where is the Psalms mentioned in the Quran?",
    "e.g. What do the mysterious letters in 29 chapters mean?",
    "e.g. How should one approach forgiveness?",
    "e.g. What guidance is given about patience?"
]
placeholder_text = random.choice(placeholders)

# =======================
# User Input
# =======================
guidance_prompt = st.text_area(
    "Ask Noor",
    placeholder=placeholder_text,
    height=80
)

# =======================
# Featured verses rotation
# =======================
featured_verses = [
    "Quran 5:48 — Compete in goodness.",
    "Quran 2:286 — Allah does not burden a soul beyond what it can bear.",
    "Quran 2:177 — Who are patient in hardship, keep up prayer, and spend in charity.",
    "Quran 3:159 — Be gentle and forgive; Allah loves the doers of good.",
    "Quran 94:5-6 — With hardship comes ease.",
    "Quran 16:125 — Invite to the way of your Lord with wisdom and good instruction.",
    "Quran 2:2 — This is the Book in which there is no doubt, a guidance for the God-fearing.",
    "Quran 18:10 — Those who believe and fear Allah, He will remove them from fear."
]

# =======================
# AI Guidance Function
# =======================
def get_ai_response(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Noor, an Islamic guidance assistant. "
                        "Be calm, structured, intelligent, and non-judgmental. "
                        "Use Quran primarily, and reference Hadith only when asked. "
                        "Provide practical advice in a welcoming, nuanced, and grounded way."
                    )
                },
                {"role": "user", "content": user_input}
            ],
            temperature=0.6
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# =======================
# Button & Response
# =======================
if st.button("Seek Guidance"):
    if guidance_prompt.strip():  # ✅ Fixed: works as long as anything is typed
        response_text = get_ai_response(guidance_prompt)
        st.markdown("### Your Guidance:")
        st.write(response_text)
    else:
        st.warning("Please enter a question first.")

# =======================
# Featured Verse Display
# =======================
st.markdown("---")
st.write(random.choice(featured_verses))
