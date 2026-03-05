# -*- coding: utf-8 -*-
import os
import json
import time
import random
from typing import List, Dict, Tuple, Optional

import numpy as np
import streamlit as st
from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =======================
# Page config
# =======================
st.set_page_config(
    page_title="NoorMVP",
    page_icon="🌙",
    layout="centered",
)

# =======================
# Styling (readable on desktop)
# =======================
st.markdown("""
<style>
html, body { background-color: #0a0a0f !important; }
.stApp, .block-container { background-color: #0a0a0f !important; }

/* Header Layout */
.header { display: flex; align-items: center; }
.moon {
    font-size: 45px; margin-right: 10px; display: inline-block;
    animation: spin 6s linear infinite;
    filter: drop-shadow(0 0 8px rgba(255, 215, 0, 0.75));
}
@keyframes spin { 0% { transform: rotate(0deg);} 100% { transform: rotate(360deg);} }

.noor { font-size: 48px; font-weight: bold; color: white; }
.mvp  { font-size: 48px; font-weight: bold; color: #FFD700; margin-left: 4px; }

.ai-guide { color: #D0D0D0; font-size: 16px; margin-top: 10px; margin-bottom: 12px; }

.small-note { color: #9a9a9a; font-size: 12px; margin-top: 6px; margin-bottom: 10px; }

/* Answer box + brighter answer text */
.noor-box {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 18px 18px;
    margin-top: 10px;
}
.noor-answer {
    color: #F5F5F5;
    font-size: 16px;
    line-height: 1.7;
}
.noor-box p, .noor-box li, .noor-box span, .noor-box div, .noor-box h1, .noor-box h2, .noor-box h3, .noor-box h4 {
    color: #F5F5F5 !important;
}

/* Buttons feel premium */
.stButton button:hover {
    box-shadow: 0 0 10px rgba(255,215,0,0.45);
}

/* Feature widgets */
.feature-row {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 10px 12px;
    margin: 8px 0 10px 0;
}
.feature-title { color: #F0F0F0; font-size: 13px; font-weight: 600; margin-bottom: 6px; }
.feature-sub { color: #BEBEBE; font-size: 12px; line-height: 1.4; }

/* Featured verse */
.featured-verse { color: #C0C0C0; font-size: 13px; margin-top: 26px; text-align: center; }
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
    '<div class="ai-guide">Exploring the Qur’an as a clear and universal guide to <b>God (Allah)</b>.</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="small-note">Qur’an-first: Noor retrieves relevant verses first, cites them, and labels reflections clearly.</div>',
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
# Qur'an dataset + retrieval
# =======================
DATA_PATH = "data/quran_en.json"

@st.cache_resource
def load_quran_and_index() -> Tuple[List[Dict], TfidfVectorizer, np.ndarray]:
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Missing {DATA_PATH}. Create it with Qur'an verses as JSON objects, e.g. "
            f'{{"surah":1,"ayah":1,"text":"..."}}'
        )

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        verses = json.load(f)

    texts = [v["text"] for v in verses]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95,
    )
    matrix = vectorizer.fit_transform(texts)
    return verses, vectorizer, matrix

def retrieve_verses(query: str, top_k: int = 6) -> List[Dict]:
    verses, vectorizer, matrix = load_quran_and_index()
    q_vec = vectorizer.transform([query])
    sims = cosine_similarity(q_vec, matrix).flatten()
    top_idx = np.argsort(sims)[::-1][:top_k]
    results = []
    for i in top_idx:
        v = verses[int(i)]
        score = float(sims[int(i)])
        if score <= 0:
            continue
        results.append({**v, "score": score})
    return results

def get_surrounding(verses: List[Dict], surah: int, ayah: int, window: int = 2) -> List[Dict]:
    out = []
    for v in verses:
        if v["surah"] == surah and (ayah - window) <= v["ayah"] <= (ayah + window):
            out.append(v)
    out.sort(key=lambda x: x["ayah"])
    return out

# =======================
# Session state
# =======================
if "history" not in st.session_state:
    st.session_state.history = []

if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""

if "last_retrieved" not in st.session_state:
    st.session_state.last_retrieved = []

if "followups" not in st.session_state:
    st.session_state.followups = []

if "quiet_reflection" not in st.session_state:
    st.session_state.quiet_reflection = False

if "clarifier" not in st.session_state:
    st.session_state.clarifier = ""

# =======================
# Placeholder prompts
# =======================
placeholder_prompts = [
    "What does the Qur’an say about patience?",
    "Where does the Qur’an describe mercy most beautifully?",
    "What does the Qur’an say about hardship and ease?",
    "What does the Qur’an say about anxiety or fear?",
    "How does the Qur’an describe sincerity?",
]

# =======================
# Lightweight helpers
# =======================
BROAD_MARKERS = [
    "life", "meaning", "everything", "help", "guidance", "hard", "hardship", "sad", "depressed",
    "anxious", "fear", "lost", "confused", "purpose", "relationships", "marriage", "money", "work"
]

def maybe_make_clarifying_question(user_q: str) -> str:
    q = user_q.lower().strip()
    if len(q) < 18:
        return ""
    # If it looks very broad or contains broad markers, offer a non-blocking clarifier.
    broad = any(w in q for w in BROAD_MARKERS) or q.endswith("?") and len(q.split()) <= 5
    if broad:
        return "Before I answer—are you seeking clarity, comfort, direction, or correction?"
    return ""

# =======================
# Controls (kept clean)
# =======================
colA, colB, colC = st.columns([1, 1, 1])
with colA:
    mode = st.selectbox("Mode", ["Guidance", "Study"], index=0)
with colB:
    concise = st.checkbox("Concise answer", value=True)
with colC:
    top_k = st.selectbox("Verses", options=[4, 6, 8, 10], index=1)

# =======================
# Feature row (non-invasive, optional)
# =======================
st.markdown("""
<div class="feature-row">
  <div class="feature-title">Optional: Open-heart features</div>
  <div class="feature-sub">
    Guidance mode offers a gentle one-line orientation and reflection prompts.
    Study mode stays more text-forward and analytical.
  </div>
</div>
""", unsafe_allow_html=True)

# =======================
# Input (form)
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
# System prompt
# =======================
def build_system_prompt(concise: bool, mode: str) -> str:
    orientation_rule = ""
    if mode == "Guidance":
        orientation_rule = """
Perception & intent (feature):
- Begin with ONE short line that either (a) clarifies intent (clarity/comfort/direction/correction) or (b) gently reframes the question.
- Keep it universal, grounded, and non-mystical.
"""
    return f"""
You are Noor, a Qur’an-first AI guide.

Non-negotiable rules:
- Use ONLY the Qur’an for religious/factual claims. Do not use hadith, scholars, or jurisprudence unless the user explicitly asks.
- Always cite verse references as (Surah:Ayah), e.g., (2:286).
- If something is not explicit in the Qur’an, say: "The Qur’an does not state this explicitly," then offer the closest Qur’anic themes with citations.
- Be grounded, inclusive, respectful, and clear.
- Use accessible language. Refer to Allah as "God (Allah)" at least once when relevant.
{orientation_rule}

Output format (markdown):
{"0) **One-line orientation**" if mode == "Guidance" else ""}
1) **Relevant verses** (bullet list: short quote or paraphrase + citation)
2) **Core meaning**
3) **Practical reflection**
4) **If you want to go deeper** (2–4 suggested angles)

