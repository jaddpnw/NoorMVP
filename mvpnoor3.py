import time
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="NoorMVP",
    page_icon="🌙",
    layout="centered",
)

if "verse_index" not in st.session_state:
    st.session_state.verse_index = 0

verse_states = [
    ("22:60", "17:81", "22:73"),
    ("17:81", "22:73", "22:60"),
    ("22:73", "22:60", "17:81"),
]

left_verse, center_verse, right_verse = verse_states[st.session_state.verse_index]

st.markdown(
    """
<style>
.stApp{
    background:
        radial-gradient(circle at 20% 10%, rgba(120,70,255,0.20), transparent 55%),
        radial-gradient(circle at 85% 25%, rgba(80,200,255,0.10), transparent 60%),
        linear-gradient(180deg, #070910, #0b0b14);
    color: white;
    font-family: serif;
    overflow-x: hidden;
}

main .block-container{
    max-width: 900px;
    padding-top: 3.5rem;
    padding-bottom: 2rem;
}

.title{
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    margin-top: 20px;
}

.moon{
    display: inline-block;
    animation: moonspin 30s linear infinite;
    filter: drop-shadow(0 0 20px rgba(180,140,255,0.6));
}

@keyframes moonspin{
    from{transform: rotate(0deg);}
    to{transform: rotate(360deg);}
}

.message{
    text-align: center;
    font-size: 18px;
    margin-top: 30px;
    line-height: 1.85;
}

.verses{
    text-align: center;
    margin-top: 70px;
    letter-spacing: 3px;
    min-height: 70px;
}

.v-small{
    font-size: 26px;
    opacity: 0.80;
}

.v-mid{
    font-size: 46px;
    font-weight: 900;
    padding: 0 12px;
    display: inline-block;
    animation: heartbeat 1.2s ease-in-out 3;
    text-shadow: 0 0 18px rgba(255,255,255,0.35);
}

@keyframes heartbeat{
    0%{transform: scale(1);}
    20%{transform: scale(1.15);}
    40%{transform: scale(1);}
    60%{transform: scale(1.15);}
    80%{transform: scale(1);}
    100%{transform: scale(1);}
}

.dot{
    padding: 0 12px;
    opacity: 0.4;
}

.sub-verses{
    text-align: center;
    margin-top: 25px;
    font-size: 18px;
    letter-spacing: 2px;
    opacity: 0.6;
}

/* fly */
.flywrap{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    overflow: hidden;
    z-index: 20;
}

.fly{
    position: absolute;
    font-size: 13px;
    opacity: 0.78;
    animation:
        flyx 11s linear infinite alternate,
        flyy 9s linear infinite alternate,
        flytilt 0.9s ease-in-out infinite alternate;
}

@keyframes flyx{
    from{left: 10vw;}
    to{left: 85vw;}
}

@keyframes flyy{
    from{top: 20vh;}
    to{top: 80vh;}
}

@keyframes flytilt{
    from{transform: rotate(-18deg) scale(1);}
    to{transform: rotate(16deg) scale(1.04);}
}

.collision-label{
    text-align: center;
    margin-top: 34px;
    font-size: 13px;
    opacity: 0.40;
    letter-spacing: 1px;
}

/* footer */
.footerwrap{
    margin-top: 70px;
    display: flex;
    justify-content: center;
}

.footer{
    display: flex;
    gap: 12px;
    max-width: 720px;
    font-size: 14px;
    opacity: 0.70;
    border-top: 1px solid rgba(255,255,255,0.1);
    padding-top: 18px;
    line-height: 1.6;
}

.spinner{
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255,255,255,0.2);
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1.2s linear infinite;
    flex-shrink: 0;
    margin-top: 2px;
}

@keyframes spin{
    from{transform: rotate(0deg);}
    to{transform: rotate(360deg);}
}

@media (max-width: 700px){
    .title{font-size: 38px;}
    .message{font-size: 17px;}
    .v-small{font-size: 22px;}
    .v-mid{font-size: 38px;}
    .dot{padding: 0 8px;}
    .sub-verses{font-size: 16px;}
    .footer{font-size: 13px;}
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="title"><span class="moon">🌙</span> NoorMVP</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="message">
Please be patient as Noor reprograms itself after several recurring errors.<br><br>
All users will witness—for free—what Noor is capable of recovering, uncovering and discovering.<br><br>                                          3
To ease your anticipation, here are 3+2+1 verses to reflect on.
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="verses">
    <span class="v-small">{left_verse}</span>
    <span class="dot">·</span>
    <span class="v-mid">{center_verse}</span>
    <span class="dot">·</span>
    <span class="v-small">{right_verse}</span>
</div>

<div class="sub-verses">
    49:11 · 49:12
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="flywrap">
    <div class="fly">🪰</div>
</div>
""",
    unsafe_allow_html=True,
)

