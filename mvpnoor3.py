import streamlit as st
import os
import random
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
# Header and styles
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

    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 10px;
    }

    .header-row {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
    }

    .spinning-moon {
        font-size: 50px;
        animation: spin 5s linear infinite;
        margin-right: 10px;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .noor {
        font-family: 'Arial Black', sans-serif;
        font-size: 60px;
        font-weight: 900;
        color: #FFD700;
        margin: 0;
    }

    .mvp {
        font-family: 'Arial Black', sans-serif;
        font-size: 60px;
        font-weight: 900;
        color: #CCCCCC;
        margin-left: 5px;
    }

    .caption {
        font-family: Verdana, sans-serif;
        font-size: 14px;
        color: #AAAAAA;
        text-transform: uppercase;
        margin-top: -5px;
    }

    .ai-guide {
        font-family: Verdana, sans-serif;
        font-size: 16px;
        font-weight: 600;
        color: #FFD700;
        margin-top: 5px;
        text-align: center;
    }
    </style>

    <div class="header-container">
        <div class="header-row">
            <div class="spinning-moon">🌙</div>
            <div>
                <span class="noor">Noor</span><span class="mvp">MVP</span>
            </div>
        </div>
        <div class="caption">REMEMBRANCE, YOUR MOST VALUABLE PRAYER</div>
        <div class="ai-guide">Noor is your AI guide, bringing <strong>LIGHT</strong> to your inquiries through the Quran.</div>
    </div>
    """,
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
placeholder_prompts = [
    "What is a fascinating verse?",
    "Where is the Psalms mentioned in the Quran?",
    "What are the mysterious letters in 29 chapters?",
    "What does patience truly mean in Quran?",
    "How is charity emphasized in the Quran?"
]

# =======================
# Prayer & Quranic content
# =======================
featured_verses = [
    "Quran 5:48 — Compete in goodness.",
    "Quran 2:286 — Allah does not burden a soul beyond what it can bear.",
    "Quran 2:177 — Who are patient in hardship, keep up prayer, and spend in charity.",
    "Quran 24:35 — Allah is the Light of the heavens and the earth.",
    "Quran 3:190 — Indeed, in the creation of the heavens and the earth are signs for those of understanding.",
    "Quran 49:13 — The most honored of you in the sight of Allah is the most righteous.",
    "Quran 2:152 — Remember Me; I will remember you."
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
                        "Use Quran extensively, provide Hadith references only when requested. "
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
    placeholder=random.choice(placeholder_prompts),
    height=15
)

if st.button("Seek Guidance"):
    if guidance_prompt.strip():
        response = get_ai_response(guidance_prompt)
        st.markdown("### Your Guidance:")
        st.write(response)
    else:
        st.warning("Please enter a question first.")

# =======================
# Featured Verse Section
# =======================
st.markdown("---")
st.write(random.choice(featured_verses))
