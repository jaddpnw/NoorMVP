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
# Custom CSS for header & dark mode
# =======================
st.markdown(
    """
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
    
    /* Dark mode across devices */
    body, .main, .block-container {
        background-color: #000000 !important;
        color: #ffffff !important;
    }

    .stButton>button {
        background-color: #FFD700;
        color: black;
        font-weight: bold;
    }

    /* Header container */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 15px;
    }

    /* Spinning moon */
    .spinning-moon {
        font-size: 50px;
        display: inline-block;
        animation: spin 5s linear infinite;
        margin-bottom: 10px;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* NoorMVP text side by side */
    h1.noor {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 60px;
        font-weight: 900;
        margin: 0;
        color: #FFD700;
        display: inline;
    }
    h1.mvp {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 60px;
        font-weight: 900;
        margin: 0 0 0 5px;
        color: #CCCCCC;
        display: inline;
    }

    /* Caption below header */
    .caption {
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        font-weight: 400;
        color: #AAAAAA;
        margin-top: -5px;
    }

    /* AI guide line */
    .ai-guide {
        font-family: 'Arial', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: #FFD700; /* emphasize LIGHT */
        margin-top: 5px;
        text-align: center;
    }
    """,
    unsafe_allow_html=True
)

# =======================
# Header HTML
# =======================
st.markdown(
    """
    <div class="header-container">
        <div class="spinning-moon">🌙</div>
        <div>
            <h1 class="noor">Noor</h1><h1 class="mvp">MVP</h1>
        </div>
        <div class="caption">Remembrance, your most valuable prayer.</div>
        <div class="ai-guide">Noor is your AI guide, bringing <strong>LIGHT</strong> to your inquiries through the Quran.</div>
    </div>
    """,
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
