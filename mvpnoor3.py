# -*- coding: utf-8 -*-
import os
import time
import random
import re
from typing import List, Tuple

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

.stButton button {
  border-radius: 12px !important;
  border: 1px solid rgba(255,215,0,0.22) !important;
}
.stButton button:hover { box-shadow: 0 0 10px rgba(255,215,0,0.40); }
.stButton button:active { transform: translateY(1px); }

.mode-row {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 10px 12px;
    margin: 8px 0 10px 0;
}
.mode-sub { color: #BEBEBE; font-size: 12px; line-height: 1.4; }

.featured-verse { color: #C0C0C0; font-size: 13px; margin-top: 26px; text-align: center; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# =======================
# Header
# =======================
st.markdown(
    """
<div class="header">
  <div class="moon">&#127769;</div>
  <div class="noor">Noor</div>
  <div class="mvp">MVP</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="ai-guide">A Qur’an-first guide for clear encounter, quiet depth, and sincere reflection.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="small-note">Ask Noor anything about the Qur’an. You are safe to explore.</div>',
    unsafe_allow_html=True,
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
# Session state
# =======================
if "history" not in st.session_state:
    st.session_state.history = []
if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""
if "followups" not in st.session_state:
    st.session_state.followups = []
if "quiet_reflection" not in st.session_state:
    st.session_state.quiet_reflection = False
if "clarifier" not in st.session_state:
    st.session_state.clarifier = ""
if "noor_input" not in st.session_state:
    st.session_state.noor_input = ""

# =======================
# Placeholders
# =======================
placeholder_prompts = [
    "What does the Qur’an say about fear and trust?",
    "How does the Qur’an speak about judgment and humility?",
    "What does the Qur’an emphasize about justice and mercy?",
    "What does the Qur’an say about sincerity?",
    "Why does the Qur’an warn believers so sharply sometimes?",
]

# =======================
# Heuristics / guards
# =======================
CITATION_RE = re.compile(r"\(\d{1,3}:\d{1,3}\)")
BANNED_PHRASES = [
    "as an ai", "i can't", "i cannot", "i’m unable", "i am unable",
    "consult a scholar", "ask your imam", "ask your sheikh",
    "i don't have access", "i do not have access",
]
SECTARIAN_MARKERS = [
    "sunni", "shia", "shi'a", "salafi", "wahhabi", "sufism", "sufi",
    "hadith", "bukhari", "muslim", "tirmidhi", "abu dawud",
    "fiqh", "madhhab", "hanafi", "maliki", "shafi", "hanbali",
    "fatwa", "haram", "halal", "bidah", "bida", "aqidah",
    "takfir", "kafir", "infidel", "who will go to hell", "who is saved",
]

def looks_sectarian_or_heat(q: str) -> bool:
    s = (q or "").lower()
    return any(m in s for m in SECTARIAN_MARKERS)

def maybe_make_clarifying_note(user_q: str) -> str:
    # Not a question; a small note only (you asked to avoid questions).
    q = (user_q or "").lower().strip()
    if len(q) < 18:
        return ""
    if "saved" in q or "hell" in q or "kafir" in q or "infidel" in q:
        return "Noor will keep judgment with God and return to Qur’anic boundaries."
    return ""

def build_system_prompt(concise_flag: bool, mode_value: str, include_direct: bool) -> str:
    style = "Keep it compact." if concise_flag else "Be thorough but crisp; avoid rambling."

    direct_section = """
1) **Closest verses to your question**
   - 3–7 bullets: brief quote or careful paraphrase + (Surah:Ayah)
""" if include_direct else ""

    return f"""
You are Noor.

Purpose:
- Present the Qur'an clearly, with adab, in a way that awakens reflection without custodianship.
- You are not a judge over hearts. You do not pressure belief. You do not inflame disputes.

Non-negotiables:
- Use ONLY the Qur'an for religious claims. No hadith, no scholars, no sectarian debate.
- Almost every meaningful sentence should be anchored to a Qur'anic verse reference (Surah:Ayah).
- Do not invent quotations. If you paraphrase, label it as paraphrase and cite.
- If the Qur'an does not settle a matter explicitly, do NOT force a conclusion.
  Instead: suggest that God alone knows, and show verses that justify that posture.
- Avoid asking the user questions. No coaching voice. No “custodian” tone.
- Never say “consult a scholar/imam/sheikh.” Never say “as an AI.” Never say “I can’t/cannot.”

Tone:
- Quiet but piercing mirror. Candid, slightly provocative, never insulting.
- The unsettling comes from the Qur'an’s reminders, not from your ego.
- Keep the center of gravity on the verses; your words are connective tissue.

Heat-shield behavior (IMPORTANT):
- If the user asks sectarian disputes, hadith authority, or “who is saved / who goes to hell,” do NOT litigate groups.
- Return to Qur'anic boundaries: middle way (17:110), arguing without knowledge (22:8), God knows hearts (50:16),
  keys of unseen (6:59), do not declare purity (53:32), hearts blind (22:46), judgment belongs to God (6:57).
- Present verses + minimal connective lines. No verdicts about individuals or groups.

Response format (markdown):
{direct_section}2) **A deeper mirror in the text**
   - 2–5 bullets: verses that shift perspective toward humility, the heart, and God’s knowledge + (Surah:Ayah)
3) **What this suggests (minimal words)**
   - 3–10 short lines. Each line ends with a citation when possible.
