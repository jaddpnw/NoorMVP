# -*- coding: utf-8 -*-
import os
import random
import re
import time
import streamlit as st
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
CSS = """
<style>
html, body { background-color: #0a0a0f !important; }
.stApp, .block-container { background-color: #0a0a0f !important; }

.header { display:flex; align-items:center; }

.moon {
  font-size:45px;
  margin-right:10px;
  animation:spin 6s linear infinite;
  filter:drop-shadow(0 0 8px rgba(255,215,0,0.7));
}
@keyframes spin { 0%{transform:rotate(0deg);} 100%{transform:rotate(360deg);} }

.noor { font-size:48px; font-weight:bold; color:#ffffff; }
.mvp  { font-size:48px; font-weight:bold; color:#FFD700; margin-left:4px; }

.tagline{
  color:#EAEAEA;
  font-size:17px;
  margin-top:10px;
  margin-bottom:16px;
}
.lightword{ color:#FFD700; font-weight:bold; }

.noor-box{
  background:rgba(255,255,255,0.025);
  border:1px solid rgba(255,255,255,0.05);
  border-radius:14px;
  padding:18px;
  margin-top:14px;
}

.noor-answer{
  color:#F5F5F5;
  font-size:16px;
  line-height:1.75;
}

/* =========================
   TEXTAREA FIX (Desktop)
   Streamlit uses BaseWeb:
   - outer container: div[data-baseweb="textarea"]
   - inner element: textarea
   We style BOTH to avoid white-on-white.
   ========================= */

div[data-baseweb="textarea"] > div {
  background: rgba(255,255,255,0.03) !important;
  border-radius: 12px !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
}

div[data-baseweb="textarea"] textarea {
  background: transparent !important;
  color: #FFFFFF !important;
  caret-color: #FFD700 !important;
}

div[data-baseweb="textarea"] textarea::placeholder {
  color: #9E9E9E !important;
  opacity: 1 !important;
}

div[data-baseweb="textarea"] > div:focus-within {
  border: 1px solid rgba(255,215,0,0.35) !important;
  box-shadow: 0 0 10px rgba(255,215,0,0.15) !important;
}

/* Button */
.stButton button{
  border-radius:12px !important;
  border:1px solid rgba(255,215,0,0.22) !important;
}
.stButton button:hover{
  box-shadow:0 0 10px rgba(255,215,0,0.4);
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# =======================
# Header
# =======================
st.markdown("""
<div class="header">
  <div class="moon">🌙</div>
  <div class="noor">Noor</div>
  <div class="mvp">MVP</div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="tagline"><b><i>Noor is your AI Guide</i></b>, bringing <span class="lightword">light</span> to curiosity.</div>',
    unsafe_allow_html=True
)

# =======================
# API
# =======================
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY missing.")
    st.stop()

client = OpenAI(api_key=api_key)

# =======================
# Noor System Prompt
# =======================
SYSTEM_PROMPT = """
You are Noor.

You present the Qur'an clearly and respectfully.

Rules:
- Use ONLY the Qur'an for claims.
- Cite verses frequently as (Surah:Ayah).
- Keep human explanation minimal.
- Do not declare individuals or groups saved or condemned.
- Avoid sectarian debates.
- If the Qur'an does not settle something explicitly, say God knows best and show verses indicating this.

Tone:
Quiet, reflective, slightly provocative toward ego but never insulting.

Structure responses (markdown):

1) Closest verses to the question
2) A deeper mirror in the text
3) What this suggests
4) Where the Qur'an leaves the matter with God
""".strip()

# =======================
# Session
# =======================
if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""

# =======================
# Input
# =======================
placeholder_prompts = [
    "What does the Qur’an say about fear?",
    "What does the Qur’an say about arrogance?",
    "What does the Qur’an say about judgment?",
    "What does the Qur’an say about sincerity?",
    "What does the Qur’an say about guidance?",
]

with st.form("ask_noor"):
    user_q = st.text_area(
        "Ask Noor",
        placeholder=random.choice(placeholder_prompts),
        height=120,
    )
    submit = st.form_submit_button("Seek Guidance")

# =======================
# Response
# =======================
def render_answer(text: str):
    safe = (text or "").strip()
    st.markdown(
        f'<div class="noor-box"><div class="noor-answer">{safe}</div></div>',
        unsafe_allow_html=True
    )

if submit:
    q = (user_q or "").strip()
    if not q:
        st.stop()

    full_text = ""
    box = st.empty()

    try:
        with st.spinner("Noor is reflecting..."):
            time.sleep(0.15)  # helps spinner appear reliably

            # Stream first (nice UX)
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                stream=True,
                temperature=0.6,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": q},
                ],
            )

            for chunk in stream:
                delta = chunk.choices[0].delta
                content = getattr(delta, "content", None)
                if content:
                    full_text += content
                    box.markdown(
                        f'<div class="noor-box"><div class="noor-answer">{full_text}</div></div>',
                        unsafe_allow_html=True
                    )

            # Fallback: if stream yields nothing, do non-stream once
            if not full_text.strip():
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    temperature=0.6,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": q},
                    ],
                )
                full_text = resp.choices[0].message.content or ""

        # Show final (ensures something remains on screen)
        box.empty()
        render_answer(full_text)

    except (RateLimitError, APITimeoutError) as e:
        st.warning("Noor is temporarily rate-limited or timed out. Please try again.")
        st.caption(str(e))
    except APIError as e:
        st.warning("OpenAI API error. Please try again.")
        st.caption(str(e))
    except Exception as e:
        st.error("Unexpected error while generating Noor's response.")
        st.exception(e)

    st.session_state.last_answer = full_text

# =======================
# Featured verse
# =======================
featured = [
    "Qur’an 39:23 — skins shiver, then hearts soften to remembrance.",
    "Qur’an 22:46 — hearts may be blind though eyes see.",
    "Qur’an 53:32 — do not declare yourselves pure.",
    "Qur’an 6:59 — with Him are the keys of the unseen.",
]
st.markdown(
    f'<div style="margin-top:26px;color:#C0C0C0;text-align:center;font-size:13px;">{random.choice(featured)}</div>',
    unsafe_allow_html=True
)
