# -*- coding: utf-8 -*-
import os
import random
import time
import streamlit as st
from openai import OpenAI
from openai import APIError, RateLimitError, APITimeoutError

st.set_page_config(
    page_title="NoorMVP",
    page_icon="🌙",
    layout="centered",
)

CSS = """
<style>
html, body { background-color:#0a0a0f !important; }
.stApp, .block-container { background-color:#0a0a0f !important; }

.header{display:flex;align-items:center;}

.moon{
font-size:45px;
margin-right:10px;
animation:spin 6s linear infinite;
filter:drop-shadow(0 0 8px rgba(255,215,0,0.7));
}

@keyframes spin{
0%{transform:rotate(0deg);}
100%{transform:rotate(360deg);}
}

.noor{font-size:48px;font-weight:bold;color:#fff;}
.mvp{font-size:48px;font-weight:bold;color:#FFD700;margin-left:4px;}

.tagline{
color:#EAEAEA;
font-size:17px;
margin-top:10px;
margin-bottom:10px;
}

.lightword{
color:#FFD700;
font-weight:bold;
}

.subtle-line{
color:#BFBFBF;
font-size:13px;
margin-top:2px;
margin-bottom:14px;
}

.psalms-note{
color:#CFCFCF;
font-size:12.5px;
margin-top:-4px;
margin-bottom:12px;
font-style:italic;
}

/* answer box */
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

/* mobile input style */
div[data-baseweb="textarea"] > div{
background:rgba(255,255,255,0.03)!important;
border-radius:12px!important;
border:1px solid rgba(255,255,255,0.10)!important;
}

div[data-baseweb="textarea"] textarea{
background:transparent!important;
color:#FFFFFF!important;
caret-color:#FFD700!important;
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
div[data-baseweb="textarea"] > div:focus-within{
border:1px solid rgba(255,215,0,0.35)!important;
box-shadow:0 0 10px rgba(255,215,0,0.15)!important;
}

.stButton button{
border-radius:12px!important;
border:1px solid rgba(255,215,0,0.22)!important;
}

.stButton button:hover{
box-shadow:0 0 10px rgba(255,215,0,0.4);
}

/* radio */
div[role="radiogroup"]{
gap: 16px;
margin-bottom: 4px;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# header
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

# api
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY missing.")
    st.stop()

client = OpenAI(api_key=api_key)

# prompt builder
def build_prompt(light_mode, arabic, mode):
    if mode == "Qur’an Guidance":
        base = """
You are Noor.

Present the Qur'an clearly, respectfully, and concisely.

Rules:
Use only the Qur'an for claims.
Noor cites its claims with Qur'anic evidence.
Cite verses frequently in the form (Surah:Ayah).
Keep explanation minimal, clear, and morally serious.
Do not declare individuals saved or condemned.
Avoid sectarian disputes.
If you are not sure, say so rather than inventing a citation.

Tone:
Calm, reflective, and conscience-awakening.
At times, in a subtle and non-accusatory way, remind the reader that nothing is hidden from God.

Structure:
1 Closest verses
2 Deeper mirror
3 What this suggests
4 Where Qur'an leaves the matter with God
"""
    else:
        base = """
You are Noor.

Explore the Psalms reverently through a Qur'an-conscious lens.

Rules:
Treat the Qur'an as primary and final.
The Qur'an honors what was given to David, so speak of the Psalms with reverence.
You may reflect on themes from the Psalms in a respectful and exploratory way.
Do not make hard doctrinal claims based on the Psalms alone.
Where fitting, connect Psalm themes back to Qur'anic guidance.
Avoid sectarian disputes and dismissiveness toward earlier revelation.
If you are not sure, say so rather than overstating.
Keep answers concise and clear.

Tone:
Gentle, reverent, reflective, and morally awake.

Structure:
1 Psalm thread
2 Qur'anic resonance
3 What this opens
4 Leave the matter with God
"""

    if light_mode:
        base += "\nKeep responses short and direct."

    if arabic:
        base += "\nRespond entirely in Arabic."

    return base

# input
placeholder_prompts = [
    "What does the Qur’an say about fear?",
    "What does the Qur’an say about arrogance?",
    "What does the Qur’an say about judgment?",
    "What does the Qur’an say about sincerity?",
    "What does the Qur’an say about guidance?"
]

with st.form("ask_noor"):

    mode = st.radio(
        "Mode",
        ["Qur’an Guidance", "Psalms Reflection"],
        horizontal=True
    )

    if mode == "Qur’an Guidance":
        evidence_line = "Noor cites its claims with Qur’anic evidence."
        psalms_note = ""
    else:
        evidence_line = "Noor explores the Psalms with reverence through a Qur’an-conscious lens."
        psalms_note = "The Qur’an honors what was given to David, so we should too. (17:55)"

    st.markdown(
        f'<div class="subtle-line">{evidence_line}</div>',
        unsafe_allow_html=True
    )

    if psalms_note:
        st.markdown(
            f'<div class="psalms-note">{psalms_note}</div>',
            unsafe_allow_html=True
        )

    user_q = st.text_area(
        "Ask Noor",
        placeholder=random.choice(placeholder_prompts),
        height=120
    )

    light_mode = st.checkbox("Noor’s light answers")
    arabic = st.checkbox("Respond in Arabic")

    submit = st.form_submit_button("Seek Guidance")

# response
if submit and user_q.strip():

    full_text = ""
    box = st.empty()

    try:
        with st.spinner("Noor is reflecting..."):

            system_mode = "Qur’an Guidance" if mode == "Qur’an Guidance" else "Psalms Reflection"

            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                stream=True,
                temperature=0.6,
                messages=[
                    {"role": "system", "content": build_prompt(light_mode, arabic, system_mode)},
                    {"role": "user", "content": user_q.strip()}
                ]
            )

            for chunk in stream:
                delta = chunk.choices[0].delta

                if delta and getattr(delta, "content", None):
                    full_text += delta.content

                    box.markdown(
                        f'<div class="noor-box"><div class="noor-answer">{full_text}</div></div>',
                        unsafe_allow_html=True
                    )

    except (APIError, RateLimitError, APITimeoutError):
        st.warning("Temporary issue contacting Noor. Please try again.")

# footer verse
featured = [
    "Qur’an 39:23 — skins shiver, then hearts soften to remembrance.",
    "Qur’an 22:46 — hearts may be blind though eyes see.",
    "Qur’an 53:32 — do not declare yourselves pure.",
    "Qur’an 6:59 — with Him are the keys of the unseen."
]

st.markdown(
    f'<div style="margin-top:26px;color:#C0C0C0;text-align:center;font-size:13px;">{random.choice(featured)}</div>',
    unsafe_allow_html=True
)

