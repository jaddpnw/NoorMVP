import streamlit as st
import os
import random
from openai import OpenAI
from streamlit_autorefresh import st_autorefresh

# =======================
# Page setup
# =======================
st.set_page_config(
    page_title="NoorMVP",
    page_icon="🌙",
    layout="centered",
)

# =======================
# Custom CSS
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
        animation: spin 5s linear infinite;
        vertical-align: middle;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .header-noor {
        font-family: 'Helvetica', sans-serif;
        font-size: 48px;
        font-weight: bold;
        display: inline;
    }
    .header-mvp {
        font-family: 'Helvetica', sans-serif;
        font-size: 48px;
        font-weight: bold;
        color: #FFD700;
        display: inline;
    }
    .caption {
        font-size: 14px;
        color: #FFD700;
        letter-spacing: 1px;
        margin-top: -10px;
        display: block;
    }
    .ai-description {
        font-size: 18px;
        color: #C0C0C0;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .featured-verse {
        font-size: 16px;
        margin-top: 10px;
        font-style: italic;
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
    <div>
        <span class="spinning-moon">🌙</span>
        <span class="header-noor">Noor</span>
        <span class="header-mvp">MVP</span>
        <span class="caption">REMEMBRANCE, THE MOST VALUABLE PRAYER</span>
    </div>
    """,
    unsafe_allow_html=True
)

# =======================
# AI Description
# =======================
st.markdown(
    '<div class="ai-description">Noor is your <i>AI guide</i>, bringing LIGHT to your inquiries through the Quran.</div>',
    unsafe_allow_html=True
)

# =======================
# API setup
# =======================
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("API key not configured. Please set OPENAI_API_KEY in your environment.")
    st.stop()
client = OpenAI(api_key=api_key)

# =======================
# Featured verses
# =======================
featured_verses = [
    "Quran 5:48 — Compete in goodness.",
    "Quran 2:286 — Allah does not burden a soul beyond what it can bear.",
    "Quran 2:177 — Who are patient in hardship, keep up prayer, and spend in charity.",
    "Quran 16:90 — Allah commands justice and doing good.",
    "Quran 3:159 — So by mercy from Allah, you were lenient with them.",
    "Quran 39:53 — Allah forgives all sins, surely He is Most Forgiving, Most Merciful.",
    "Quran 41:53 — We will show them Our signs on the horizons and within themselves.",
    "Quran 94:5-6 — Indeed, with hardship comes ease."
]

# =======================
# Placeholder prompts
# =======================
placeholder_prompts = [
    "e.g. What is a fascinating verse?",
    "e.g. Where is the Psalms mentioned in the Quran?",
    "e.g. What are the mysterious letters in 29 chapters?",
    "e.g. How should one perform wudu?",
    "e.g. Which ayah inspires patience the most?"
]

# =======================
# User interaction
# =======================
if "user_question" not in st.session_state:
    st.session_state.user_question = ""

st.session_state.user_question = st.text_area(
    "Ask Noor",
    value=st.session_state.user_question,
    placeholder=random.choice(placeholder_prompts),
    height=15
)

if st.button("Seek Guidance"):
    question = st.session_state.user_question.strip()
    if question:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system",
                     "content": "You are Noor, an Islamic guidance assistant. "
                                "Be calm, structured, intelligent, and non-judgmental. "
                                "Use Quran, and authentic hadith references only when requested. "
                                "Provide practical advice in a welcoming, nuanced way."},
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
# Auto-rotating featured verse below question box
# =======================
st_autorefresh(interval=4000, key="verse_refresh")  # rotate every 4 seconds
st.markdown(f'<div class="featured-verse">{random.choice(featured_verses)}</div>', unsafe_allow_html=True)
