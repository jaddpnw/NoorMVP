# -*- coding: utf-8 -*-
import os
import json
import time
import random
from typing import List, Dict, Tuple

import numpy as np
import streamlit as st
from openai import OpenAI
from openai import APIError, RateLimitError, APITimeoutError
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
# Styling (IMPORTANT: keep this as ONE triple-quoted string)
# =======================
CSS = """
<style>
html, body { background-color: #0a0a0f !important; }
.stApp, .block-container { background-color: #0a0a0f !important; }

/* Header Layout */
.header { display: flex; align-items: center; }
.moon {
    font-size: 45px; margin-right: 10px; display: inline-block;
    animation: spin 6s linear infinite;
    filter: drop-shadow(0 0 8px rgba(255, 215, 0, 0.70));
}
@keyframes spin { 0% { transform: rotate(0deg);} 100% { transform: rotate(360deg);} }

.noor { font-size: 48px; font-weight: bold; color: #FFFFFF; }
.mvp  { font-size: 48px; font-weight: bold; color: #FFD700; margin-left: 4px; }

.ai-guide { color: #E3E3E3; font-size: 16px; margin-top: 10px; margin-bottom: 8px; }
.small-note { color: #B5B5B5; font-size: 12px; margin-top: 4px; margin-bottom: 10px; }

/* Answer box + softer bright text */
.noor-box {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 18px 18px;
    margin-top: 10px;
}
.noor-answer {
    color: #EAEAEA;
    font-size: 16px;
    line-height: 1.75;
}
.noor-box p, .noor-box li, .noor-box span, .noor-box div, .noor-box h1, .noor-box h2, .noor-box h3, .noor-box h4 {
    color: #EAEAEA !important;
}

/* Premium input feel */
textarea {
  background: rgba(255,255,255,0.03) !important;
  color: #F2F2F2 !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 12px !important;
}
textarea:focus {
  outline: none !important;
  border: 1px solid rgba(255,215,0,0.32) !important;
  box-shadow: 0 0 12px rgba(255,215,0,0.16) !important;
}

/* Button polish */
.stButton button {
  border-radius: 12px !important;
  border: 1px solid rgba(255,215,0,0.22) !important;
}
.stButton button:hover {
    box-shadow: 0 0 10px rgba(255,215,0,0.40);
}
.stButton button:active {
  transform: translateY(1px);
}

/* Mode row */
.mode-row {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 10px 12px;
    margin: 8px 0 10px 0;
}
.mode-sub { color: #BEBEBE; font-size: 12px; line-height: 1.4; }

/* Featured verse */
.featured-verse { color: #C0C0C0; font-size: 13px; margin-top: 26px; text-align: center; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

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
    '<div class="ai-guide">The Qur’an is purposely simple—clearer than the interpretations often associated with it.</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="small-note">Ask Noor anything about the Qur’an. You are safe to explore.</div>',
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
DEFAULT_TOP_K = 6  # fixed to avoid UI clutter

@st.cache_resource
def load_quran_and_index() -> Tuple[List[Dict], TfidfVectorizer, np.ndarray]:
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Missing {DATA_PATH}. You need: data/quran_en.json"
        )

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        verses = json.load(f)

    if not isinstance(verses, list) or not verses:
        raise ValueError(f"{DATA_PATH} must be a non-empty JSON list.")

    for i, v in enumerate(verses[:100]):
        if not isinstance(v, dict) or not all(k in v for k in ("surah", "ayah", "text")):
            raise ValueError(f"Verse at index {i} missing keys: surah, ayah, text")

    texts = [v["text"] for v in verses]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95,
    )
    matrix = vectorizer.fit_transform(texts)
    return verses, vectorizer, matrix

def retrieve_verses(query: str, top_k: int = DEFAULT_TOP_K) -> List[Dict]:
    verses, vectorizer, matrix = load_quran_and_index()
    q_vec = vectorizer.transform([query])
    sims = cosine_similarity(q_vec, matrix).flatten()
    top_idx = np.argsort(sims)[::-1][:top_k]
    results = []
    for i in top_idx:
        score = float(sims[int(i)])
        if score <= 0:
            continue
        v = verses[int(i)]
        results.append({**v, "score": score})
    return results

def get_surrounding(verses: List[Dict], surah: int, ayah: int, window: int = 2) -> List[Dict]:
    out = []
    for v in verses:
        if int(v["surah"]) == int(surah) and (ayah - window) <= int(v["ayah"]) <= (ayah + window):
            out.append(v)
    out.sort(key=lambda x: int(x["ayah"]))
    return out

def clip(text: str, n: int = 360) -> str:
    text = (text or "").strip()
    return text if len(text) <= n else text[:n].rstrip() + "…"

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
# Broadness heuristic (non-blocking)
# =======================
BROAD_MARKERS = [
    "life", "meaning", "everything", "help", "guidance", "hard", "hardship", "sad",
    "depressed", "anxious", "fear", "lost", "confused", "purpose", "relationships",
    "marriage", "money", "work"
]

def maybe_make_clarifying_question(user_q: str) -> str:
    q = (user_q or "").lower().strip()
    if len(q) < 18:
        return ""
    broad = any(w in q for w in BROAD_MARKERS) or (q.endswith("?") and len(q.split()) <= 5)
    if broad:
        return "Before I answer—are you seeking clarity, comfort, direction, or correction?"
    return ""

# =======================
# Controls (keep concise checkbox)
# =======================
colA, colB = st.columns([1.0, 1.0])
with colA:
    mode = st.selectbox("Mode", ["Guidance", "Study"], index=0)
with colB:
    concise = st.checkbox("Concise answer", value=True)

st.markdown("""
<div class="mode-row">
  <div class="mode-sub">
    Guidance mode offers gentle reflection. Study mode focuses more directly on the text.
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
# Prompt builder
# =======================
def build_system_prompt(concise_flag: bool, mode_value: str) -> str:
    orientation_rule = ""
    if mode_value == "Guidance":
        orientation_rule = """
Perception & intent (feature):
- Begin with ONE short line that either (a) clarifies intent (clarity/comfort/direction/correction) or (b) gently reframes the question.
- Keep it universal, grounded, and non-mystical.
"""
    style_rule = "- Be concise, clean, and avoid rambling." if concise_flag else "- Be thorough but still readable. Keep sections tight."
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
{"0) **One-line orientation**" if mode_value == "Guidance" else ""}
1) **Relevant verses** (bullet list: short quote or paraphrase + citation)
2) **Core meaning**
3) **Practical reflection**
4) **If you want to go deeper** (2–4 suggested angles)

