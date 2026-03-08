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

/* --- subtle ambient layer for bee + hovering verses --- */
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

/* soft trail restored */
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

/* three hovering verse refs near header zone */
.ayah-a,
.ayah-b,
.ayah-c{
    position:absolute;
    color:rgba(245,245,255,0.72);
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

.ayah-a{
    left: 10vw;
    top: 12vh;
    animation:
        ayah-a-x 14s linear infinite alternate,
        ayah-a-y 9s ease-in-out infinite alternate;
}

.ayah-b{
    left: 66vw;
    top: 11vh;
    animation:
        ayah-b-x 16s linear infinite alternate,
        ayah-b-y 10s ease-in-out infinite alternate;
}

.ayah-c{
    left: 39vw;
    top: 33vh;
    animation:
        ayah-c-x 13s linear infinite alternate,
        ayah-c-y 8s ease-in-out infinite alternate;
}

@keyframes bee-x{
    from{ left: 7vw; }
    to{ left: 84vw; }
}

@keyframes bee-y{
    from{ top: 18vh; }
    to{ top: 78vh; }
}

@keyframes ayah-a-x{
    from{ left: 6vw; }
    to{ left: 16vw; }
}

@keyframes ayah-a-y{
    from{ top: 11vh; }
    to{ top: 16vh; }
}

@keyframes ayah-b-x{
    from{ left: 62vw; }
    to{ left: 74vw; }
}

@keyframes ayah-b-y{
    from{ top: 10vh; }
    to{ top: 15vh; }
}

@keyframes ayah-c-x{
    from{ left: 34vw; }
    to{ left: 46vw; }
}

@keyframes ayah-c-y{
    from{ top: 30vh; }
    to{ top: 37vh; }
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
    margin-bottom: 6px;
    font-style: italic;
}

.psalms-footnote {
    color: #BDBDBD;
    font-size: 11.8px;
    margin-top: 0px;
    margin-bottom: 14px;
    line-height: 1.5;
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

.noor-answer h4, .noor-answer h5 {
    margin-bottom: 6px;
}

.noor-answer p {
    margin-bottom: 10px;
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
    .ayah-a, .ayah-b, .ayah-c{
        font-size:11px;
        padding: 3px 8px;
    }

    .ayah-a{
        left: 8vw;
        top: 11vh;
    }

    .ayah-b{
        left: 62vw;
        top: 10vh;
    }

    .ayah-c{
        left: 34vw;
        top: 28vh;
    }

    @keyframes ayah-a-x{
        from{ left: 6vw; }
        to{ left: 14vw; }
    }

    @keyframes ayah-a-y{
        from{ top: 10vh; }
        to{ top: 14vh; }
    }

    @keyframes ayah-b-x{
        from{ left: 58vw; }
        to{ left: 70vw; }
    }

    @keyframes ayah-b-y{
        from{ top: 9vh; }
        to{ top: 13vh; }
    }

    @keyframes ayah-c-x{
        from{ left: 30vw; }
        to{ left: 42vw; }
    }

    @keyframes ayah-c-y{
        from{ top: 26vh; }
        to{ top: 32vh; }
    }
}
</style>
""", unsafe_allow_html=True)

# =======================
# Ambient bee + hovering verses
# =======================
st.markdown("""
<div class="ambient-wrap">
    <div class="bee-wrap"><div class="bee">🐝</div></div>
    <div class="ayah-a">16:68</div>
    <div class="ayah-b">16:125</div>
    <div class="ayah-c">16:90</div>
</div>
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
- Help the user form better, deeper, and more reflective questions when appropriate.

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
# Shared theme library
# =======================
THEME_LIBRARY = {
    "trust": {
        "keywords": [
            "trust", "fear", "worry", "anxious", "anxiety",
            "unsafe", "uncertain", "burden", "rest"
        ],
        "quran_refs": ["13:28", "94:5-6", "3:173"],
        "psalm_refs": ["Psalm 23:1-3", "Psalm 27:1", "Psalm 46:1-2"],
    },
    "mercy": {
        "keywords": [
            "mercy", "forgiveness", "repent", "repentance",
            "despair", "shame", "guilt", "hope"
        ],
        "quran_refs": ["39:53", "7:156", "25:70"],
        "psalm_refs": ["Psalm 103:8-10", "Psalm 51:1-2", "Psalm 130:3-4"],
    },
    "guidance": {
        "keywords": [
            "guidance", "direction", "lost", "path",
            "clarity", "confused", "begin", "way"
        ],
        "quran_refs": ["1:5-6", "17:9", "2:2"],
        "psalm_refs": ["Psalm 119:105", "Psalm 25:4-5", "Psalm 143:8"],
    },
    "patience": {
        "keywords": [
            "patience", "waiting", "delay", "endure",
            "endurance", "trial", "sabr", "steadfast"
        ],
        "quran_refs": ["2:153", "3:200", "94:5-6"],
        "psalm_refs": ["Psalm 27:14", "Psalm 37:7", "Psalm 40:1"],
    },
    "awe": {
        "keywords": [
            "creation", "sky", "heavens", "nature", "signs",
            "wonder", "beauty", "universe", "stars"
        ],
        "quran_refs": ["67:3-4", "16:68-69", "3:190-191"],
        "psalm_refs": ["Psalm 19:1-2", "Psalm 8:3-4", "Psalm 104:24"],
    },
    "gratitude": {
        "keywords": [
            "gratitude", "thankful", "thanks", "blessing",
            "blessings", "praise", "remember"
        ],
        "quran_refs": ["14:7", "55:13", "2:152"],
        "psalm_refs": ["Psalm 100:1-5", "Psalm 103:1-5", "Psalm 145:1-3"],
    },
    "heaviness": {
        "keywords": [
            "heavy", "sad", "tired", "grief", "pain",
            "overwhelmed", "hurt", "weak", "lonely"
        ],
        "quran_refs": ["94:1-6", "2:286", "13:28"],
        "psalm_refs": ["Psalm 34:18", "Psalm 42:11", "Psalm 147:3"],
    },
    "return": {
        "keywords": [
            "return", "come back", "far from god", "distance",
            "soften", "heart", "renew", "wake up"
        ],
        "quran_refs": ["39:53", "57:16", "11:90"],
        "psalm_refs": ["Psalm 51:10", "Psalm 63:1", "Psalm 143:10"],
    },
}

# =======================
# Starting Point clusters
# =======================
STARTING_POINTS = [
    {
        "theme": "trust",
        "keywords": ["trust", "fear", "worry", "anxious", "anxiety", "unsafe", "uncertain", "burden", "heavy"],
        "intro": "Here is a place to begin reflecting today.",
        "psalm_ref": "Psalm 23:1–3",
        "psalm_text": (
            "The Lord is my shepherd; I shall not want. "
            "He maketh me to lie down in green pastures: he leadeth me beside the still waters. "
            "He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake."
        ),
        "quran_ref_1": "Qur’an 13:28",
        "quran_text_1": (
            "Surely, in the remembrance of Allah do hearts find rest."
        ),
        "quran_ref_2": "Qur’an 94:5–6",
        "quran_text_2": (
            "So truly, with hardship comes ease. Truly, with hardship comes ease."
        ),
        "closing": "You might sit with these passages for a moment, or ask Noor how they speak to one another."
    },
    {
        "theme": "mercy",
        "keywords": ["mercy", "forgiveness", "repent", "despair", "shame", "return", "guilt", "hope"],
        "intro": "Here is a place to begin reflecting today.",
        "psalm_ref": "Psalm 103:8–10",
        "psalm_text": (
            "The Lord is merciful and gracious, slow to anger, and plenteous in mercy. "
            "He will not always chide: neither will he keep his anger for ever. "
            "He hath not dealt with us after our sins; nor rewarded us according to our iniquities."
        ),
        "quran_ref_1": "Qur’an 39:53",
        "quran_text_1": (
            "Say: O My servants who have wronged themselves, do not despair of the mercy of Allah. "
            "Indeed, Allah forgives all sins. Indeed, He is the Most Forgiving, the Most Merciful."
        ),
        "quran_ref_2": "Qur’an 7:156",
        "quran_text_2": (
            "My mercy encompasses all things."
        ),
        "closing": "You may also ask Noor what these passages reveal about returning to God without despair."
    },
    {
        "theme": "creation",
        "keywords": ["creation", "sky", "heavens", "nature", "signs", "wonder", "beauty", "universe"],
        "intro": "Here is a place to begin reflecting today.",
        "psalm_ref": "Psalm 19:1–2",
        "psalm_text": (
            "The heavens declare the glory of God; and the firmament sheweth his handiwork. "
            "Day unto day uttereth speech, and night unto night sheweth knowledge."
        ),
        "quran_ref_1": "Qur’an 67:3–4",
        "quran_text_1": (
            "He who created seven heavens in layers. You do not see any inconsistency in the creation of the Most Merciful. "
            "So return your vision: do you see any breaks? Then return your vision twice again; your vision will return to you humbled and weary."
        ),
        "quran_ref_2": "Qur’an 16:68–69",
        "quran_text_2": (
            "And your Lord inspired the bee: Take for yourself among the mountains houses, and among the trees and what they build. "
            "Then eat from all fruits and follow the ways of your Lord laid down for you. "
            "From within them comes a drink of varying colors, in which there is healing for people. "
            "Indeed, in that is a sign for people who reflect."
        ),
        "closing": "You might also ask Noor how creation becomes a form of remembrance in these passages."
    },
    {
        "theme": "guidance",
        "keywords": ["guidance", "direction", "lost", "begin", "path", "clarity", "confused"],
        "intro": "Here is a place to begin reflecting today.",
        "psalm_ref": "Psalm 119:105",
        "psalm_text": (
            "Thy word is a lamp unto my feet, and a light unto my path."
        ),
        "quran_ref_1": "Qur’an 1:5–6",
        "quran_text_1": (
            "You alone we worship, and You alone we ask for help. Guide us to the straight path."
        ),
        "quran_ref_2": "Qur’an 17:9",
        "quran_text_2": (
            "Indeed, this Qur’an guides to that which is most upright."
        ),
        "closing": "You might ask Noor what kind of guidance these passages are pointing you toward right now."
    },
    {
        "theme": "patience",
        "keywords": ["patience", "waiting", "delay", "endure", "endurance", "trial", "sabr"],
        "intro": "Here is a place to begin reflecting today.",
        "psalm_ref": "Psalm 27:14",
        "psalm_text": (
            "Wait on the Lord: be of good courage, and he shall strengthen thine heart: wait, I say, on the Lord."
        ),
        "quran_ref_1": "Qur’an 2:153",
        "quran_text_1": (
            "O you who believe, seek help through patience and prayer. Indeed, Allah is with the patient."
        ),
        "quran_ref_2": "Qur’an 3:200",
        "quran_text_2": (
            "O you who believe, be steadfast, outdo one another in steadfastness, remain firm, and be mindful of Allah so that you may succeed."
        ),
        "closing": "You might sit with the kind of strength these passages call for, and ask Noor where patience meets trust."
    },
]

THEME_TO_CLUSTER = {
    "trust": "trust",
    "mercy": "mercy",
    "guidance": "guidance",
    "patience": "patience",
    "awe": "creation",
    "gratitude": "mercy",
    "heaviness": "trust",
    "return": "mercy",
}

# =======================
# Helpers
# =======================
def detect_theme(user_text: str):
    text = (user_text or "").strip().lower()
    if not text:
        return None

    best_theme = None
    best_score = 0

    for theme_name, theme_data in THEME_LIBRARY.items():
        score = sum(1 for keyword in theme_data["keywords"] if keyword in text)
        if score > best_score:
            best_score = score
            best_theme = theme_name

    return best_theme if best_score > 0 else None

def build_theme_hint(user_text: str) -> str:
    theme = detect_theme(user_text)
    if not theme:
        return ""

    return f"""
Likely theme or user need: {theme}.
If fitting, let this gently inform verse selection, pairing, and tone without forcing the response or overriding the user's actual question.
""".strip()

def choose_starting_point(user_text: str):
    text = (user_text or "").strip().lower()

    # First try cluster-native keyword matching
    if text:
        for cluster in STARTING_POINTS:
            if any(keyword in text for keyword in cluster["keywords"]):
                return cluster

    # Then use shared theme library as a quiet supplement
    theme = detect_theme(text)
    if theme:
        cluster_theme = THEME_TO_CLUSTER.get(theme)
        if cluster_theme:
            for cluster in STARTING_POINTS:
                if cluster["theme"] == cluster_theme:
                    return cluster

    return random.choice(STARTING_POINTS)

def render_starting_point(cluster: dict) -> str:
    return f"""
<h4>{cluster["intro"]}</h4>

<p><b>{cluster["psalm_ref"]}</b><br>
{cluster["psalm_text"]}</p>

<p><b>{cluster["quran_ref_1"]}</b><br>
{cluster["quran_text_1"]}</p>

<p><b>{cluster["quran_ref_2"]}</b><br>
{cluster["quran_text_2"]}</p>

<p><i>{cluster["closing"]}</i></p>
""".strip()

# =======================
# Prompt Builder
# =======================
def build_prompt(mode: str, user_text: str = "") -> str:
    theme_hint = build_theme_hint(user_text)

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
- When suggesting a verse or passage, lay out the full verse text or clear rendered meaning before explaining it.
- Let any thematic sensitivity remain subtle and supportive rather than dominant.

{theme_hint}

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
    elif mode == "Psalms Reflection":
        return f"""
{NOOR_CONSTITUTION}

Additional mode instructions for Psalms Reflection:
- Treat the Qur’an as primary and final.
- The Qur’an honors what was given to David, so Noor does as well.
- You may reflect on themes from the Psalms in a respectful and exploratory way.
- Where fitting, connect Psalm themes back to the Qur’an.
- Do not make hard doctrinal claims based on the Psalms alone.
- Avoid sectarian disputes.
- Keep answers concise, clear, reflective, and reverent.
- Let the answer feel thoughtful and alive, but disciplined.
- When recommending or discussing passages, always lay out the full Psalm passage and the full Qur’anic passage text or clear rendered meaning before the reflection.
- Encourage the user to notice sincere praise, trust, repentance, remembrance, and devotion to God.
- When it helps the user, suggest a Psalm and a Qur’anic passage to read side by side.
- Let thematic sensitivity quietly guide pairing choices where fitting, without turning the response into a rigid theme match.

{theme_hint}

Tone:
- Gentle, reverent, morally awake, and respectful.

Structure:
Guidance:
2-5 concise sentences.

Passages to reflect on:
- Full Psalm passage
- Full Qur’anic passage

Qur’anic resonance:
- (Surah:Ayah)
- (Surah:Ayah)

Closing:
- One gentle question or one suggested next question the user could ask.
"""
    else:
        return f"""
{NOOR_CONSTITUTION}

Additional mode instructions for Starting Point:
- Offer one Psalm passage, one Qur’anic passage, and one additional Qur’anic passage.
- Lay out the full passage text or clear rendered meaning for each before any reflection.
- Keep the response warm, calm, and invitational.
- Begin with: Here is a place to begin reflecting today.
- End with one gentle sentence inviting further reflection or a follow-up question.

{theme_hint}
"""

# =======================
# Mode selector
# =======================
mode = st.radio(
    "Mode",
    ["Qur’an Guidance", "Psalms Reflection", "Starting Point"],
    horizontal=True
)

if mode == "Qur’an Guidance":
    st.markdown(
        '<div class="method-line">Noor cites its claims with Qur’anic evidence.</div>',
        unsafe_allow_html=True
    )
elif mode == "Psalms Reflection":
    st.markdown(
        '<div class="method-line">Noor explores the Psalms with reverence through a Qur’an-conscious lens.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="psalms-line">The Qur’an honors what was given to David, so Noor does as well. (4:163, 17:55, 21:105)</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="psalms-footnote">Noor reflects on the Psalms because the Qur’an affirms the Zabur given to David, while the Qur’an remains the primary criterion.</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="method-line">Starting Point offers one Psalm and two Qur’anic passages to help you begin reflecting, even if you do not know what to ask yet.</div>',
        unsafe_allow_html=True
    )

# =======================
# Placeholder Prompts
# =======================
if mode == "Qur’an Guidance":
    placeholder_prompts = [
        "Give me a verse to reflect on today.",
        "What is a verse that might help me see myself more clearly?",
        "What should I read when my heart feels heavy?",
        "What is a good verse to carry with me today?",
    ]
elif mode == "Psalms Reflection":
    placeholder_prompts = [
        "Give me a Psalm and a Qur’anic verse to reflect on today.",
        "What Psalm should I carry in my heart today with the Qur’an?",
        "Show me a Psalm and a verse that speak to trust in God.",
        "Give me something beautiful from the Psalms and Qur’an to sit with.",
    ]
else:
    placeholder_prompts = [
        "Leave this blank, or write a word like mercy, trust, patience, or guidance.",
        "You can simply press the button and Noor will offer a place to begin.",
        "Try a word like fear, hope, repentance, or gratitude.",
        "Or just let Noor choose a place to begin reflecting today.",
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
    try:
        if mode == "Starting Point":
            cluster = choose_starting_point(user_question)
            answer = render_starting_point(cluster)

            st.markdown("### Your Guidance:")
            st.markdown(
                f'<div class="noor-box"><div class="noor-answer">{answer}</div></div>',
                unsafe_allow_html=True
            )

        elif user_question and user_question.strip():
            with st.spinner("Noor is reflecting..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": build_prompt(mode, user_question.strip())
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

        else:
            st.warning("Please enter a question, or choose Starting Point to begin without one.")

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
