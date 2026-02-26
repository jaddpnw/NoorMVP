import streamlit as st
import os
import random
from openai import OpenAI

# =======================
# Page setup
# =======================
st.set_page_config(
    page_title="NoorMVP",
    page_icon="🌙",
    layout="centered"
)

# =======================
# Styles and header
# =======================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@700&display=swap');

    body, .main, .block-container {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    .stButton>button {
        background-color: #FFD700;
        color: black;
        font-weight: bold;
    }
    .header-container {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .moon {
        font-size: 50px;
        animation: spin 5s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .noor {
        font-family: 'Roboto Slab', serif;
        font-size: 48px;
        color: #FFD700;
        font-weight: 700;
    }
    .mvp {
        font-family: 'Roboto Slab', serif;
        font-size: 48px;
        color: #C0C0C0;
        font-weight: 700;
    }
    .caption {
        font-size: 12px;
        text-transform: uppercase;
        color: #FFD700;
        margin-top: -5px;
        margin-left: 60px; /* align under header */
    }
    .noor-description {
        color: #C0C0C0;
        font-size: 16px;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Header with moon and NoorMVP
st.markdown(
    '<div class="header-container">'
    '<div class="moon">🌙</div>'
    '<div class="noor">Noor</div>'
    '<div class="mvp">MVP</div>'
    '</div>',
    unsafe_allow_html=True
)

# Caption / spacing
st.markdown('<div class="caption">REMEMBRANCE, THE MOST VALUABLE PRAYER</div>', unsafe_allow_html=True)

# Noor description
st.markdown('<div class="noor-description">Noor is your AI guide, bringing <b>LIGHT</b> to your inquiries through the Quran.</div>', unsafe_allow_html=True)

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
    "e.g. How many mysterious letters are in 29 chapters?",
    "e.g. What is the story of Yusuf in brief?",
    "e.g. How does the Quran define patience?"
]

# =======================
# Featured verses
# =======================
featured_verses = [
    "Quran 5:48 — Compete in goodness.",
    "Quran 2:286 — Allah does not burden a soul beyond what it can bear.",
    "Quran 2:177 — Who are patient in hardship, keep up prayer, and spend in charity.",
    "Quran 3:190 — Indeed, in the creation of the heavens and the earth are signs for those of understanding.",
    "Quran 31:20 — Do they not see that Allah has subjected to their benefit all that is in the heavens and on earth?",
    "Quran 94:5-6 — For indeed, with hardship comes ease.",
    "Quran 13:28 — Verily, in the remembrance of Allah do hearts find rest.",
    "Quran 16:97 — Whoever does righteousness, whether male or female, while a believer, We will surely give them a good life."
]

st.markdown("---")
st.write(random.choice(featured_verses))

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
                        "Use Quran, and authentic hadith references only when requested. "
                        "Provide practical advice in a welcoming, nuanced, inclusive, and grounded way."
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
# User Interaction
# =======================
guidance_prompt = st.text_area(
    "Ask Noor",
    placeholder=random.choice(placeholder_prompts),
    height=15
)

if st.button("Seek Guidance"):
    if guidance_prompt.strip() == "":
        st.warning("Please type a question first.")
    else:
        response = get_ai_response(guidance_prompt)
        st.markdown("### Your Guidance:")
        st.write(response)
