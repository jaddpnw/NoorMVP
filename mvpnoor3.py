# app.py — NoorMVP (Streamlit)
# ---------------------------------
# Requirements:
#   pip install streamlit openai
#
# Env:
#   export OPENAI_API_KEY="..."
# Optional:
#   export NOOR_MODEL="gpt-4o-mini"
#
# Run:
#   streamlit run app.py

import os
import re
import streamlit as st
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
# Theme / Styling
# =======================
st.markdown(
    """
<style>
/* --- Page background --- */
.stApp {
  background: radial-gradient(1200px circle at 10% 10%, #1b1f2a 0%, #0b0d12 40%, #07080c 100%);
  color: #EDEFF5;
}

/* --- Title area --- */
.noor-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 4px;
  margin-bottom: 2px;
}
.noor-moon { font-size: 44px; line-height: 1; }
.noor-name { font-size: 34px; font-weight: 750; letter-spacing: 0.2px; }
.noor-sub {
  margin-top: 6px;
  margin-bottom: 16px;
  color: rgba(237,239,245,0.75);
  font-size: 14px;
}

/* --- Card container --- */
.noor-card {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 18px;
  padding: 16px 16px 14px 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}

/* --- Inputs: fix white-on-white on desktop --- */
div[data-baseweb="textarea"] textarea {
  background: rgba(10,12,18,0.85) !important;
  color: #EDEFF5 !important;
  border-radius: 14px !important;
  border: 1px solid rgba(255,255,255,0.16) !important;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
}
div[data-baseweb="textarea"] textarea::placeholder {
  color: rgba(237,239,245,0.45) !important;
}

/* Remove Streamlit default label spacing a bit */
label, .stMarkdown, .stText, .stCaption { color: #EDEFF5; }

/* --- Button styling --- */
.stButton > button {
  width: 100%;
  border-radius: 14px;
  padding: 10px 14px;
  font-weight: 700;
  border: 1px solid rgba(255,255,255,0.16);
  background: linear-gradient(180deg, rgba(255,255,255,0.14), rgba(255,255,255,0.08));
  color: #EDEFF5;
}
.stButton > button:hover {
  border-color: rgba(255,255,255,0.24);
  background: linear-gradient(180deg, rgba(255,255,255,0.18), rgba(255,255,255,0.10));
}

/* --- Response box --- */
.noor-response {
  margin-top: 12px;
  background: rgba(10,12,18,0.55);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  padding: 14px 14px 10px 14px;
}
.noor-footnote {
  color: rgba(237,239,245,0.55);
  font-size: 12px;
  margin-top: 10px;
}
</style>
""",
    unsafe_allow_html=True,
)

# =======================
# Header
# =======================
st.markdown(
    """
<div class="noor-title">
  <div class="noor-moon">🌙</div>
  <div class="noor-name">Noor</div>
</div>
<div class="noor-sub">
  Qur’an-first guidance. Hadith only when directly requested.
</div>
""",
    unsafe_allow_html=True,
)

# =======================
# Helpers
# =======================
def require_api_key() -> str | None:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    return key if key else None


def normalize_question(q: str) -> str:
    q = (q or "").strip()
    q = re.sub(r"\s+", " ", q)
    return q


SYSTEM_PROMPT = """You are Noor, a Qur’an-first guidance assistant.
Rules:
- Prioritize the Qur’an above all else.
- Provide verse *bundles*: 1 Primary verse + 2–4 Supporting verses.
- Always cite references as (Surah:Ayah). If unsure, say you are unsure rather than inventing references.
- Keep explanations short, gentle, and non-sectarian.
- Do NOT quote hadith unless the user explicitly asks for hadith.
- Avoid long debates; focus on guidance and clarity.
Output format:
1) Primary verse (Surah:Ayah)
2) Supporting verses (list 2–4)
3) Brief guidance (3–6 sentences)
"""


def get_noor_answer(user_question: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.getenv("NOOR_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"

    resp = client.chat.completions.create(
        model=model,
        temperature=0.4,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_question},
        ],
    )
    return (resp.choices[0].message.content or "").strip()


# =======================
# UI
# =======================
st.markdown('<div class="noor-card">', unsafe_allow_html=True)

question = st.text_area(
    label="",
    height=140,
    placeholder=(
        "Ask for guidance…\n\n"
        "e.g. How should I respond when I’m wronged?\n"
        "e.g. What does the Qur’an say about patience?\n"
        "e.g. How do I treat my parents with excellence?"
    ),
)

ask = st.button("Seek Guidance")

st.markdown('</div>', unsafe_allow_html=True)

# =======================
# Response
# =======================
if ask:
    q = normalize_question(question)

    if not q:
        st.warning("Type a question first.")
    else:
        key = require_api_key()
        if not key:
            st.error("Missing OPENAI_API_KEY environment variable.")
        else:
            with st.spinner("Seeking guidance…"):
                try:
                    answer = get_noor_answer(q)
                    if not answer:
                        st.error("No response returned. Try again.")
                    else:
                        st.markdown(f'<div class="noor-response">\n\n{answer}\n\n</div>', unsafe_allow_html=True)
                        st.markdown(
                            '<div class="noor-footnote">'
                            "Note: Noor offers Qur’an-first guidance, not a legal ruling (fatwa). "
                            "If you need scholarly counsel, consult a qualified teacher."
                            "</div>",
                            unsafe_allow_html=True,
                        )
                except Exception as e:
                    st.error("The app hit an error while generating a response.")
                    st.code(str(e))