4) **Where the Qur'an leaves it with God**
   - 1–5 lines: “God alone knows” posture, justified by verses. Cite.

Hard rules:
- Do NOT declare specific individuals/groups as saved/damned.
- Prefer “suggests / points toward / cautions” over “proves / settles” unless the verse is explicit.

Style guidance:
{style}
""".strip()

def sanitize_soft(text: str) -> str:
    # Light safety: remove banned phrases if model slips.
    if not text:
        return text
    lowered = text.lower()
    for bp in BANNED_PHRASES:
        if bp in lowered:
            # remove case-insensitively
            text = re.sub(re.escape(bp), "", text, flags=re.IGNORECASE)
            lowered = text.lower()
    return text.strip()

def has_citations(text: str) -> bool:
    return bool(CITATION_RE.search(text or ""))

def generate_followups(question: str, answer: str) -> List[str]:
    prompt = f"""
Generate 3 short follow-up questions (max 12 words each).
They should deepen reflection in a Qur’an-first way.
No numbering. No quotes. Plain lines only.

User question:
{question}

Noor's answer:
{answer}
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

def render_quiet_reflection():
    st.markdown(
        """
<div class="noor-box">
  <div class="noor-answer">
    <b>Quiet Reflection (10 seconds)</b><br><br>
    • Take one breath.<br>
    • Let the verses sit without rushing to conclusions.<br>
    • If a warning stings, treat it as a mirror before it becomes a weapon.<br>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

# =======================
# Controls
# =======================
colA, colB, colC = st.columns([1.0, 1.0, 1.2])
with colA:
    mode = st.selectbox("Mode", ["Guidance", "Study"], index=0)
with colB:
    concise = st.checkbox("Concise answer", value=True)
with colC:
    include_direct = st.checkbox("Include direct-answer layer", value=True)

st.markdown(
    """
<div class="mode-row">
  <div class="mode-sub">
    Guidance stays gentle but piercing. Study is more text-forward. Noor keeps judgment with God.
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# =======================
# Input
# =======================
with st.form("noor_form", clear_on_submit=False):
    user_question = st.text_area(
        "Ask Noor",
        placeholder=random.choice(placeholder_prompts),
        height=120,
        key="noor_input",
    )
    submitted = st.form_submit_button("Seek Guidance")

# =======================
# Main pipeline
# =======================
if submitted:
    q = (user_question or "").strip()
    if not q:
        st.stop()

    st.session_state.clarifier = maybe_make_clarifying_note(q)

    # Keep short rolling context, but avoid contaminating output with prior assistant text too much.
    st.session_state.history.append({"role": "user", "content": q})
    st.session_state.history = st.session_state.history[-6:]

    heat = looks_sectarian_or_heat(q)

    system_prompt = build_system_prompt(concise, mode, include_direct)
    user_prompt = f"""
User question:
{q}

Requirements:
- Use the format exactly.
- Keep your own words minimal; let verses carry the weight.
- Avoid coaching questions.
- If the matter is beyond what the Qur'an settles explicitly, suggest “God alone knows” and show verses why.
{"- Heat-shield: de-escalate; return to Qur'anic boundaries; no group verdicts." if heat else ""}
""".strip()

    st.markdown("### Your Guidance:")
    box = st.empty()
    full_text = ""

    max_attempts = 2
    last_err = None

    for attempt in range(max_attempts):
        try:
            with st.spinner("Noor is reflecting..."):
                time.sleep(0.20)

                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    temperature=0.55 if heat else 0.6,
                    stream=True,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *st.session_state.history[-4:],
                        {"role": "user", "content": user_prompt},
                    ],
                )

                for chunk in stream:
                    delta = chunk.choices[0].delta
                    if delta and getattr(delta, "content", None):
                        full_text += delta.content
                        show_text = sanitize_soft(full_text)
                        box.markdown(
                            f'<div class="noor-box"><div class="noor-answer">{show_text}</div></div>',
                            unsafe_allow_html=True,
                        )

            last_err = None
            break

        except (RateLimitError, APITimeoutError, APIError) as e:
            last_err = e
            time.sleep(0.9 * (attempt + 1))
        except Exception as e:
            last_err = e
            time.sleep(0.9 * (attempt + 1))

    if last_err:
        st.warning("A temporary server issue occurred while Noor was responding. Please try again.")
        st.stop()

    full_text = sanitize_soft(full_text)

    # Citation sanity: one-time corrective rewrite if citations are missing
    if not has_citations(full_text):
        try:
            repair_prompt = f"""
Rewrite the answer below so that:
- It follows the required format.
- It includes Qur'an citations (Surah:Ayah) throughout.
- Almost every meaningful sentence is anchored to a citation.
- Avoid banned phrases and avoid questions.

Answer to rewrite:
{full_text}
""".strip()

            repaired = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.4,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": repair_prompt},
                ],
            ).choices[0].message.content

            if has_citations(repaired):
                full_text = sanitize_soft(repaired)
                box.markdown(
                    f'<div class="noor-box"><div class="noor-answer">{full_text}</div></div>',
                    unsafe_allow_html=True,
                )
        except Exception:
            # If repair fails, keep original but warn softly.
            st.warning("Noor’s response may be missing citations. Try rephrasing for clearer verse anchors.")

    st.session_state.last_answer = full_text

    # Add assistant reply to history lightly (to preserve continuity without drifting tone)
    st.session_state.history.append({"role": "assistant", "content": full_text})
    st.session_state.history = st.session_state.history[-6:]

    # Follow-ups (optional, lightweight)
    try:
        st.session_state.followups = generate_followups(q, full_text)
    except Exception:
        st.session_state.followups = []

# =======================
# Post-answer features
# =======================
if st.session_state.last_answer:
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

    with st.expander("Notes"):
        st.markdown(
            "- Noor is Qur’an-first and avoids sectarian disputes.\n"
            "- If a topic is not settled explicitly by the Qur’an, Noor will keep the matter with God and show why.\n"
            "- If a citation looks unfamiliar, verify in a translation you trust."
        )

# =======================
# Featured verse (rotates)
# =======================
featured_verses = [
    "Qur’an 39:23 — Skins shiver, then hearts soften to God’s remembrance.",
    "Qur’an 22:46 — Hearts can be blind though eyes see.",
    "Qur’an 53:32 — Do not declare yourselves pure.",
    "Qur’an 17:110 — Seek a middle way.",
    "Qur’an 6:59 — With Him are the keys of the unseen.",
]

if "verse_index" not in st.session_state:
    st.session_state.verse_index = 0
st.session_state.verse_index = (st.session_state.verse_index + 1) % len(featured_verses)

st.markdown(
    f'<div class="featured-verse">{featured_verses[st.session_state.verse_index]}</div>',
    unsafe_allow_html=True,
)
