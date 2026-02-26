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

    /* Ensure dark background on all devices */
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
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Header Fonts */
    h1.noor {
        font-family: 'Bebas Neue', sans-serif;
        font-weight: 900;
        font-size: 60px;  /* restored size for proper display */
        display: inline;
        margin: 0;
        color: #FFD700;
    }

    h1.mvp {
        font-family: 'Bebas Neue', sans-serif;
        font-weight: 900;
        font-size: 60px;  /* matched with Noor */
        display: inline;
        margin: 0;
        color: #CCCCCC;
    }

    .caption {
        font-size: 18px;
        color: #CCCCCC;
        margin-top: 5px;
    }

    .rotating-placeholder {
        color: #AAAAAA;
        font-style: italic;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =======================
# Header
# =======================
st.markdown('<div class="spinning-moon">🌙</div> <h1 class="noor">Noor</h1><h1 class="mvp">MVP</h1>', unsafe_allow_html=True)
st.markdown('<div class="caption">Remembrance, your most valuable prayer.</div>', unsafe_allow_html=True)

# =======================
# Tagline
# =======================
st.markdown(
    '<p style="color:#CCCCCC; font-size:18px;">'
    '<b>Noor</b> is your AI guide, bringing <b>LIGHT</b> to your inquiries through the Quran.'
    '</p>',
    unsafe_allow_html=True
)

# =======================
# OpenAI API setup
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
    "Quran 3:190 — Indeed, in the creation of the heavens and the earth, and the alternation of night and day are signs for those of understanding.",
    "Quran 16:97 — Whoever does righteousness, whether male or female, while being a believer — We will surely give them a good life.",
    "Quran 39:53 — Say, 'O My servants who have transgressed against themselves, do not despair of the mercy of Allah.'",
    "Quran 94:5-6 — For indeed, with hardship comes ease. Indeed, with hardship comes ease."
]

# =======================
# AI Response Function
# =======================
def get_ai_response(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Noor, an AI Islamic guidance assistant. "
                        "Respond in a lively, thoughtful, and inspiring manner — beautifully spicy — "
                        "while remaining Quran-centered, neutral, and inclusive. "
                        "Always use the Quran first, quoting chapter and verse when relevant. "
                        "Highlight moral, ethical, and spiritual principles praised by the Quran: "
                        "patience, justice, charity, gratitude, compassion, and honesty. "
                        "Do NOT make definitive statements about anyone's salvation. "
                        "Include Hadith only if the user explicitly asks, and present it as practical guidance. "
                        "Provide insights in a welcoming, reflective, and elegant manner, encouraging thought and reflection."
                    )
                },
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# =======================
# Rotating placeholders
# =======================
placeholders = [
    "What is a fascinating verse?",
    "Where is the Psalms mentioned in the Quran?",
    "How should one perform wudu?",
    "What does the Quran say about gratitude?",
    "Which verse inspires patience the most?"
]
rotating_placeholder = random.choice(placeholders)

guidance_prompt = st.text_area(
    "Ask Noor",
    placeholder=f"e.g. {rotating_placeholder}",
    height=15
)

# =======================
# Button and AI response
# =======================
if st.button("Seek Guidance"):
    # Trim spaces and newlines to accurately detect empty input
    if guidance_prompt.strip() == "":
        st.warning("Type a question first.")
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