Style:
{"- Be concise, clean, and avoid rambling." if concise else "- Be thorough but still readable. Keep sections tight."}
""".strip()

# =======================
# Follow-up generation (cached)
# =======================
@st.cache_data(ttl=3600)
def generate_followups(question: str, verse_refs: str) -> List[str]:
    prompt = f"""
Generate 3 short, compelling follow-up questions (max 12 words each).
They should extend the user's question using Qur'anic themes.
No numbering. No quotes. Plain lines only.

User question:
{question}

Verse refs:
{verse_refs}
""".strip()

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.5,
        messages=[
            {"role": "system", "content": "You write concise follow-up questions."},
            {"role": "user", "content": prompt},
        ],
    )
    lines = [ln.strip("-• \t") for ln in resp.choices[0].message.content.splitlines() if ln.strip()]
    cleaned = []
    for ln in lines:
        if len(cleaned) >= 3:
            break
        if 2 <= len(ln) <= 80:
            cleaned.append(ln)
    return cleaned[:3]

# =======================
# Quiet reflection feature (purely optional)
# =======================
def render_quiet_reflection():
    st.markdown("""
<div class="noor-box">
  <div class="noor-answer">
    <b>Quiet Reflection (10 seconds)</b><br><br>
    • Take one breath.<br>
    • Ask: “What is God (Allah) inviting me to notice?”<br>
    • Then read one cited verse again—slowly.<br>
  </div>
