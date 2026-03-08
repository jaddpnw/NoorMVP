# -*- coding: utf-8 -*-
import streamlit as st
import os
import random
import time
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
# Styling + Cosmic Background
# =======================

st.markdown("""
<style>

/* cosmic gradient background */

html, body, [class*="css"]  {
background:
radial-gradient(circle at 20% 10%, rgba(120,70,255,0.20), transparent 55%),
radial-gradient(circle at 85% 25%, rgba(80,200,255,0.10), transparent 60%),
linear-gradient(180deg,#070910,#0b0b14) !important;
}

.stApp{
background:transparent;
}

.block-container{
position:relative;
z-index:2;
}

/* ambient layer */

.ambient-wrap{
position:fixed;
inset:0;
pointer-events:none;
z-index:1;
}

/* bee */

.bee-wrap{
position:absolute;
left:10vw;
top:25vh;
animation:beex 14s linear infinite alternate, beey 9s ease-in-out infinite alternate;
}

.bee{
font-size:16px;
opacity:0.9;
filter:drop-shadow(0 0 10px rgba(255,215,120,0.35));
}

/* glow trail */

.bee-wrap::before{
content:"";
position:absolute;
width:40px;
height:12px;
left:-25px;
top:10px;
background:linear-gradient(90deg, rgba(255,215,120,0), rgba(255,215,120,0.25));
filter:blur(7px);
border-radius:999px;
}

/* ayah */

.ayah-wrap{
position:absolute;
left:70vw;
top:65vh;
animation:ayahx 18s linear infinite alternate, ayahy 12s ease-in-out infinite alternate;
}

.ayah{
font-size:12px;
color:rgba(240,240,255,0.7);
text-shadow:0 0 10px rgba(255,255,255,0.15);
}

/* movement */

@keyframes beex{
from{left:8vw;}
to{left:85vw;}
}

@keyframes beey{
from{top:20vh;}
to{top:80vh;}
}

@keyframes ayahx{
from{left:15vw;}
to{left:75vw;}
}

@keyframes ayahy{
from{top:70vh;}
to{top:25vh;}
}

/* header */

.header{
display:flex;
align-items:center;
}

.moon{
font-size:45px;
margin-right:10px;
animation:spin 6s linear infinite;
filter:drop-shadow(0 0 8px rgba(255,215,0,0.6));
}

@keyframes spin{
0%{transform:rotate(0deg);}
100%{transform:rotate(360deg);}
}

.noor{
font-size:48px;
font-weight:bold;
color:white;
}

.mvp{
font-size:48px;
font-weight:bold;
color:#FFD700;
margin-left:4px;
}

.ai-guide{
color:#C0C0C0;
font-size:16px;
margin-top:10px;
margin-bottom:12px;
}

.method-line{
color:#CFCFCF;
font-size:13px;
margin-bottom:6px;
}

.psalms-line{
color:#CFCFCF;
font-size:12px;
font-style:italic;
margin-bottom:12px;
}

/* answer box */

.noor-box{
background:rgba(255,255,255,0.03);
border:1px solid rgba(255,255,255,0.07);
border-radius:14px;
padding:18px;
margin-top:14px;
}

.noor-answer{
color:#F5F5F5;
font-size:16px;
line-height:1.7;
}

/* textarea */

div[data-baseweb="textarea"] > div{
background:rgba(255,255,255,0.04)!important;
border-radius:12px!important;
border:1px solid rgba(255,255,255,0.12)!important;
}

div[data-baseweb="textarea"] textarea{
background:transparent!important;
color:white!important;
caret-color:#FFD700!important;
}

/* desktop */

@media (min-width:900px){

div[data-baseweb="textarea"] > div{
background:#ffffff!important;
border:1px solid #DDD!important;
}

div[data-baseweb="textarea"] textarea{
color:#111!important;
}

}

.stButton button{
border-radius:12px!important;
border:1px solid rgba(255,215,0,0.25)!important;
}

.stButton button:hover{
box-shadow:0 0 10px rgba(255,215,0,0.4);
}

</style>
""", unsafe_allow_html=True)

# =======================
# Ambient bee + ayah
# =======================

st.markdown("""
<div class="ambient-wrap">
<div class="bee-wrap"><div class="bee">🐝</div></div>
<div class="ayah-wrap"><div class="ayah">16:90</div></div>
</div>
""", unsafe_allow_html=True)

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
'<div class="ai-guide"><i>Noor</i> is your <i>AI guide</i>, bringing <b>light</b> to your inquiries through the Qur’an.</div>',
unsafe_allow_html=True
)

# =======================
# API Setup
# =======================

api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY missing.")
    st.stop()

client = OpenAI(api_key=api_key)

# =======================
# Mode
# =======================

mode = st.radio(
"Mode",
["Qur’an Guidance","Psalms Reflection"],
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
# Prompt builder
# =======================

def build_prompt(mode):

    if mode == "Qur’an Guidance":

        return """
You are Noor.

Present the Qur'an clearly and respectfully.

Rules:
Use only Qur'an for claims.
Cite verses frequently (Surah:Ayah).
Keep explanation minimal.
Avoid sectarian disputes.
"""

    else:

        return """
You are Noor.

Reflect on the Psalms through a Qur'an-conscious lens.

Treat the Qur'an as primary and final.
Speak of the Psalms with reverence.
Connect Psalm themes back to Qur'anic guidance when possible.
Keep answers concise.
"""

# =======================
# Input
# =======================

placeholder_prompts=[
"What verse speaks about patience?",
"Where is mercy described most beautifully?",
"What does the Quran say about hardship?",
"What does the Quran say about sincerity?"
]

user_question = st.text_area(
"Ask Noor",
placeholder=random.choice(placeholder_prompts),
height=120
)

# =======================
# Response
# =======================

if st.button("Seek Guidance"):

    if user_question and user_question.strip():

        with st.spinner("Noor is reflecting..."):

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":build_prompt(mode)},
                    {"role":"user","content":user_question.strip()}
                ],
                temperature=0.6
            )

        answer=response.choices[0].message.content

        st.markdown("### Your Guidance:")

        st.markdown(
        f'<div class="noor-box"><div class="noor-answer">{answer}</div></div>',
        unsafe_allow_html=True
        )

# =======================
# Rotating verse
# =======================

featured_verses=[
"Quran 94:5 — With hardship comes ease.",
"Quran 13:28 — In remembrance of Allah do hearts find rest.",
"Quran 2:286 — Allah does not burden a soul beyond what it can bear.",
"Quran 16:90 — Allah commands justice and excellence."
]

if "verse_index" not in st.session_state:
    st.session_state.verse_index=0

if "last_update" not in st.session_state:
    st.session_state.last_update=time.time()

current_time=time.time()

if current_time - st.session_state.last_update > 9:

    st.session_state.verse_index=(st.session_state.verse_index+1)%len(featured_verses)
    st.session_state.last_update=current_time

st.markdown(
f'<div class="rotating-verse">{featured_verses[st.session_state.verse_index]}</div>',
unsafe_allow_html=True
)
