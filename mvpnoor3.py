# -*- coding: utf-8 -*-
import streamlit as st
import os
import random
import time
import hashlib
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
html, body {
    background-color: #0a0a0f !important;
}
.stApp, .block-container {
    background-color: #0a0a0f !important;
}

/* Header Layout */
.header { display: flex; align-items: center; }
.moon {
    font-size: 45px; margin-right: 10px; display: inline-block;
    animation: spin 6s linear infinite;
    filter: drop-shadow(0 0 6px rgba(255, 215, 0, 0.6));
}
@keyframes spin { 0%{transform:rotate(0deg);} 100%{transform:rotate(360deg);} }

.noor { font-size: 48px; font-weight: bold; color: white; }
.mvp  { font-size: 48px; font-weight: bold; color: #FFD700; margin-left: 4px; }

.ai-guide { color: #C0C0C0; font-size: 16px; margin-top: 10px; margin-bottom: 20px; }

.rotating-verse { color: #C0C0C0; font-size: 13px; margin-top: 34px; text-align: center; }

.small-note { color: #9a9a9a; font-size: 12px; margin-top: 6px; }
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
# Options
# =======================
col1, col2 = st.columns([1, 1])
with col1:
    include_arabic = st.checkbox("Include Arabic (optional)", value=False)
with col2:
    concise = st.checkbox("Concise answer", value=True)

st.markdown('<div class="small-note">Qur’an-first: Noor cites verses for claims and labels reflections clearly.</div>',
            unsafe_allow_html=True)

# =======================
# Cache helper
# =======================
def _qhash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

if "qa_cache" not in st.session_state:
    st.session_state.qa_cache = {}

# =======================
# Input + Submit (Form)
# =======================
with st.form("noor_form", clear_on_submit=False):
    user_question = st.text_area(
        "Ask Noor",
        placeholder=random.choice(placeholder_prompts),
        height=120,
        key="noor_input"
    )
    submitted = st.form_submit_button("Seek Guidance")

# =======================
# Answer
# =======================
if submitted:
    q = (user_question or "").strip()
    if not q:
        st.stop()

    cache_key = _qhash(q + f"|arabic={include_arabic}|concise={concise}")
    if cache_key in st.session_state.qa_cache:
        st.markdown("### Your Guidance:")
        st.markdown(st.session_state.qa_cache[cache_key])
    else:
        system_prompt = f"""
You are Noor, a Qur’an-first Islamic AI guide.

Rules:
- Use the Qur’an as the ONLY source for factual/religious claims.
- ALWAYS cite verse references in the form (Surah:Ayah), e.g., (2:286).
- If something is not explicit in the Qur’an, say: "The Qur’an does not state this explicitly" and then give the closest Qur’anic themes with citations.
- Do NOT use hadith, scholars, or jurisprudence unless the user explicitly asks.
- Be grounded, inclusive, respectful, and clear.

Output format (markdown):
1) Relevant verses (bullet list with brief context + citations)
2) Core meaning (2–5 bullets)
3) Practical steps (3–7 bullets)
4) Reflection (clearly labeled; keep it short)
{ "5) Arabic (if requested)" if include_arabic else "" }

Style:
{ "Be concise." if concise else "Be thorough but not long-winded." }
"""

        with st.spinner("Noor is reflecting..."):
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt.strip()},
                    {"role": "user", "content": q},
                ],
                temperature=0.6
            )

        answer = resp.choices[0].message.content
        st.session_state.qa_cache[cache_key] = answer

        st.markdown("### Your Guidance:")
        st.markdown(answer)

# =======================
# Featured Verses (rotates on interaction)
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

# rotate each rerun (interaction)
st.session_state.verse_index = (st.session_state.verse_index + 1) % len(featured_verses)

st.markdown(
    f'<div class="rotating-verse">{featured_verses[st.session_state.verse_index]}</div>',
    unsafe_allow_html=True
)
