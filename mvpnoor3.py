import streamlit as st
import os
import random
import time
from openai import OpenAI

# =======================
# Page Config
# =======================
st.set_page_config(
    page_title="NoorMVP",
    page_icon="🌙",
    layout="centered"
)

# =======================
# Custom CSS
# =======================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@700&display=swap');

body {
    background-color: #000000;
    color: #ffffff;
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
}
#header-title {
    font-family: 'Roboto Slab', serif;
    font-size: 48px;
    display: inline;
    color: #FFD700;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)

# =======================
# Header
# =======================
st.markdown('<div class="spinning-moon">🌙</div> <span id="header-title">NoorMVP</span>', unsafe_allow_html=True)
st.caption("Remembrance, the most valuable prayer.")
st.markdown('<small style="color:#CCCCCC">Noor is your Quran-first guidance assistant, providing calm answers; Hadith referenced only when asked.</small>', unsafe_allow_html=True)

# =======================
# API Key Setup
# =======================
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("API key not configured. Please set OPENAI_API_KEY in your environment.")
    st.stop()
client = OpenAI(api_key=api_key)

# =======================
# App Intro
# =======================
st.markdown("*Qur’an First. Hadith by request.*")

# =======================
# Featured Verses
# =======================
featured_verses = [
    "Quran 5:48 — Compete in goodness.",
    "Quran 2:286 — Allah does not burden a soul beyond what it can bear.",
    "Quran 2:177 — Who are patient in hardship, keep up prayer, and spend in charity.",
    "Quran 94:5-6 — Indeed, with hardship comes ease.",
    "Quran 3:159 — Consult and be gentle in decision making.",
    "Quran 57:18 — Charity enriches both giver and receiver.",
    "Quran 16:90 — Justice, good conduct, and generosity are commanded.",
    "Quran 49:13 — Humanity is diverse; God values piety above status.",
    "Quran 2:255 — Allah! There is no deity except Him, the Ever-Living, the Sustainer of all existence.",
    "Quran 36:36 — Exalted is He who created all pairs – from what the earth grows and from themselves and from that which they do not know.",
    "Quran 18:109 — If the sea were ink for writing the words of my Lord, it would be exhausted before the words of my Lord were exhausted.",
    "Quran 51:56 — I did not create jinn and humans except to worship Me.",
    "Quran 55:1-13 — The Most Merciful / He taught the Quran / He created man / He taught him eloquence…"
]

# =======================
# Placeholder Prompts
# =======================
placeholder_prompts = [
    "eg What are the mysterious letters in 29 chapters?",
    "eg How can one stay patient in hardship according to the Quran?",
    "eg What guidance does the Quran give about generosity?",
    "eg How does reflection on creation deepen understanding?",
    "eg What is one verse that inspires thoughtful action?"
]
placeholder_text = random.choice(placeholder_prompts)

# =======================
# AI Guidance Function (Noor Philosophy)
# =======================
def get_ai_response(user_input):
    system_message = (
        "You are Noor, an Islamic guidance assistant. "
        "Respond calmly and clearly, grounded in the Quran. "
        "Use Hadith only if explicitly requested. "
        "Leave space for reflection only when the answer is partial or invites deeper thought. "
        "Encourage curiosity. Avoid absolutes, preaching, or mystical exaggeration. "
        "Only include a note about reflecting on the verse if it genuinely adds insight."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input}
            ],
            temperature=0.6
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# =======================
# User Interaction
# =======================
guidance_prompt = st.text_area(
    "Ask Noor",
    placeholder=placeholder_text,
    height=15
)

if st.button("Seek Guidance"):
    prompt_text = guidance_prompt.strip()
    if not prompt_text:
        st.warning("Please enter a question first.")
    else:
        response_text = get_ai_response(prompt_text)
        st.markdown("### Your Guidance:")
        st.write(response_text)

# =======================
# Rotating Featured Verses
# =======================
st.markdown("---")
verse_container = st.empty()
for _ in range(20):  # rotates 20 times; adjust as needed
    verse_container.write(random.choice(featured_verses))
    time.sleep(5)
