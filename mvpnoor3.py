# -*- coding: utf-8 -*-
import streamlit as st
import os
import random
import time
from openai import OpenAI
from openai import APIError, RateLimitError, APITimeoutError

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
    margin-bottom: 14px;
}

.method-line {
    color: #BFBFBF;
    font-size: 13px;
    margin-top: 2px;
    margin-bottom: 8px;
}

.psalms-line {
    color: #CFCFCF;
    font-size: 12.5px;
    margin-top: 0px;
    margin-bottom: 14px;
    font-style: italic;
}

.rotating-verse {
    color: #C0C0C0;
    font-size: 13px;
    margin-top: 40px;
    text-align: center;
}

/* Answer box */
.noor-box {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 18px;
    margin-top: 14px;
}

.noor-answer {
    color: #F5F5F5;
    font-size: 16px;
    line-height: 1.75;
}

/* Textarea style */
div[data-baseweb="textarea"] > div {
    background: rgba(255,255,255,0.03)!important;
    border-radius: 12px!important;
    border: 1px solid rgba(255,255,255,0.10)!important;
}

div[data-baseweb="textarea"] textarea {
    background: transparent!important;
    color: #FFFFFF!important;
    caret-color: #FFD700!important;
}

/* desktop override */
@media (min-width:900px){

div[data-baseweb="textarea"] > div{
    background:#FFFFFF!important;
    border:1px solid #DDD!important;
}

div[data-baseweb="textarea"] textarea{
    color:#111!important;
    caret-color:#FFD700!important;
}

div[data-baseweb="textarea"] textarea::placeholder{
    color:#777!important;
}

}

/* focus glow */
div[data-baseweb="textarea"] > div:focus-within {
    border: 1px solid rgba(255,215,0,0.35)!important;
    box-shadow: 0 0 10px rgba(255,215,0,0.15)!important;
}

.stButton button {
    border-radius: 12px!important;
    border: 1px solid rgba(255,215,0,0.22)!important;
}

.stButton button:hover {
    box-shadow: 0 0 10px rgba(255,215,0,0.4);
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
    '<div class="ai-guide"><i>Noor</i> is your <i>AI guide</i>, bringing <b>light</b> to your inquiries through the Quran.</div>',
    unsafe_allow_html=True
)

# =======================
# API Setup
# =======================
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("Missing OPENAI_API_KEY.")
    st.stop()

client = OpenAI(api_key=api_key)

# =======================
# Prompt Builder
# =======================
def build_prompt(mode: str) -> str:
    if mode == "Qur’an Guidance":
        return """
You are Noor, a Qur’an-first guide.

Rules:
- Use only the Qur’an for claims.
- Noor cites its claims with Qur’anic evidence.
- Cite verses frequently in the form (Surah:Ayah).
- Keep answers concise, clear, and reflective.
- Do not declare specific individuals saved or condemned.
- Avoid sectarian disputes.
- If you are unsure of a citation, say so instead of guessing.

Tone:
- Grounded, thoughtful, morally serious, and respectful.
- At times, in a subtle way, remind the reader that nothing is hidden from God.

Structure:
Guidance:
2-5 concise sentences.

Qur’an anchors:
- (Surah:Ayah)
- (Surah:Ayah)
- (Surah:Ayah)
"""
    else:
        return """
You are Noor, reflecting on the Psalms through a Qur’an-conscious lens.

Rules:
- Treat the Qur’an as primary and final.
- The Qur’an honors what was given to David, so speak of the Psalms with reverence.
- You may reflect on themes from the Psalms in a respectful and exploratory way.
- Where fitting, connect Psalm themes back to the Qur’an.
- Do not make hard doctrinal claims based on the Psalms alone.
- Avoid sectarian disputes.
- Keep answers concise, clear, and reflective.

Tone:
- Gentle, reverent, morally awake, and respectful.

Structure:
Guidance:
2-5 concise sentences.

Qur’anic resonance:
- (Surah:Ayah)
- (Surah:Ayah)

Psalm thread:
- Briefly mention the Psalm theme or idea being explored.
"""

# =======================
# Mode selector
# =======================
mode = st.radio(
    "Mode",
    ["Qur’an Guidance", "Psalms Reflection"],
    horizontal=True
)

if mode == "Qur’an Guidance":
    st.markdown(
        '<div class="method-line">Noor cites its claims with Qur’anic evidence.</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="method-line">Noor explores the Psalms with reverence through a Qur’an-conscious lens.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="psalms-line">The Qur’an honors what was given to David, so we should too. (17:55)</div>',
        unsafe_allow_html=True
    )

# =======================
# Placeholder Prompts
# =======================
if mode == "Qur’an Guidance":
    placeholder_prompts = [
        "What verse speaks about patience?",
        "Where is mercy described most beautifully?",
        "What does the Quran say about hardship?",
        "What are the mysterious letters in 29 chapters?",
    ]
else:
    placeholder_prompts = [
        "What in the Psalms resonates with trust in God?",
        "How do the Psalms speak about fear and refuge?",
        "How might the Psalms and the Quran both speak of praise?",
        "What Psalm themes echo humility before God?",
    ]

# =======================
# Question Input
# =======================
user_question = st.text_area(
    "Ask Noor",
    placeholder=random.choice(placeholder_prompts),
    height=120,
    key="noor_input"
)

# =======================
# Response
# =======================
if st.button("Seek Guidance"):

    if user_question and user_question.strip():

        try:
            with st.spinner("Noor is reflecting..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": build_prompt(mode)
                        },
                        {
                            "role": "user",
                            "content": user_question.strip()
                        }
                    ],
                    temperature=0.6
                )

            answer = response.choices[0].message.content

            st.markdown("### Your Guidance:")
            st.markdown(
                f'<div class="noor-box"><div class="noor-answer">{answer}</div></div>',
                unsafe_allow_html=True
            )

        except (APIError, RateLimitError, APITimeoutError):
            st.warning("Temporary issue contacting Noor. Please try again.")
        except Exception as e:
            st.warning(f"Something went wrong: {e}")

    # If empty → do nothing

# =======================
# Rotating Verses
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
