# -*- coding: utf-8 -*-
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
# Styling
# =======================
st.markdown("""
<style>

/* Force full cosmic black background everywhere */
html, body, [class*="css"]  {
    background-color: #0a0a0f !important;
}

.stApp {
    background-color: #0a0a0f !important;
}

.block-container {
    background-color: #0a0a0f !important;
}

/* Header Layout */
.header {
    display: flex;
    align-items: center;
}

.moon {
    font-size: 45px;
    margin-right: 10px;
    display: inline-block;
    animation: spin 6s linear infinite;
    filter: drop-shadow(0 0 6px rgba(255, 215, 0, 0.6));
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.noor {
    font-size: 48px;
    font-weight: bold;
    color: white;
}

.mvp {
    font-size: 48px;
    font-weight: bold;
    color: #FFD700;
    margin-left: 4px;
}

.ai-guide {
    color: #C0C0C0;
    font-size: 16px;
    margin-top: 10px;
    margin-bottom: 25px;
}

.rotating-verse {
    color: #C0C0C0;
    font-size: 13px;
    margin-top: 40px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# =======================
# Header
# =======================
st.markdown("""
<div class="header">
    <div class="moon">&#127769;</div>
    <div class="noor">Noor</div>
    <div class="mvp">MVP</div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="ai-guide">Noor is your <i>AI guide</i>, bringing <b>light</b> to your inquiries through the Quran.</div>',
    unsafe_allow_html=True
)

# =======================
# API Setup
# =======================
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Missing OPENAI_API_KEY.")
    st.stop()

client = OpenAI(api_key=api_key)

# =======================
# Placeholder Prompts
# =======================
placeholder_prompts = [
    "What verse speaks about patience?",
    "Where is mercy described most beautifully?",
    "What does the Quran say about hardship?",
    "What are the mysterious letters in 29 chapters?",
]

# =======================
# Question Input (Fixed — no warning)
# =======================
user_question = st.text_area(
    "Ask Noor",
    placeholder=random.choice(placeholder_prompts),
    height=120,
    key="noor_input"
)

if st.button("Seek Guidance"):

    if user_question and user_question.strip():

        with st.spinner("Noor is reflecting..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Noor, an Islamic AI guide. "
                            "Be grounded, inclusive, thoughtful, structured, "
                            "a little spicy but respectful. "
                            "Base answers on the Quran."
                        )
                    },
                    {"role": "user", "content": user_question.strip()}
                ],
                temperature=0.6
            )

        st.markdown("### Your Guidance:")
        st.write(response.choices[0].message.content)

    # If empty → do nothing


# =======================
# Rotating Verses (9 sec, silver)
# =======================
featured_verses = [
    "Quran 94:5 — With hardship comes ease.",
    "Quran 13:28 — In remembrance of Allah do hearts find rest.",
    "Quran 2:286 — Allah does not burden a soul beyond what it can bear.",
    "Quran 16:90 — Allah commands justice and excellence.",
    "Quran 39:53 — Do not despair of the mercy of Allah.",
]

if "verse_index" not in st.session_state:
    st.session_state.verse_index = 0

if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

current_time = time.time()

if current_time - st.session_state.last_update > 9:
    st.session_state.verse_index = (
        st.session_state.verse_index + 1
    ) % len(featured_verses)
    st.session_state.last_update = current_time

st.markdown(
    f'<div class="rotating-verse">{featured_verses[st.session_state.verse_index]}</div>',
    unsafe_allow_html=True
)
