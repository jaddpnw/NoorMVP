import streamlit as st
import os
import random
from openai import OpenAI

st.set_page_config(
    page_title="NoorMVP",
    page_icon="🌙",
    layout="centered"
)

# =======================
# Page config and styles
# =======================
st.set_page_config(
    page_title="NoorMVP",
    page_icon="🌙",
    layout="centered",
)

# Custom CSS
st.markdown(
    """
    <style>
    /* Black background and white font */
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
    </style>
    """,
    unsafe_allow_html=True,
)

# Header with spinning moon
st.markdown('<div class="spinning-moon">🌙</div> <h1 style="display:inline;">NoorMVP</h1>', unsafe_allow_html=True)
st.caption("Your prayer is most valuable")

# =======================
# API key setup
# =======================
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("API key not configured. Please set OPENAI_API_KEY in your environment.")
    st.stop()

client = OpenAI(api_key=api_key)

# =======================
# App Title & Intro
# =======================
st.markdown("""
Welcome! Noor's answers will be *based on the Quran first and foremost*.
Hadith references will be provided only if specifically requested.
""")

# =======================
# Prayer & Quranic content
# =======================
prayers = {
    "Quran 2:201":
        "Our Lord, grant us good in this world and good in the Hereafter, and protect us from the punishment of the Fire.",
    "Quran 20:114":
        "My Lord, increase me in knowledge.",
    "Quran 94:6":
        "Indeed, with hardship comes ease."
}

featured_verses = [
    "Quran 39:9 — Are those who know equal to those who do not know?",
    "Quran 5:48 — Compete in goodness.",
    "Quran 2:286 — Allah does not burden a soul beyond what it can bear.",
    "Quran 2:177 — Who are patient in hardship, keep up prayer, and spend in charity"
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
                        "Use Quran, and authentic hadith references only  when requested. "
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
    "",
    placeholder="e.g. What is considered virtue?",
    height=150
)

if st.button("Seek Guidance"):
    if guidance_prompt.strip() == "":
        st.warning("Please enter a question first.")
    else:
        # Example API call (adjust for your implementation)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You answer based on the Quran first, and only reference Hadith when directly asked."},
                {"role": "user", "content": guidance_prompt}
            ]
        )
        st.markdown("### Your Guidance:")
        st.write(response.choices[0].message.content)


# =======================
# Quranic Duas Section
# =======================
st.markdown("---")
st.markdown("### 📖 Quranic Duas")
for key, value in prayers.items():
    st.markdown(f"**{key}**")
    st.write(value)

# =======================
# Featured Verse Section
# =======================
st.markdown("---")
st.markdown("### ✨ Featured Verse")
st.write(random.choice(featured_verses))