</div>
""", unsafe_allow_html=True)

# =======================
# Main pipeline: retrieve -> answer (stream)
# =======================
if submitted:
    q = (user_question or "").strip()
    if not q:
        st.stop()

    # Non-blocking clarifier (stored for display; does not halt answers)
    st.session_state.clarifier = maybe_make_clarifying_question(q) if mode == "Guidance" else ""

    retrieved = retrieve_verses(q, top_k=top_k)

    if not retrieved:
        st.warning("Noor couldn’t confidently retrieve relevant verses from the local dataset. Try rephrasing.")
        st.stop()

    verse_context_lines = [f'{v["surah"]}:{v["ayah"]} — {v["text"]}' for v in retrieved]
    verse_context = "\n".join(verse_context_lines)

    st.session_state.last_retrieved = retrieved

    # Keep light history
    st.session_state.history.append({"role": "user", "content": q})
    st.session_state.history = st.session_state.history[-8:]

    system_prompt = build_system_prompt(concise=concise, mode=mode)

    user_prompt = f"""
User question:
{q}

You MUST ground your answer in these retrieved Qur'an verses:
{verse_context}
""".strip()

    st.markdown("### Your Guidance:")
    box = st.empty()
    full_text = ""

    with st.spinner("Noor is reflecting..."):
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.6,
            stream=True,
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.history[-6:],
                {"role": "user", "content": user_prompt},
            ],
        )

        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and getattr(delta, "content", None):
                full_text += delta.content
                box.markdown(
                    f'<div class="noor-box"><div class="noor-answer">{full_text}</div></div>',
                    unsafe_allow_html=True
                )

    st.session_state.last_answer = full_text
    st.session_state.history.append({"role": "assistant", "content": full_text})
    st.session_state.history = st.session_state.history[-8:]

    try:
        refs = "\n".join([f'{v["surah"]}:{v["ayah"]}' for v in retrieved[:6]])
        st.session_state.followups = generate_followups(q, refs)
    except Exception:
        st.session_state.followups = []

# =======================
# Post-answer features (optional)
# =======================
if st.session_state.last_answer and st.session_state.last_retrieved:
    # Guidance-mode gentle clarifier (non-blocking)
    if st.session_state.clarifier:
        st.markdown(
            f'<div class="small-note">{st.session_state.clarifier}</div>',
            unsafe_allow_html=True
        )

    # Quiet Reflection toggle button (does not affect answer flow)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Quiet Reflection (10s)"):
            st.session_state.quiet_reflection = not st.session_state.quiet_reflection
    with col2:
        if st.button("Clear"):
            st.session_state.noor_input = ""
            st.session_state.last_answer = ""
            st.session_state.last_retrieved = []
            st.session_state.followups = []
            st.session_state.quiet_reflection = False
            st.session_state.clarifier = ""
            st.rerun()

    if st.session_state.quiet_reflection:
        render_quiet_reflection()

    # Follow-up buttons (keeps engagement)
    if st.session_state.followups:
        st.markdown("### Explore further")
        cols = st.columns(3)
        for i, fu in enumerate(st.session_state.followups[:3]):
            with cols[i]:
                if st.button(fu, key=f"fu_{i}"):
                    st.session_state.noor_input = fu
                    st.rerun()

    with st.expander("Show retrieved verses (what Noor used)"):
        for v in st.session_state.last_retrieved:
            st.markdown(f"**({v['surah']}:{v['ayah']})** — {v['text']}")

    with st.expander("Show surrounding verses (context window)"):
        verses_all, _, _ = load_quran_and_index()
        for v in st.session_state.last_retrieved[:2]:
            s, a = int(v["surah"]), int(v["ayah"])
            around = get_surrounding(verses_all, s, a, window=2)
            st.markdown(f"**Context around ({s}:{a})**")
            for x in around:
                st.markdown(f"- **({x['surah']}:{x['ayah']})** — {x['text']}")
            st.divider()

# =======================
# Featured verse (rotates per interaction)
# =======================
featured_verses = [
    "Qur’an 94:5 — With hardship comes ease.",
    "Qur’an 13:28 — In remembrance of God (Allah) do hearts find rest.",
    "Qur’an 2:286 — God (Allah) does not burden a soul beyond what it can bear.",
    "Qur’an 16:90 — God (Allah) commands justice and excellence.",
    "Qur’an 39:53 — Do not despair of the mercy of God (Allah).",
]

if "verse_index" not in st.session_state:
    st.session_state.verse_index = 0
st.session_state.verse_index = (st.session_state.verse_index + 1) % len(featured_verses)

st.markdown(
    f'<div class="featured-verse">{featured_verses[st.session_state.verse_index]}</div>',
    unsafe_allow_html=True
)
