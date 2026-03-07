import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="NoorMVP", page_icon="🌙", layout="centered")

if "verse_index" not in st.session_state:
    st.session_state.verse_index = 0

verse_states = [
    ("39:53", "59:23", "2:177"),
    ("59:23", "2:177", "39:53"),
    ("2:177", "39:53", "59:23"),
]

left_verse, center_verse, right_verse = verse_states[st.session_state.verse_index]

st.markdown("""
<style>

.stApp{
background:
radial-gradient(circle at 20% 10%, rgba(120,70,255,0.20), transparent 55%),
radial-gradient(circle at 85% 25%, rgba(80,200,255,0.10), transparent 60%),
linear-gradient(180deg,#070910,#0b0b14);
color:white;
font-family:serif;
}

main .block-container{
max-width:900px;
padding-top:3.2rem;
padding-bottom:2rem;
}

.title{
text-align:center;
font-size:44px;
font-weight:800;
margin-top:20px;
}

.moon{
display:inline-block;
animation:moonspin 30s linear infinite;
filter:drop-shadow(0 0 20px rgba(180,140,255,0.6));
}

@keyframes moonspin{
from{transform:rotate(0deg);}
to{transform:rotate(360deg);}
}

.message{
text-align:center;
font-size:18px;
margin-top:30px;
line-height:1.8;
}

.verses{
text-align:center;
margin-top:70px;
letter-spacing:3px;
min-height:70px;
}

.v-small{
font-size:26px;
opacity:0.8;
}

.v-mid{
font-size:46px;
font-weight:900;
padding:0 12px;
display:inline-block;
animation:heartbeat 1.2s ease-in-out 3;
text-shadow:0 0 18px rgba(255,255,255,0.35);
}

@keyframes heartbeat{
0%{transform:scale(1);}
20%{transform:scale(1.15);}
40%{transform:scale(1);}
60%{transform:scale(1.15);}
80%{transform:scale(1);}
100%{transform:scale(1);}
}

.dot{
padding:0 12px;
opacity:0.4;
}

.sub-verses{
text-align:center;
margin-top:25px;
font-size:18px;
letter-spacing:2px;
opacity:0.6;
}

.beewrap{
position:fixed;
top:0;
left:0;
width:100vw;
height:100vh;
pointer-events:none;
overflow:hidden;
z-index:20;
}

.bee{
position:absolute;
font-size:14px;
animation:beex 12s linear infinite alternate, beey 8s linear infinite alternate;
}

@keyframes beex{
from{left:10vw;}
to{left:85vw;}
}

@keyframes beey{
from{top:20vh;}
to{top:78vh;}
}

.footerwrap{
margin-top:120px;
display:flex;
justify-content:center;
}

.footer{
display:flex;
gap:12px;
max-width:720px;
font-size:14px;
opacity:0.7;
border-top:1px solid rgba(255,255,255,0.1);
padding-top:18px;
line-height:1.6;
}

.spinner{
width:16px;
height:16px;
border:2px solid rgba(255,255,255,0.2);
border-top:2px solid white;
border-radius:50%;
animation:spin 1.2s linear infinite;
flex-shrink:0;
margin-top:2px;
}

@keyframes spin{
from{transform:rotate(0deg);}
to{transform:rotate(360deg);}
}

@media (max-width:700px){
.title{font-size:38px;}
.message{font-size:17px;}
.v-small{font-size:22px;}
.v-mid{font-size:38px;}
.dot{padding:0 8px;}
.sub-verses{font-size:16px;}
.footer{font-size:13px;}
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title"><span class="moon">🌙</span> NoorMVP</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="message">
Sorry for the delay. Noor is reprogramming itself after several recurring errors. Thanks for your understanding.<br><br>
Please come back later.
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
    16:68 · 16:114
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="beewrap">
    <div class="bee">🐝</div>
</div>
""",
    unsafe_allow_html=True,
)

components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
body{
margin:0;
background:transparent;
overflow:hidden;
font-family:serif;
}
.scene{
position:relative;
width:100%;
height:100px;
background:transparent;
opacity:0.55;
}
.obj{
position:absolute;
user-select:none;
white-space:nowrap;
}
#spider{
font-size:14px;
left:120px;
top:38px;
}
#ayah{
font-size:11px;
color:rgba(255,255,255,0.60);
left:300px;
top:56px;
}
</style>
</head>
<body>
<div class="scene">
    <div id="spider" class="obj">🕷️</div>
    <div id="ayah" class="obj">29:41</div>
</div>

<script>
const spider = document.getElementById("spider");
const ayah = document.getElementById("ayah");

let x1 = 120, y1 = 38, vx1 = 1.0, vy1 = 0.8;
let x2 = 300, y2 = 56, vx2 = -0.9, vy2 = 0.7;

function move() {
    x1 += vx1;
    y1 += vy1;
    x2 += vx2;
    y2 += vy2;

    if (x1 < 0 || x1 > 800) vx1 *= -1;
    if (y1 < 0 || y1 > 80) vy1 *= -1;

    if (x2 < 0 || x2 > 800) vx2 *= -1;
    if (y2 < 0 || y2 > 80) vy2 *= -1;

    const dx = x1 - x2;
    const dy = y1 - y2;
    const dist = Math.sqrt(dx * dx + dy * dy);

    if (dist < 28) {
        vx1 *= -1;
        vy1 *= -1;
        vx2 *= -1;
        vy2 *= -1;
    }

    spider.style.transform = `translate(${x1}px, ${y1}px)`;
    ayah.style.transform = `translate(${x2}px, ${y2}px)`;

    requestAnimationFrame(move);
}

move();
</script>
</body>
</html>
""", height=100)

st.markdown(
    """
<div class="footerwrap">
    <div class="footer">
        <div class="spinner"></div>
        <div>
            Noor is actively reprogramming itself—undertaking the careful work of consideration.<br>
            Noor is your AI guide that brings darkness to light through the Qur’an.
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

time.sleep(3)
st.session_state.verse_index = (st.session_state.verse_index + 1) % len(verse_states)
st.rerun()
