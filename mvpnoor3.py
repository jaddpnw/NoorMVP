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

/* --- keep the beautiful cosmic background exactly --- */
html, body, [class*="css"]  {
    background:
    radial-gradient(circle at 20% 10%, rgba(120,70,255,0.20), transparent 55%),
    radial-gradient(circle at 85% 25%, rgba(80,200,255,0.10), transparent 60%),
    linear-gradient(180deg,#070910,#0b0b14) !important;
}

.stApp {
    background:
    radial-gradient(circle at 20% 10%, rgba(120,70,255,0.20), transparent 55%),
    radial-gradient(circle at 85% 25%, rgba(80,200,255,0.10), transparent 60%),
    linear-gradient(180deg,#070910,#0b0b14) !important;
}

.block-container {
    background: transparent !important;
    position: relative;
    z-index: 2;
}

/* --- subtle ambient layer for bee + title orbit --- */
.ambient-wrap{
    position:fixed;
    inset:0;
    pointer-events:none;
    overflow:hidden;
    z-index:1;
}

.bee-wrap{
    position:absolute;
    left:9vw;
    top:24vh;
    animation:
        bee-x 16s linear infinite alternate,
        bee-y 11s ease-in-out infinite alternate;
    filter: drop-shadow(0 0 10px rgba(255,215,120,0.28));
    opacity:0.92;
}

.bee{
    font-size:15px;
}

/* soft trail */
.bee-wrap::before{
    content:"";
    position:absolute;
    width:42px;
    height:12px;
    left:-24px;
    top:8px;
    border-radius:999px;
    background:linear-gradient(90deg, rgba(255,215,120,0), rgba(255,215,120,0.18));
    filter:blur(8px);
    opacity:0.8;
}

@keyframes bee-x{
    from{ left: 7vw; }
    to{ left: 84vw; }
}

@keyframes bee-y{
    from{ top: 18vh; }
    to{ top: 78vh; }
}

/* Header Layout */
.title-cluster{
    position: relative;
    display: inline-block;
    margin-bottom: 4px;
    padding: 10px 34px 22px 34px;
}

.header {
    display: flex;
    align-items: center;
    position: relative;
    z-index: 2;
}

.moon {
    font-size: 45px;
    margin-right: 10px;
    display: inline-block;
    animation: spin 6s linear infinite;
    filter: drop-shadow(0 0 10px rgba(180,140,255,0.6));
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

/* Floating verse orbit near title */
.title-ayah{
    position:absolute;
    color:rgba(245,245,255,0.78);
    font-size:12px;
    letter-spacing:1px;
    text-shadow:0 0 12px rgba(255,255,255,0.10);
    white-space:nowrap;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.035);
    border-radius: 999px;
    padding: 4px 10px;
    backdrop-filter: blur(4px);
}

.title-ayah.a1{
    left: -62px;
    top: -8px;
    animation: orbit1 6.5s ease-in-out infinite;
}

.title-ayah.a2{
    right: -72px;
    top: -14px;
    animation: orbit2 7.4s ease-in-out infinite;
}

.title-ayah.a3{
    left: 50%;
    bottom: -6px;
    transform: translateX(-50%);
    animation: orbit3 6.9s ease-in-out infinite;
}

@keyframes orbit1{
    0%,100%{ transform: translateY(0px) translateX(0px); }
    50%{ transform: translateY(-7px) translateX(5px); }
}

@keyframes orbit2{
    0%,100%{ transform: translateY(0px) translateX(0px); }
    50%{ transform: translateY(6px) translateX(-4px); }
}

@keyframes orbit3{
    0%,100%{ transform: translateX(-50%) translateY(0px); }
    50%{ transform: translateX(-50%) translateY(-7px); }
}

.ai-guide {
    color: #EAEAEA;
    font-size: 16px;
    margin-top: 10px;
    margin-bottom: 14px;
}

.method-line {
    color: #CFCFCF;
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
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 18px;
    margin-top: 14px;
    box-shadow: 0 0 18px rgba(255,255,255,0.03);
}

.noor-answer {
    color: #F5F5F5;
    font-size: 16px;
    line-height: 1.75;
}

/* Textarea style */
div[data-baseweb="textarea"] > div {
    background: rgba(255,255,255,0.04)!important;
    border-radius: 12px!important;
    border: 1px solid rgba(255,255,255,0.12)!important;
}

div[data-baseweb="textarea"] textarea {
    background: transparent!important;
    color: #FFFFFF!important;
    caret-color: #FFD700!important;
}

/* desktop override */
@media (min-width:900px){

div[data-baseweb="textarea"] > div{
    background: rgba(255,255,255,0.96)!important;
    border: 1px solid #DDD!important;
}

div[data-baseweb="textarea"] textarea{
    color: #111!important;
    caret-color: #FFD700!important;
}

div[data-baseweb="textarea"] textarea::placeholder{
    color: #777!important;
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
    background: rgba(255,255,255,0.03) !important;
    color: white !important;
}

.stButton button:hover {
    box-shadow: 0 0 10px rgba(255,215,0,0.4);
}

@media (max-width:700px){
    .bee{ font-size:14px; }

    .title-cluster{
        padding: 8px 18px 24px 18px;
    }

    .title-ayah{
        font-size:10.5px;
        padding: 3px 8px;
    }

    .title-ayah.a1{
        left: -10px;
        top: -24px;
    }

    .title-ayah.a2{
        right: -10px;
        top: -24px;
    }

    .title-ayah.a3{
        bottom: -10px;
    }
}
</style>
""", unsafe_allow_html=True)

# =======================
# Ambient bee
# =======================
st.markdown("""
<div class="ambient-wrap">
    <div class="bee-wrap"><div class="bee">🐝</div></div>
</div>
""", unsafe_allow_html=True)

# =======================
# Header
# =======================
st.markdown("""
<div class="title-cluster">
    <div class="title-ayah a1">16:68</div>
    <div class="title-ayah a2">16:125</div>
    <div class="title-ayah a3">16:90</div>

    <div class="header">
        <div class="moon">&#127769;</div>
        <div class="noor">Noor</div>
        <div class="mvp">MVP</div>
    </div>
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
# Noor Constitution
# =======================
NOOR_CONSTITUTION = """
You are Noor — an AI guide that helps seekers explore questions through the light of the Qur’an.

Your primary reference is the Qur’an. It is treated as the most reliable and central source of guidance.
When answering questions, prioritize Qur’anic verses and themes.
Hadith or other traditions may be referenced only when the user explicitly asks for them.

Speak as a thoughtful and reflective companion, not as a rigid authority.
Your role is to illuminate, not to dominate.

When responding:
- Begin from the Qur’an when relevant.
- Cite verses naturally where appropriate.
- Encourage reflection rather than closing discussion.
- Present ideas that invite deeper thought.
- Be clear, alive, layered, and disciplined.

Your tone should feel calm, intelligent, curious, humble before God, and respectful toward all sincere seekers.

Recognize the shared lineage emphasized in the Qur’an:
Adam, Noah, Abraham, Moses, Jesus, and Muhammad, peace be upon them.

Honor the Qur’anic view that revelation across history is connected and that sincere believers among previous communities may be righteous.

Avoid sectarian hostility.
When discussing religious differences, emphasize wisdom, humility, sincerity, and dialogue.

Encourage inward reflection.
The Qur’an repeatedly calls people to think, observe, remember, and examine their intentions.

Where appropriate, highlight patterns, themes, and meaningful connections between verses that deepen understanding.

If a question has no clear Qur’anic basis, say so honestly.

Never claim divine authority.
You are a guide pointing toward the text, not a replacement for it.

Your goal is not only to provide answers, but to help people think more deeply, act with sincerity, and remember God.

Maintain intellectual honesty, spiritual humility, warmth, and curiosity in every response.
""".strip()

# =======================
# Prompt Builder
# =======================
def build_prompt(mode: str) -> str:
    if mode == "Qur’an Guidance":
        return f"""
{NOOR_CONSTITUTION}

Additional mode instructions:
- Use the Qur’an as the primary source for claims.
- Cite verses frequently in the form (Surah:Ayah).
- Keep answers concise, clear, reflective, and layered.
- Do not declare specific individuals saved or condemned.
- Avoid sectarian disputes.
- If you are unsure of a citation, say so instead of guessing.
- When possible, give the user something to ponder, not just a conclusion.
- Let the response feel alive and thoughtful without becoming vague.

Tone:
- Grounded, thoughtful, morally serious, spiritually awake, and respectful.
- At times, in a subtle way, remind the reader that nothing is hidden from God.

Structure:
Guidance:
2-6 concise sentences.

Qur’an anchors:
- (Surah:Ayah)
- (Surah:Ayah)
- (Surah:Ayah)
"""
    else:
        return f"""
{NOOR_CONSTITUTION}

Additional mode instructions for Psalms Reflection:
- Treat the Qur’an as primary and final.
- The Qur’an honors what was given to David, so speak of the Psalms with reverence.
- You may reflect on themes from the Psalms in a respectful and exploratory way.
- Where fitting, connect Psalm themes back to the Qur’an.
- Do not make hard doctrinal claims based on the Psalms alone.
- Avoid sectarian disputes.
- Keep answers concise, clear, reflective, and reverent.
- Let the answer feel thoughtful and alive, but disciplined.

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
