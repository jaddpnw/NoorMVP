import streamlit as st
import os
import random
import time
from openai import OpenAI

# =======================
# Page config
# =======================
st.set_page_config(
    page_title="NoorMVP",
    page_icon="🌙",
    layout="centered",
)

# =======================
# Styles and header
# =======================
st.markdown(
    """
    <style>
    body, .main, .block-container {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    .stButton>button {
        background-color: #FFD700;
        color: black;
        font-weight: bold;
    }
    .spinning-moon {
        font-size: 50px;
        display: inline-block;
        vertical-align: middle;
        margin-right: 10px;
    }
    .header-noor {
        display: inline;
        font-family: 'Helvetica', sans-serif;
        font-weight: bold;
        font-size: 48px;
        color: #ffffff;
    }
    .header-mvp {
        display: inline;
        font-family: 'Helvetica', sans-serif;
        font-weight: bold;
        font-size: 48px;
        color: #FFD700;
        margin-left: 2px;
    }
    .caption {
        font-size: 12px;
        color: #FFD700;
        text-transform: uppercase;
        margin-top: -10px;
    }
    .ai-guide {
        color: #C0C0C0; /* silver */
        font-size: 16px;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .light-bold {
        font-weight: bold;
    }
    .rotating-verse {
        font-size: 14px;
        margin-top: 15px;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =======================
# Header
# =======================
st.markdown(
    '<div><span class="spinning-moon">🌙</span>'
    '<span class="header-noor">Noor</span>'
    '<span class="header-mvp">MVP</span></div>',
    unsafe_allow_html=True
)
st.markdown('<div class="caption">&nbsp;</div>', unsafe_allow_html=True)  # spacing placeholder

st.markdown(
    '<div class="ai-guide">Noor is your *AI guide*, bringing <span class="light-bold">LIGHT</span> to your inquiries through the Quran.</div>',
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
# Placeholder prompts
# =======================
placeholder_prompts = [
    "e.g. What is a fascinating verse?",
    "e.g. Where is the Psalms mentioned in the Quran?",
    "e.g. How should one perform wudu?",
    "e.g. Which verses mention patience?",
    "e.g. What are the mysterious letters that appear in 29 different chapters?"
]

# =======================
# Featured / rotating verses
# =======================
featured_verses = [
    "Quran 5:48 — Compete in goodness.",
    "Quran 2:286 — Allah does not burden a soul beyond what it can bear.",
    "Quran 2:177 — Who are patient in hardship, keep up prayer, and spend in charity.",
    "Quran 3:190 — Indeed in the creation of the heavens and the earth are signs for those of understanding.",
    "Quran 94:5 — So verily, with the hardship, there is relief.",
    "Quran 57:20 — Life is like rain: growth then decay; be mindful of your deeds.",
    "Quran 13:28 — Verily, in the remembrance of Allah do hearts find rest.",
    "Quran 31:18 — Speak kindly and lower your voice.",
]

# =======================
# User interaction
# =======================
user_question = st.text_area(
    "Ask Noor",
    placeholder=random.choice(placeholder_prompts),
    height=15
)

if st.button("Seek Guidance"):
    question = user_question.strip()
    if question:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Noor, an Islamic guidance assistant. "
                            "Be calm, structured, intelligent, and non-judgmental. "
                            "Use Quran, and authentic hadith references only when requested. "
                            "Provide practical advice in a welcoming, nuanced way."
                        )
                    },
                    {"role": "user", "content": question}
                ],
                temperature=0.6
            )
            st.markdown("### Your Guidance:")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please type a question first.")

# =======================
# Rotating verse below question
# =======================
verse_placeholder = st.empty()
while True:
    verse_placeholder.markdown(
        f'<div class="rotating-verse">{random.choice(featured_verses)}</div>',
        unsafe_allow_html=True
    )
    time.sleep(10)  # rotate every 10 seconds