Style:
{style_rule}
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
# Quiet reflection feature
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
# Main pipeline (retrieve -> stream with retry)
# =======================
if submitted:
    q = (user_question or "").strip()
    if not q:
        st.stop()

    st.session_state.clarifier = maybe_make_clarifying_question(q) if mode == "Guidance" else ""

    retrieved = retrieve_verses(q, top_k=DEFAULT_TOP_K)
    if not retrieved:
        st.warning("Noor couldn’t confidently retrieve relevant verses from the local dataset. Try rephrasing.")
        st.stop()

    verse_context_lines = [
        f'{int(v["surah"])}:{int(v["ayah"])} — {clip(v["text"], 360)}'
        for v in retrieved
    ]
    verse_context = "\n".join(verse_context_lines)

    st.session_state.last_retrieved = retrieved

    st.session_state.history.append({"role": "user", "content": q})
    st.session_state.history = st.session_state.history[-8:]

    system_prompt = build_system_prompt(concise, mode)
    user_prompt = f"""
User question:
{q}

You MUST ground your answer in these retrieved Qur'an verses:
{verse_context}
""".strip()

    st.markdown("### Your Guidance:")
    box = st.empty()
    full_text = ""

    max_attempts = 2
    last_err = None

    for attempt in range(max_attempts):
        try:
            with st.spinner("Noor is reflecting..."):
                # ensure spinner reliably shows before stream begins
                time.sleep(0.25)

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

            last_err = None
            break

        except (RateLimitError, APITimeoutError) as e:
            last_err = e
            time.sleep(0.9 * (attempt + 1))
        except APIError as e:
            last_err = e
            time.sleep(0.9 * (attempt + 1))
        except Exception as e:
            last_err = e
            time.sleep(0.9 * (attempt + 1))

    if last_err:
        st.warning("A temporary server issue occurred while Noor was responding. Please try again.")
        st.stop()

    st.session_state.last_answer = full_text
    st.session_state.history.append({"role": "assistant", "content": full_text})
    st.session_state.history = st.session_state.history[-8:]

    try:
        refs = "\n".join([f'{int(v["surah"])}:{int(v["ayah"])}' for v in retrieved[:6]])
        st.session_state.followups = generate_followups(q, refs)
    except Exception:
        st.session_state.followups = []

# =======================
# Post-answer features
# =======================
if st.session_state.last_answer and st.session_state.last_retrieved:
    if st.session_state.clarifier:
        st.markdown(f'<div class="small-note">{st.session_state.clarifier}</div>', unsafe_allow_html=True)

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
            st.markdown(f"**({int(v['surah'])}:{int(v['ayah'])})** — {v['text']}")

    with st.expander("Show surrounding verses (context window)"):
        verses_all, _, _ = load_quran_and_index()
        for v in st.session_state.last_retrieved[:2]:
            s, a = int(v["surah"]), int(v["ayah"])
            around = get_surrounding(verses_all, s, a, window=2)
            st.markdown(f"**Context around ({s}:{a})**")
            for x in around:
                st.markdown(f"- **({int(x['surah'])}:{int(x['ayah'])})** — {x['text']}")
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