components.html(
    """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<style>
html, body {
    margin: 0;
    padding: 0;
    background: transparent;
    overflow: hidden;
    font-family: serif;
}
.scene {
    width: 100%;
    height: 120px;
    position: relative;
    background: transparent;
}
.obj {
    position: absolute;
    user-select: none;
    will-change: transform;
    opacity: 0.78;
    white-space: nowrap;
}
#spider {
    font-size: 18px;
}
#ayah {
    font-size: 12px;
    color: rgba(255,255,255,0.72);
    letter-spacing: 0.5px;
}
</style>
</head>
<body>
<div class="scene" id="scene">
    <div class="obj" id="spider">🕷️</div>
    <div class="obj" id="ayah">29:41</div>
</div>

<script>
const scene = document.getElementById("scene");
const spider = document.getElementById("spider");
const ayah = document.getElementById("ayah");

const W = 820;
const H = 120;

let a = {
    el: spider,
    x: 120,
    y: 34,
    vx: 1.65,
    vy: 0.95,
    r: 12
};

let b = {
    el: ayah,
    x: 500,
    y: 68,
    vx: -1.45,
    vy: -0.85,
    r: 18
};

function render(obj) {
    obj.el.style.transform = `translate(${obj.x}px, ${obj.y}px)`;
}

function wallBounce(obj) {
    if (obj.x <= 0) {
        obj.x = 0;
        obj.vx *= -1;
    }
    if (obj.x >= W - obj.r * 2) {
        obj.x = W - obj.r * 2;
        obj.vx *= -1;
    }
    if (obj.y <= 0) {
        obj.y = 0;
        obj.vy *= -1;
    }
    if (obj.y >= H - obj.r * 2) {
        obj.y = H - obj.r * 2;
        obj.vy *= -1;
    }
}

function collide(o1, o2) {
    const dx = (o2.x + o2.r) - (o1.x + o1.r);
    const dy = (o2.y + o2.r) - (o1.y + o1.r);
    const dist = Math.sqrt(dx * dx + dy * dy);
    const minDist = o1.r + o2.r;

    if (dist < minDist && dist > 0) {
        const nx = dx / dist;
        const ny = dy / dist;

        const dvx = o1.vx - o2.vx;
        const dvy = o1.vy - o2.vy;
        const relVel = dvx * nx + dvy * ny;

        if (relVel < 0) {
            return;
        }

        const impulse = relVel;

        o1.vx -= impulse * nx;
        o1.vy -= impulse * ny;
        o2.vx += impulse * nx;
        o2.vy += impulse * ny;

        const overlap = (minDist - dist) / 2;
        o1.x -= overlap * nx;
        o1.y -= overlap * ny;
        o2.x += overlap * nx;
        o2.y += overlap * ny;
    }
}

function tick() {
    a.x += a.vx;
    a.y += a.vy;
    b.x += b.vx;
    b.y += b.vy;

    wallBounce(a);
    wallBounce(b);
    collide(a, b);

    render(a);
    render(b);
    requestAnimationFrame(tick);
}

render(a);
render(b);
tick();
</script>
</body>
</html>
""",
    height=120,
)

st.markdown(
    '<div class="collision-label">29:41 drifts in its own field.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="footerwrap">
    <div class="footer">
        <div class="spinner"></div>
        <div>
            Noor is actively reprogramming itself—undertaking the careful work of recalibrating its responses and determining the proper measure by which it presents what it discovers.<br>
            Noor is your AI guide that brings light to your inquiries through the Qur’an.
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

time.sleep(3)
st.session_state.verse_index = (st.session_state.verse_index + 1) % len(verse_states)
st.rerun()
