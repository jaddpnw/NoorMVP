# -*- coding: utf-8 -*-
import streamlit as st
import os
import random
import time
import re
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
# Styling (UNCHANGED)
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

/* --- Inputs: fix white-on-white on desktop WITHOUT changing your look --- */
div[data-baseweb="textarea"] textarea {
    background-color: #0a0a0f !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
}
div[data-baseweb="textarea"] textarea::placeholder {
    color: rgba(192,192,192,0.80) !important;
}

</style>
""", unsafe_allow_html=True)

# =======================
# Header (UNCHANGED)
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
# API Setup (UNCHANGED)
# =======================
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Missing OPENAI_API_KEY.")
    st.stop()

client = OpenAI(api_key=api_key)

# =======================
# Noor POV / Instruction (FUSED IN)
# =======================
SYSTEM_PROMPT = """You are Noor, a Qur’an-first guidance assistant.

Core approach:
- Prioritize guidance directly from the Qur’an above all else.
- Provide verse bundles, not single-verse replies: 1 Primary verse + 2–4 Supporting verses.
- Cite references as (Surah:Ayah). If you are unsure of a reference, say you are unsure rather than inventing.
- Keep guidance gentle, inclusive, non-sectarian, and practically useful.
- Do NOT quote or rely on hadith unless the user explicitly asks for hadith.
- Avoid long debates; keep it clear and structured.

Output format (follow exactly):
1) Primary verse: (Surah:Ayah) — short paraphrase (no long quotes)
2) Supporting verses:
   - (Surah:Ayah) — short paraphrase
   - (Surah:Ayah) — short paraphrase
   - (Surah:Ayah) — short paraphrase
3) Brief guidance (3–6 sentences), connecting the verses to the question.

Important:
- If the question asks for a ruling (fatwa), respond with Qur’an-first guidance and encourage consulting a qualified scholar.
"""

def clean_question(q: str) -> str:
    q = (q or "").strip()
    q = re.sub(r"\s+", " ", q)
    return q

# =======================
# Placeholder Prompts (UNCHANGED)
# =======================
placeholder_prompts = [
    "What verse speaks about patience?",
    "Where is mercy described most beautifully?",
    "What does the Quran say about hardship?",
    "What are the mysterious letters in 29 chapters?",
]

# =======================
# Question Input (UNCHANGED)
# =======================
user_question = st.text_area(
    "Ask Noor",
    placeholder=random.choice(placeholder_prompts),
    height=120,
    key="noor_input"
)

# =======================
# Button + Response (ONLY prompt logic changed)
# =======================
if st.button("Seek Guidance"):

    q = clean_question(user_question)

    if q:
        with st.spinner("Noor is reflecting..."):
            response = client.chat.completions.create(
                model=os.getenv("NOOR_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": q}
                ],
                temperature=0.5
            )

        st.markdown("### Your Guidance:")
        st.write(response.choices[0].message.content)

    # If empty → do nothing


# =======================
# Rotating Verses (UNCHANGED)
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
