import streamlit as st
import os
import random
from openai import OpenAI

# =======================
# Page Config
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
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
    
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
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    h1 {
        font-family: 'Bebas Neue', sans-serif;
        font-weight: 900;
        font-size: 60px;
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =======================
# Header with spinning moon
# =======================
st.markdown('<div class="spinning-moon">🌙</div> <h1><span style="color:#FFD700;">NOOR</span><span style="color:#CCCCCC;">MVP</span></h1>', unsafe_allow_html=True)
st.caption("Remembrance, your most valuable prayer.")

# =======================
# Tagline / Description
# =======================
st.markdown(
    '<p style="color:#CCCCCC; font-size:18px;">'
    '<b>Noor</b> is your AI guide, bringing <b>light</b> to your inquiries through the Quran.'
    '</p>',
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
# Featured Verses
# =======================
featured_verses = [
    "Quran 5:48 — Compete in goodness.",
    "Quran 2:286 — Allah does not burden a soul beyond what it can bear.",
    "Quran 2:177 — Who are patient in hardship, keep up prayer, and spend in charity.",
    "Quran 3:190 — Indeed, in the creation of the heavens and the earth, and the alternation of night and day are signs for those of understanding.",
    "Quran 16:97 — Whoever does righteousness, whether male or female, while being a believer — We will surely give them a good life.",
    "Quran 39:53 — Say, 'O My servants who have transgressed against themselves, do not despair of the mercy of Allah.'",
    "Quran 94:5-6 — For indeed, with hardship comes ease. Indeed, with hardship comes ease."
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
                        "Use Quran, and authentic Hadith references only when requested. "
                        "Provide practical advice in a welcoming, nuanced way."
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
    placeholder="e.g. What are the mysterious letters that appear in 29 different chapters?",
    height=15
)

if st.button("Seek Guidance"):
    if guidance_prompt.strip() == "":
        st.warning("Please enter a question first.")
    else:
        response_text = get_ai_response(guidance_prompt)
        st.markdown("### Your Guidance:")
        st.write(response_text)

# =======================
# Rotating Featured Verse Section
# =======================
st.markdown("---")
st.markdown(
    f'<p style="text-align:center; font-size:16px; color:#CCCCCC;">{random.choice(featured_verses)}</p>',
    unsafe_allow_html=True
)

# =======================
# Donation Section
# =======================
st.markdown("---")
st.markdown(
    '<div style="text-align:center; color:#CCCCCC;">'
    'Support Noor if it helps you: '
    '<a href="https://www.paypal.com/donate?hosted_button_id=YOUR_BUTTON_ID" target="_blank" style="color:#FFD700;">Donate</a>'
    '</div>',
    unsafe_allow_html=True
)
